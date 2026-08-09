import ROOT
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from plot_control import applycuts_semileptonic, samples_config_semileptonic, define_objects, get_objects


MPL_COLORS = {
    "TTbar": "#f89c20",
    "QCD":   "#5790fc",
    "ST":    "#e42536",
    "DY":    "#92dadd",
    "WJets": "#83c246",
    "WW":    "#f5e401",
    "WZ":    "#e8d200",
    "ZZ":    "#dbc800",
}
DATA_COLOR = "black"

ROOT_TO_MPL = {
    "p_{T}": r"$p_T$", "H_{T}": r"$H_T$", "S_{T}": r"$S_T$", "E_{T}": r"$E_T$",
    "m_{#mu#mu}": r"$m_{\mu\mu}$", "m_{T}(W)": r"$m_T(W)$", "#mu#mu": r"$\mu\mu$",
    "#mu": r"$\mu$", "#nu": r"$\nu$", "#eta": r"$\eta$", "#phi": r"$\phi$",
    "#bar{t}": r"$\bar{t}$", "#bar{b}": r"$\bar{b}$",
}


def th1_to_numpy(hist):
    n = hist.GetNbinsX()
    contents = np.array([hist.GetBinContent(i + 1) for i in range(n)])
    errors = np.array([hist.GetBinError(i + 1) for i in range(n)])
    return contents, errors


def make_plot(obj_name, config, selection, hist_store, plot_dir, luminosity):
    nbins, xmin, xmax = config["bins"]
    edges = np.linspace(xmin, xmax, nbins + 1)

    fig, ax = plt.subplots(figsize=(9, 7))

    max_val = 0
    if hist_store["MC"]:
        mc_contents, mc_labels, mc_colors = zip(*hist_store["MC"])

        hep.histplot(
            mc_contents,
            bins=edges,
            stack=True,
            histtype="fill",
            label=mc_labels,
            color=mc_colors,
            edgecolor="black",
            linewidth=0.5,
            ax=ax,
        )
        max_val = max(max_val, np.sum(mc_contents, axis=0).max())

    data = hist_store["data"]
    if data is not None:
        contents, errors = data
        centers = 0.5 * (edges[:-1] + edges[1:])
        ax.errorbar(
            centers, contents, yerr=errors,
            fmt="o", color=DATA_COLOR, markersize=5, label="Data",
        )
        max_val = max(max_val, contents.max())

    xlabel = config["xlabel"]
    for old, new in ROOT_TO_MPL.items():
        xlabel = xlabel.replace(old, new)

    ax.set_xlabel(xlabel)
    ax.set_ylabel("Events")
    ax.set_ylim(0, max_val * 1.5)
    ax.legend(fontsize=14, frameon=False)
    ax.text(0.98, 0.94, selection, transform=ax.transAxes, ha="right", va="top", fontsize=14)

    hep.cms.label("Preliminary", data=True, lumi=luminosity, year=2018, ax=ax)

    save_path = os.path.join(plot_dir, selection, f"{obj_name}_{selection}.pdf") #check
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Created: {save_path}")


def main():
    data_dir = "/home/jso/heptutorial/data"
    mc_dir = "/home/jso/heptutorial/mc/merged_MC"
    plot_dir = "/home/jso/heptutorial/plotting/plots/"
    luminosity = 188.09

    all_objects = list(get_objects().keys())
    all_selections = ["s0", "s1", "s2", "s3", "s4"]

    parser = argparse.ArgumentParser(description="CMS Batch Plotter (matplotlib/mplhep)")
    parser.add_argument("--objects", nargs="+", choices=all_objects, default=all_objects,
                        help="플롯할 변수들 (기본값: 전체)")
    parser.add_argument("--selections", nargs="+", choices=all_selections, default=all_selections,
                        help="적용할 selection들 (기본값: 전체)")
    args = parser.parse_args()

    objects_config = {k: get_objects()[k] for k in args.objects}

    hep.style.use("CMS")

    for selection in args.selections:
        results = {obj_name: {"data": None, "MC": []} for obj_name in objects_config}

        for sample_name, (filename, label, _, is_data, _) in samples_config_semileptonic.items():
            full_path = os.path.join(data_dir if is_data else mc_dir, filename)

            df = ROOT.RDataFrame("Events", full_path)
            df = define_objects(df, "Events")
            df = applycuts_semileptonic(df, selection)
            if not is_data:
                df = df.Define(
                    "event_weight",
                    f"{luminosity} * xsecWeight * Pileup_weight * Muon_weight * PUJetID_weight"
                )

            booked = {}
            for obj_name, config in objects_config.items():
                col_name = f"plot_var__{obj_name}"
                df_var = df.Define(col_name, config["variable"])
                hist_model = (f"h_{sample_name}_{obj_name}", config["title"], *config["bins"])
                if is_data:
                    booked[obj_name] = df_var.Histo1D(hist_model, col_name)
                else:
                    booked[obj_name] = df_var.Histo1D(hist_model, col_name, "event_weight")

            for obj_name, h in booked.items():
                hist = h.GetValue()
                hist.SetDirectory(0)
                if is_data:
                    results[obj_name]["data"] = th1_to_numpy(hist)
                else:
                    contents, _ = th1_to_numpy(hist)
                    mpl_color = MPL_COLORS.get(sample_name, "gray")
                    results[obj_name]["MC"].append((contents, label, mpl_color))

        for obj_name, config in objects_config.items():
            make_plot(obj_name, config, selection, results[obj_name], plot_dir, luminosity)


if __name__ == "__main__":
    main()
