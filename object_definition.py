
def define_objects(df, tree_name):

    ##### muons are defined using Rochester-corrected pt #####
    df = df.Define("GoodMuon_Mask",
        "Muon_pt_Roc > 30 && abs(Muon_eta) < 2.4 && Muon_tightId == 1 && Muon_pfIsoId >= 4")
    df = df.Define("nGoodMuon", "Sum(GoodMuon_Mask)")
    df = df.Define("GoodMuon_pt",  "Muon_pt_Roc[GoodMuon_Mask]")
    df = df.Define("GoodMuon_eta", "Muon_eta[GoodMuon_Mask]")
    df = df.Define("GoodMuon_phi", "Muon_phi[GoodMuon_Mask]")
    df = df.Define("GoodMuon_iso", "Muon_pfIsoId[GoodMuon_Mask]")
    df = df.Define("GoodMuon_mass", "Muon_mass[GoodMuon_Mask]")
    df = df.Define("GoodMuon_charge", "Muon_charge[GoodMuon_Mask]")

    df = df.Define("LooseMuon_Mask",
        "Muon_pt_Roc > 10 && abs(Muon_eta) < 2.4 && Muon_looseId == 1 && Muon_pfIsoId >= 2")
    df = df.Define("ExtraLooseMuon_Mask", "LooseMuon_Mask && !GoodMuon_Mask")
    df = df.Define("nExtraLooseMuon", "Sum(ExtraLooseMuon_Mask)")

    df = df.Define("GoodJet_Mask",
        "Jet_pt_JEC > 30 && abs(Jet_eta) < 2.4 && Jet_jetId == 6 && (Jet_pt_JEC >= 50 || Jet_puId >= 4)")
    df = df.Define("GoodJet_pt", "Jet_pt_JEC[GoodJet_Mask]")
    df = df.Define("GoodJet_eta", "Jet_eta[GoodJet_Mask]")
    df = df.Define("nGoodJet", "Sum(GoodJet_Mask)")
    df = df.Define("GoodJet_phi", "Jet_phi[GoodJet_Mask]")
    df = df.Define("GoodJet_btag", "Jet_btagDeepFlavB[GoodJet_Mask]")
    df = df.Define("GoodJet_mass", "Jet_mass_JEC[GoodJet_Mask]")

    df = df.Define("LooseElectron_Mask",
        "Electron_pt > 15 && Electron_cutBased >= 2") # check pt, eta and iso
    df = df.Define("nLooseElectron", "Sum(LooseElectron_Mask)")
    df = df.Define("LooseElectron_pt", "Electron_pt[LooseElectron_Mask]")
    df = df.Define("LooseElectron_eta", "Electron_eta[LooseElectron_Mask]")
    df = df.Define("LooseElectron_phi", "Electron_phi[LooseElectron_Mask]")
    df = df.Define("LooseElectron_iso", "Electron_pfRelIso03_all[LooseElectron_Mask]")
    df = df.Define("LooseElectron_mass", "Electron_mass[LooseElectron_Mask]")
    df = df.Define("LooseElectron_charge", "Electron_charge[LooseElectron_Mask]")

    df = df.Define("loose_bJet_Mask",
                "Jet_pt_JEC > 30 && abs(Jet_eta) < 2.4 && Jet_jetId == 6 && (Jet_pt_JEC >= 50 || Jet_puId >= 4) && Jet_btagDeepFlavB >= 0.0490")
    df = df.Define("loose_nbJet", "Sum(loose_bJet_Mask)")
    df = df.Define("loose_bJet_pt", "Jet_pt_JEC[loose_bJet_Mask]")
    df = df.Define("loose_bJet_eta", "Jet_eta[loose_bJet_Mask]")
    df = df.Define("loose_bJet_phi", "Jet_phi[loose_bJet_Mask]")

    df = df.Define("medium_bJet_Mask",
                "Jet_pt_JEC > 30 && abs(Jet_eta) < 2.4 && Jet_jetId == 6 && (Jet_pt_JEC >= 50 || Jet_puId >= 4) && Jet_btagDeepFlavB >= 0.2783")
    df = df.Define("medium_nbJet", "Sum(medium_bJet_Mask)")
    df = df.Define("medium_bJet_pt", "Jet_pt_JEC[medium_bJet_Mask]")
    df = df.Define("medium_bJet_eta", "Jet_eta[medium_bJet_Mask]")
    df = df.Define("medium_bJet_phi", "Jet_phi[medium_bJet_Mask]")

    df = df.Define("tight_bJet_Mask",
                "Jet_pt_JEC > 30 && abs(Jet_eta) < 2.4 && Jet_jetId == 6 && (Jet_pt_JEC >= 50 || Jet_puId >= 4) && Jet_btagDeepFlavB >= 0.7100")
    df = df.Define("tight_nbJet", "Sum(tight_bJet_Mask)")
    df = df.Define("tight_bJet_pt", "Jet_pt_JEC[tight_bJet_Mask]")
    df = df.Define("tight_bJet_eta", "Jet_eta[tight_bJet_Mask]")
    df = df.Define("tight_bJet_phi", "Jet_phi[tight_bJet_Mask]")

    return df
