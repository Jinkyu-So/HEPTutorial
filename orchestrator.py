"""
Orchestrator for the NewHEPTutorial (Python/RDataFrame) semi-leptonic ttbar
analysis chain.

This is the Python-tutorial equivalent of the old HEPHYU/HEPTutorial
example.C: it wires together object_definition.py -> event_selection.py ->
plot_control.py (histogram/sample config) -> matplotlib plotting, and runs
them in the same order as the four CMS data analysis tutorial exercises
(see the PDFs in NewHEPTutorial/):

  Exercise 1 - warmup: muon multiplicity & dimuon mass at selection "s0"
  Exercise 2 - background-rejection variables across selections s0-s4,
               plus a cutflow (event yields per sample per step)
  Exercise 3 - trigger efficiency turn-on curve (from TTbar) + the cutflow
               table needed to work out acceptance/purity/cross-section
  Exercise 4 - ttbar mass reconstruction at the tightest selection ("s4")

Usage:
    python orchestrator.py                       # run all four exercises
    python orchestrator.py --exercise 2           # only exercise 2
    python orchestrator.py --exercise 1 2 3 4     # explicit list, in order
    python orchestrator.py --object leading_jet_pt --selection s2
        # ad hoc single-variable plot, independent of the exercise sequence

Data files are expected under NewHEPTutorial/files/ (one level above this
script's directory), matching the filenames in plot_control.samples_config_semileptonic.

Note: this script needs PyROOT (RDataFrame) to run; it was written and its
branch names verified against the real files with uproot, but has not been
executed end to end in this environment because ROOT is not installed here.
Please do a first run yourselves and report back anything that breaks.
"""

import argparse
import csv
import os
from array import array

import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import ROOT

from plot_control import (
    define_objects,
    applycuts_semileptonic,
    get_objects,
    samples_config_semileptonic,
)
from plotter_ver4 import make_plot, th1_to_numpy, MPL_COLORS

HERE = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(HERE, "..", "files")
DEFAULT_OUT_DIR = os.path.join(HERE, "outputs")

ALL_SELECTIONS = ["s0", "s1", "s2", "s3", "s4"]

# Curated subset of get_objects() used for Exercise 2's background-rejection
# study (jet multiplicity, jet/lepton kinematics, isolation, b-tagging, MET -
# the variables the exercise sheet explicitly calls out).
EXERCISE2_OBJECTS = [
    "nmuons",
    "leading_muon_pt",
    "leading_muon_isoID",
    "njets",
    "leading_jet_pt",
    "leading_jet_btag",
    "tight_nbjets",
    "MET",
]

EXERCISE1_OBJECTS = ["nmuons", "nextra_loose_muons", "dimuon_mass", "dimuon_mass_thinbins"]
EXERCISE4_OBJECTS = ["hadTop_mass", "lepTop_mass", "hadW_mass", "lepW_mt"]

DATA_LUMI = samples_config_semileptonic["Data"][4]


# --------------------------------------------------------------------------
# Sample loading
# --------------------------------------------------------------------------

def load_sample(name, require_trigger=True):
    """Build the RDataFrame for one configured sample: objects defined,
    optionally trigger-required, with a uniform "event_weight" column
    (1.0 for data, luminosity-scaled MC weight otherwise)."""

    filename, label, _root_color, is_data, lumi_ref = samples_config_semileptonic[name]
    path = os.path.join(FILES_DIR, filename)
    df = ROOT.RDataFrame("Events", path)

    if require_trigger:
        df = df.Filter("HLT_IsoMu24", "trigger")

    df = define_objects(df, "Events")

    if is_data:
        df = df.Define("event_weight", "1.0")
    else:
        # eventWeight normalizes this MC sample to represent `lumi_ref`
        # pb^-1 of data (see samples_config_semileptonic); rescale to the
        # actual data luminosity so MC and data are on the same footing.
        df = df.Define("event_weight", f"({DATA_LUMI} / {lumi_ref}) * eventWeight")

    return df, label, is_data


def apply_selection(df, selection):
    return applycuts_semileptonic(df, selection)


# --------------------------------------------------------------------------
# Histogram booking / plotting
#
# Plotting itself is delegated to plotter_ver4.make_plot (that's the plotter
# this project standardized on) - this module only handles sample loading,
# selection, and histogram booking, then hands the filled histograms to it.
# --------------------------------------------------------------------------

def run_objects_for_selection(selection, object_keys, out_dir, require_trigger=True):
    """Load every sample once, book histograms for all requested variables
    in a single pass per sample (RDataFrame batches these together), then
    save one stacked plot per variable."""

    objects_config = {k: get_objects()[k] for k in object_keys}
    hep.style.use("CMS")

    results = {obj_name: {"data": None, "MC": []} for obj_name in objects_config}

    for name in samples_config_semileptonic:
        df, label, is_data = load_sample(name, require_trigger=require_trigger)
        df = apply_selection(df, selection)

        booked = {}
        for obj_name, config in objects_config.items():
            col_name = f"plot_var__{obj_name}"
            df_var = df.Define(col_name, config["variable"])
            hist_model = (f"h_{name}_{obj_name}_{selection}", config["title"], *config["bins"])
            booked[obj_name] = df_var.Histo1D(hist_model, col_name, "event_weight")

        for obj_name, h in booked.items():
            hist = h.GetValue()
            hist.SetDirectory(0)
            if is_data:
                results[obj_name]["data"] = th1_to_numpy(hist)
            else:
                contents, _ = th1_to_numpy(hist)
                mpl_color = MPL_COLORS.get(name, "gray")
                results[obj_name]["MC"].append((contents, label, mpl_color))

    for obj_name, config in objects_config.items():
        make_plot(obj_name, config, selection, results[obj_name], out_dir, DATA_LUMI)


# --------------------------------------------------------------------------
# Cutflow (feeds Exercise 2's background-rejection study and Exercise 3's
# efficiency / purity / cross-section ingredients)
# --------------------------------------------------------------------------

def build_cutflow(selections=ALL_SELECTIONS, require_trigger=True):
    """Book raw and weighted event counts for every (sample, selection),
    deferring GetValue() until everything is booked so each sample's file
    is only read once."""

    pending = {}
    for name in samples_config_semileptonic:
        df, label, is_data = load_sample(name, require_trigger=require_trigger)
        pending[name] = {"label": label, "is_data": is_data, "counts": {}}
        for sel in selections:
            df_sel = apply_selection(df, sel)
            pending[name]["counts"][sel] = (df_sel.Count(), df_sel.Sum("event_weight"))

    rows = []
    for name, info in pending.items():
        row = {"sample": name, "label": info["label"], "is_data": info["is_data"]}
        for sel in selections:
            n_raw_h, n_w_h = info["counts"][sel]
            row[f"{sel}_raw"] = n_raw_h.GetValue()
            row[f"{sel}_weighted"] = n_w_h.GetValue()
        rows.append(row)
    return rows


def write_cutflow_csv(rows, selections, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fieldnames = ["sample", "label", "is_data"]
    for sel in selections:
        fieldnames += [f"{sel}_raw", f"{sel}_weighted"]
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  wrote {out_path}")


def print_cutflow(rows, selections):
    header = f"{'sample':<8}" + "".join(f"{sel:>14}" for sel in selections)
    print(header)
    for row in rows:
        line = f"{row['sample']:<8}" + "".join(f"{row[f'{sel}_weighted']:>14.1f}" for sel in selections)
        print(line)


# --------------------------------------------------------------------------
# Trigger efficiency (Exercise 3, first bullet)
# --------------------------------------------------------------------------

def trigger_efficiency_plot(out_dir, pt_edges=(0, 10, 20, 25, 30, 40, 60, 100)):
    """TTbar is the only sample that also contains non-triggered events, so
    it is what lets us measure the HLT_IsoMu24 turn-on curve vs muon pT."""

    filename, label, _root_color, is_data, _lumi = samples_config_semileptonic["TTbar"]
    path = os.path.join(FILES_DIR, filename)

    df = ROOT.RDataFrame("Events", path)          # no trigger filter here on purpose
    df = define_objects(df, "Events")
    df = df.Filter("nGoodMuon >= 1")
    df = df.Define("leadmu_pt", "GoodMuon_pt[0]")

    edges = array("d", pt_edges)
    nbins = len(pt_edges) - 1

    h_all = df.Histo1D(("h_trig_all", "", nbins, edges), "leadmu_pt", "eventWeight")
    h_pass = df.Filter("HLT_IsoMu24").Histo1D(("h_trig_pass", "", nbins, edges), "leadmu_pt", "eventWeight")

    all_contents, _ = th1_to_numpy(h_all.GetValue())
    pass_contents, _ = th1_to_numpy(h_pass.GetValue())

    with np.errstate(divide="ignore", invalid="ignore"):
        eff = np.where(all_contents > 0, pass_contents / all_contents, 0.0)
        err = np.where(all_contents > 0, np.sqrt(eff * (1 - eff) / all_contents), 0.0)

    centers = 0.5 * (np.array(pt_edges[:-1]) + np.array(pt_edges[1:]))

    hep.style.use("CMS")
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.errorbar(centers, eff, yerr=err, xerr=np.diff(pt_edges) / 2, fmt="o", color="black")
    ax.axvline(25, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel(r"Leading muon $p_T$ (GeV)")
    ax.set_ylabel("HLT_IsoMu24 efficiency")
    ax.set_ylim(0, 1.1)
    hep.cms.label("Preliminary", data=False, lumi=DATA_LUMI, year=2018, ax=ax)

    save_path = os.path.join(out_dir, "trigger_efficiency.pdf")
    os.makedirs(out_dir, exist_ok=True)
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {save_path}")

    # efficiency for muon pT > 25 GeV specifically, as asked in Exercise 3
    df_25 = df.Filter("leadmu_pt > 25")
    n_25 = df_25.Sum("eventWeight").GetValue()
    n_25_trig = df_25.Filter("HLT_IsoMu24").Sum("eventWeight").GetValue()
    eff_25 = n_25_trig / n_25 if n_25 > 0 else float("nan")
    print(f"  trigger efficiency for muon pT > 25 GeV (TTbar MC): {eff_25:.3f}")
    return eff_25


# --------------------------------------------------------------------------
# Exercises
# --------------------------------------------------------------------------

def exercise1(out_root, require_trigger=True):
    print("Exercise 1: muon multiplicity & dimuon mass (selection s0)")
    out_dir = os.path.join(out_root, "exercise1")
    run_objects_for_selection("s0", EXERCISE1_OBJECTS, out_dir, require_trigger=require_trigger)


def exercise2(out_root, require_trigger=True):
    print("Exercise 2: background-rejection variables across s0-s4 + cutflow")
    out_dir = os.path.join(out_root, "exercise2")
    for sel in ALL_SELECTIONS:
        print(f" selection {sel}")
        run_objects_for_selection(sel, EXERCISE2_OBJECTS, out_dir, require_trigger=require_trigger)

    rows = build_cutflow(ALL_SELECTIONS, require_trigger=require_trigger)
    print_cutflow(rows, ALL_SELECTIONS)
    write_cutflow_csv(rows, ALL_SELECTIONS, os.path.join(out_dir, "cutflow.csv"))


def exercise3(out_root, require_trigger=True):
    print("Exercise 3: trigger efficiency + cutflow-based purity")
    out_dir = os.path.join(out_root, "exercise3")

    eff_25 = trigger_efficiency_plot(out_dir)

    rows = build_cutflow(ALL_SELECTIONS, require_trigger=require_trigger)
    print_cutflow(rows, ALL_SELECTIONS)
    write_cutflow_csv(rows, ALL_SELECTIONS, os.path.join(out_dir, "cutflow.csv"))

    final_sel = ALL_SELECTIONS[-1]
    signal = next(r for r in rows if r["sample"] == "TTbar")[f"{final_sel}_weighted"]
    background = sum(
        r[f"{final_sel}_weighted"] for r in rows if not r["is_data"] and r["sample"] != "TTbar"
    )
    data_obs = next(r for r in rows if r["is_data"])[f"{final_sel}_weighted"]
    purity = signal / (signal + background) if (signal + background) > 0 else float("nan")

    summary_path = os.path.join(out_dir, "summary.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(summary_path, "w") as f:
        f.write(f"Trigger efficiency (muon pT > 25 GeV, TTbar MC): {eff_25:.3f}\n")
        f.write(f"Selection '{final_sel}' expected TTbar yield:      {signal:.2f}\n")
        f.write(f"Selection '{final_sel}' expected background yield: {background:.2f}\n")
        f.write(f"Purity S/(S+B) at '{final_sel}':                   {purity:.3f}\n")
        f.write(f"Observed data yield at '{final_sel}':               {data_obs:.2f}\n")
        f.write(
            "\nUse these numbers with the acceptance (generated vs. selected TTbar events,\n"
            "from the generator-level MC_* branches) and the known TTbar branching fraction\n"
            "to work out the cross-section by hand, following the exercise sheet.\n"
            "This script does not compute the final cross-section number for you -\n"
            "that derivation is the point of Exercise 3.\n"
        )
    print(f"  wrote {summary_path}")


def exercise4(out_root, require_trigger=True):
    print("Exercise 4: ttbar mass reconstruction (selection s4)")
    out_dir = os.path.join(out_root, "exercise4")
    run_objects_for_selection("s4", EXERCISE4_OBJECTS, out_dir, require_trigger=require_trigger)


EXERCISES = {1: exercise1, 2: exercise2, 3: exercise3, 4: exercise4}


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="NewHEPTutorial ttbar analysis orchestrator")
    parser.add_argument(
        "--exercise", nargs="+", type=int, choices=[1, 2, 3, 4], default=[1, 2, 3, 4],
        help="which exercise(s) to run, in the order given (default: 1 2 3 4)",
    )
    parser.add_argument("--out", default=DEFAULT_OUT_DIR, help="output directory")
    parser.add_argument(
        "--no-trigger", action="store_true",
        help="skip the HLT_IsoMu24 requirement (debugging only)",
    )
    parser.add_argument(
        "--object", choices=list(get_objects().keys()), default=None,
        help="ad hoc: plot a single variable instead of running an exercise",
    )
    parser.add_argument("--selection", choices=ALL_SELECTIONS, default="s0")
    args = parser.parse_args()

    require_trigger = not args.no_trigger

    if args.object is not None:
        run_objects_for_selection(args.selection, [args.object], args.out, require_trigger=require_trigger)
        return

    for ex in args.exercise:
        EXERCISES[ex](args.out, require_trigger=require_trigger)


if __name__ == "__main__":
    main()
