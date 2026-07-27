import ROOT
import os 
import argparse
import cmsstyle as CMS
from plot_control import applycuts_semileptonic, samples_config_semileptonic, define_objects, get_objects

def main():
    data_dir = "/home/jso/heptutorial/data"
    mc_dir = "/home/jso/heptutorial/mc/merged_MC"
    plot_dir = "/home/jso/heptutorial/plotting/plots/"
    luminosity = 188.09

    parser = argparse.ArgumentParser(description="CMS Single Plotter")
    parser.add_argument("--object", choices=get_objects().keys(), help="Variable to plot")
    parser.add_argument("--selection", choices=["s0", "s1", "s2", "s3", "s4", "s-1"], default="s0")
    args = parser.parse_args()

    config = get_objects()[args.object]

    # --- Initialize Style ---
    CMS.setCMSStyle() 
    CMS.SetExtraText("Preliminary")
    CMS.SetLumi(luminosity, "pb", "", 1)
    ROOT.TGaxis.SetMaxDigits(3)
    ROOT.TGaxis.SetExponentOffset(-0.08, 0.01, "Y")
    ROOT.gStyle.SetLabelSize(0.04, "XYZ")
    ROOT.gStyle.SetTitleSize(0.04, "XYZ")
    ROOT.gStyle.SetLegendTextSize(0.03)
 
    mc_stack = ROOT.THStack("hs", "")
    legend = ROOT.TLegend(0.65, 0.57, 0.92, 0.89)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    
    hist_store = {"MC": [], "data": None}

    # --- Data Processing ---
    for name, info in samples_config_semileptonic.items():
        filename, label, color, is_data, lumi = info
        full_path = os.path.join(data_dir if is_data else mc_dir, filename)

        df = ROOT.RDataFrame("Events", full_path)
        df = define_objects(df, "Events")
        df = applycuts_semileptonic(df, args.selection)
        df = df.Define("plot_var", config["variable"])
        
        if is_data:
            h_temp = df.Histo1D(("data_hist", config["title"], *config["bins"]), "plot_var")
            h = h_temp.GetValue()
            h.SetDirectory(0) 
            h.Scale(luminosity / lumi)
            h.SetMarkerStyle(20)
            hist_store["data"] = h
            legend.AddEntry(h, label, "pe")

        else:
            df = df.Define("event_weight", f"{luminosity} * xsecWeight * Pileup_weight * Muon_weight * PUJetID_weight")
            h_temp = df.Histo1D(("data_hist", config["title"], *config["bins"]), "plot_var", "event_weight")
            h = h_temp.GetValue()
            h.SetDirectory(0) 
            h.SetFillColor(color)
            h.SetLineColor(ROOT.kBlack)
            mc_stack.Add(h)
            hist_store["MC"].append(h)
            legend.AddEntry(h, label, "f")


    # --- Plotting ---
    max_val = max(mc_stack.GetMaximum(), hist_store["data"].GetMaximum() if hist_store["data"] else 0) * 1.5
    
    # Use the official TCmsCanvas wrapper
    canv = CMS.cmsCanvas('canv_single', config['bins'][1], config['bins'][2], 0, max_val, 
                          config['xlabel'], 'Events', True, 0, 0, False, 1.0, 1.3)

    #canv.SetLeftMargin(0.12)
    canv.Modified()
    canv.Update()

    frame = canv.GetPrimitive("hframe")
    frame.GetXaxis().SetTitleOffset(1.2)
    frame.GetYaxis().CenterTitle()

    mc_stack.Draw("HIST SAME")
    if hist_store["data"]:
        hist_store["data"].Draw("PE SAME")
    legend.Draw()

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.035)

    latex.DrawLatex(0.40, 0.06, config["title"])


    save_path = os.path.join(plot_dir, f"{args.selection}", f"{args.object}_{args.selection}.pdf")
    target_dir = os.path.dirname(save_path)
    os.makedirs(target_dir, exist_ok=True)
    canv.SaveAs(save_path)
    print(f"Created single plot: {save_path}")

if __name__ == "__main__":
    main()