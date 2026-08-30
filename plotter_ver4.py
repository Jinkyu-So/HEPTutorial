import os
import re
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep


def root_latex_to_mpl(text):
    return re.sub(r"#bar\{(\w+)\}", r"$\\bar{\1}$", text)


def plot_variable(dfs, variable, bins, xlabel, luminosity, out_path):
    hep.style.use("CMS")

    mc_hists = []
    data_hist = None

    for key, (df, label, is_data) in dfs.items():
        hist_model = (f"h_{key}", "", *bins)
        df = df.Define("plot_var", variable)  #check
        if is_data:
            hist = df.Histo1D(hist_model, "plot_var").GetValue()
        else:
            df = df.Define("weight", f"{luminosity} * eventWeight")
            hist = df.Histo1D(hist_model, "plot_var", "weight").GetValue()
        hist.SetDirectory(0)

        contents = np.array([hist.GetBinContent(i + 1) for i in range(hist.GetNbinsX())])

        if is_data:
            errors = np.array([hist.GetBinError(i + 1) for i in range(hist.GetNbinsX())])
            data_hist = (contents, errors)
        else:
            mc_hists.append((contents, label))

    edges = np.linspace(bins[1], bins[2], bins[0] + 1)
    fig, ax = plt.subplots()

    max_val = 0
    if mc_hists:
        #check
        hep.histplot(
            [h[0] for h in mc_hists],
            bins=edges,
            stack=True,
            histtype="fill",
            label=[root_latex_to_mpl(h[1]) for h in mc_hists],
            edgecolor="black",
            linewidth=0.5,
            ax=ax,
        )
        max_val = max(max_val, np.sum([h[0] for h in mc_hists], axis=0).max())

    if data_hist is not None:
        contents, errors = data_hist
        centers = 0.5 * (edges[:-1] + edges[1:])
        ax.errorbar(centers, contents, yerr=errors, fmt="o", color="black", markersize=5, label="Data")
        max_val = max(max_val, contents.max())

    ax.set(xlabel=xlabel, ylabel="Events")
    ax.set_ylim(0, max_val * 1.5)
    ax.legend()

    hep.cms.label(
        "Preliminary",
        data=True,
        rlabel=f"{luminosity:.2f} " + r"$\mathrm{pb^{-1}}$" + ", 2018 (13 TeV)",
        ax=ax,
    )

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    import ROOT
    from plot_control import applycuts_semileptonic, define_objects, samples_config_semileptonic

    data_dir = os.path.join(os.path.dirname(__file__), "data")
    mc_dir = os.path.join(os.path.dirname(__file__), "mc")
    plot_dir = os.path.join(os.path.dirname(__file__), "plotting", "plots")
    selection = "s2"

    dfs = {}
    for name, (filename, label, _, is_data, _) in samples_config_semileptonic.items():
        file_path = os.path.join(data_dir if is_data else mc_dir, filename)
        df = ROOT.RDataFrame("Events", file_path)
        df = df.Define("Muon_pt_Roc", "Muon_pt")
        df = df.Define("Jet_pt_JEC", "Jet_pt")
        df = df.Define("Jet_mass_JEC", "Jet_mass")
        df = define_objects(df, "Events")
        df = applycuts_semileptonic(df, selection)
        dfs[name] = (df, label, is_data)

    luminosity = samples_config_semileptonic["Data"][4]

    variables = [
        ("GoodMuon_pt", "GoodMuon_pt", (20, 0, 100), r"Muon $p_T$ [GeV]"),
        ("GoodJet_pt", "GoodJet_pt", (30, 0, 300), r"Jet $p_T$ [GeV]"),
    ]

    for out_name_base, variable, bins, xlabel in variables:
        out_name = f"{out_name_base}_{selection}.pdf"
        out_path = os.path.join(plot_dir, selection, out_name)
        plot_variable(dfs, variable, bins, xlabel, luminosity, out_path)