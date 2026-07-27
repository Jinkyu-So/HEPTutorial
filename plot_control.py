import ROOT
ROOT.gInterpreter.Declare('#include "TopRecoHelper.h"')
####################################################################################

def get_objects():
    return{

############################    Muons   ################################

        "nmuons": {
            "variable": "nGoodMuon",
            "title": "Number of Muons",
            "bins": [5, 0.0, 5.0],
            "xlabel": "Number of Muons"
        },

        "nextra_loose_muons": {
            "variable": "nExtraLooseMuon",
            "title": "Number of Extra Loose Muons",
            "bins": [5, 0.0, 5.0],
            "xlabel": "Number of Extra Loose Muons"
        },

        "leading_muon_pt": {
            "variable": "GoodMuon_pt[0]",
            "title": "Leading Muon p_{T}",
            "bins": [20, 0, 100],
            "xlabel": "p_{T} (GeV)"
        },

        "leading_muon_pt_thinbins": {
            "variable": "GoodMuon_pt[0]",
            "title": "Leading Muon p_{T}",
            "bins": [50, 0, 100],
            "xlabel": "p_{T} (GeV)"
        },

        "leading_muon_eta": {
            "variable": "GoodMuon_eta[0]",
            "title": "Leading Muon eta",
            "bins": [20, -2.5, 2.5],
            "xlabel": "#eta"
        },

        "leading_muon_phi": {
            "variable": "GoodMuon_phi[0]",
            "title": "Leading Muon phi",
            "bins": [20, -3.14, 3.14],
            "xlabel": "#phi"
        },

        "subleading_muon_pt": {
            "variable": "nGoodMuon >= 2 ? GoodMuon_pt[1] : -1",
            "title": "Subleading Muon p_{T}",
            "bins": [20, 0, 100],
            "xlabel": "p_{T} (GeV)"
        },

        "subleading_muon_eta": {
            "variable": "nGoodMuon >= 2 ?GoodMuon_eta[1] : -1",
            "title": "Subleading Muon eta",
            "bins": [20, -2.5, 2.5],
            "xlabel": "#eta"
        },

        "subleading_muon_phi": {
            "variable": "nGoodMuon >= 2 ? GoodMuon_phi[1] : -1",
            "title": "Subleading Muon phi",
            "bins": [20, -3.14, 3.14],
            "xlabel": "#phi"
        },

        "leading_muon_isoID": {
            "variable": "GoodMuon_iso[0]",
            "title": "Leading Muon Isolation ID",
            "bins": [8, 0, 8],
            "xlabel": "Isolation ID"
        },

        "leading_muon_mvaTTH": {
            "variable": "Muon_mvaTTH[GoodMuon_Mask][0]",
            "title": "Leading Muon MVA TTH Score",
            "bins": [20, -1, 1],
            "xlabel": "MVA TTH Score"
        },


############################    Jets   ################################

        "njets": {
            "variable": "nGoodJet",
            "title": "Number of Jets",
            "bins": [10, 0.0, 10.0],
            "xlabel": "Number of Jets"
        },

        "leading_jet_pt": {
            "variable": "nGoodJet >= 1 ? GoodJet_pt[0] : -999",
            "title": "Leading Jet p_{T}",
            "bins": [30, 0, 300],
            "xlabel": "p_{T} (GeV)"
        },

        "leading_jet_eta": {
            "variable": "nGoodJet >= 1 ? GoodJet_eta[0] : -999",
            "title": "Leading Jet eta",
            "bins": [20, -2.5, 2.5],
            "xlabel": "#eta"
        },

        "leading_jet_phi": {
            "variable": "nGoodJet >= 1 ? GoodJet_phi[0] : -999",
            "title": "Leading Jet phi",
            "bins": [20, -3.14, 3.14],
            "xlabel": "#phi"
        },

        "leading_jet_btag": {
            "variable": "nGoodJet >= 1 ? GoodJet_btag[0] : -999",
            "title": "Leading Jet b-tag score",
            "bins": [20, 0, 1],
            "xlabel": "b-tag score"
        },

        "subleading_jet_pt": {
            "variable": "nGoodJet >= 2 ? GoodJet_pt[1] : -999",
            "title": "Subleading Jet p_{T}",
            "bins": [30, 0, 300],
            "xlabel": "p_{T} (GeV)"
        },

        "subleading_jet_eta": {
            "variable": "nGoodJet >= 2 ? GoodJet_eta[1] : -999",
            "title": "Subleading Jet eta",
            "bins": [20, -2.5, 2.5],
            "xlabel": "#eta"
        },

        "subleading_jet_phi": {
            "variable": "nGoodJet >= 2 ? GoodJet_phi[1] : -999",
            "title": "Subleading Jet phi",
            "bins": [20, -3.14, 3.14],
            "xlabel": "#phi"
        },

        "subleading_jet_btag": {
            "variable": "nGoodJet >= 2 ? GoodJet_btag[1] : -999",
            "title": "Subleading Jet b-tag score",
            "bins": [20, 0, 1],
            "xlabel": "b-tag score"
        },

#########################   B-jets   ################################

        "loose_nbjets": {
            "variable": "loose_nbJet",
            "title": "Number of b-jets",
            "bins": [5, 0.0, 5.0],
            "xlabel": "Number of b-jets"
        },

        "medium_nbjets": {
            "variable": "medium_nbJet",
            "title": "Number of b-jets",
            "bins": [5, 0.0, 5.0],
            "xlabel": "Number of b-jets"
        },

        "tight_nbjets": {
            "variable": "tight_nbJet",
            "title": "Number of b-jets",
            "bins": [5, 0.0, 5.0],
            "xlabel": "Number of b-jets"
        },

        "leading_tight_bjet_pt": {
            "variable": "tight_nbJet >= 1 ? tight_bJet_pt[0] : -999",
            "title": "Leading Tight b-jet p_{T}",
            "bins": [30, 0, 300],
            "xlabel": "p_{T} (GeV)"
        },

#########################   MET   ################################

        "MET": {
            "variable": "MET_pt",
            "title": "Missing E_{T}",
            "bins": [40, 0, 200],
            "xlabel": "MET (GeV)"
        },

        "MET_phi": {
            "variable": "MET_phi",
            "title": "Missing E_{T} phi",
            "bins": [20, -3.14, 3.14],
            "xlabel": "MET phi"
        },

#########################   Global Objects   ################################

        "nPV": {
            "variable": "PV_npvs",
            "title": "Number of Primary Vertices",
            "bins": [80, 0, 80],
            "xlabel": "Number of Primary Vertices"
        },

        "HT": {
            "variable": "nGoodJet >= 1 ? Sum(GoodJet_pt) : -999",
            "title": "Scalar Sum of Jet p_{T}",
            "bins": [50, 0, 1000],
            "xlabel": "H_{T} (GeV)"
        },

        "ST": {
            "variable": "(nGoodJet > 0 ? Sum(GoodJet_pt) : 0.0) + MET_pt + Sum(GoodMuon_pt)",
            "title": "Scalar Sum of Jet p_{T}, MET and Muon p_{T}",
            "bins": [50, 0, 1000],
            "xlabel": "S_{T} (GeV)"
        },


#########################   Reconstructed Objects   ##################################


        "dimuon_mass": {
            "variable": "nGoodMuon >= 2 ? ROOT::VecOps::InvariantMass(GoodMuon_pt, GoodMuon_eta, GoodMuon_phi, GoodMuon_mass) : -999",
            "title": "Dimuon Invariant Mass",
            "bins": [20, 70, 120],
            "xlabel": "m_{#mu#mu} (GeV)"
        },

        "dimuon_mass_thinbins": {
            "variable": "nGoodMuon >= 2 ? ROOT::VecOps::InvariantMass(GoodMuon_pt, GoodMuon_eta, GoodMuon_phi, GoodMuon_mass) : -999",
            "title": "Dimuon Invariant Mass",
            "bins": [50, 70, 120],
            "xlabel": "m_{#mu#mu} (GeV)"
        },

        "lepW_mt": {
            "variable": "TopReco::Wmt(GoodMuon_pt, GoodMuon_phi, MET_pt, MET_phi)",
            "title": "W m_{T}",
            "bins": [20, 0, 200],
            "xlabel": "m_{T}(W) (GeV)"
        },

        "lepTop_mass": {
            "variable": "TopReco::LeptonicTopMass(GoodMuon_pt, GoodMuon_eta, GoodMuon_phi, GoodMuon_mass, GoodJet_pt, GoodJet_eta, GoodJet_phi, GoodJet_mass, GoodJet_btag, MET_pt, MET_phi)",
            "title": "Leptonic top mass",
            "bins": [20, 0, 400],
            "xlabel": "m(b#mu#nu) (GeV)"
        },

        "hadW_mass": {
            "variable": "TopReco::HadronicWMass(GoodJet_pt, GoodJet_eta, GoodJet_phi, GoodJet_mass, GoodJet_btag)",
            "title": "Hadronic W mass",
            "bins": [20, 0, 200],
            "xlabel": "m(jj) (GeV)"
        },

        "hadTop_mass": {
            "variable": "TopReco::HadronicTopMass(GoodJet_pt, GoodJet_eta, GoodJet_phi, GoodJet_mass, GoodJet_btag)",
            "title": "Hadronic top mass",
            "bins": [20, 0, 500],
            "xlabel": "m(bjj) (GeV)"
        },

    }

####################################################################################

def applycuts_semileptonic(df, selection):

    step = int(selection.replace("s",""))
    # default s0 : At least one good muon
    # s1 : extra lepton veto -> removes Drell-Yan, WZ, ZZ, dileptonic ttbar, leptonic ST, QCD-lep
    # s2 : jet multiplicity cut -> removes Wjets, QCD-had
    # s3 : bjet requirement -> removes Wjets
    # s4 : MET cut ?

    df = df.Filter("nGoodMuon >= 1")

    if step >= 1:
        df = df.Filter("nGoodMuon == 1")
        df = df.Filter("nExtraLooseMuon == 0")
        df = df.Filter("nLooseElectron == 0")

    if step >= 2:
        df = df.Filter("nGoodJet >= 4")

    if step >= 3:
        df = df.Filter("Muon_mvaTTH[GoodMuon_Mask][0] >= 0.64")

    if step >= 4:
        df = df.Filter("tight_nbJet >= 2")

    return df

####################################################################################

def applycuts_dileptonic(df, selection):

    step = int(selection.replace("s",""))
    # default s0 : At least one good muon
    # s1 : exactly two good muons with opposite sign
    # s2 : MET cut
    # s3 : jet multiplicity cut 
    # s4 : bjet requirement 

    df = df.Filter("nGoodMuon >= 2")

    if step >= 1:
        df = df.Filter("nGoodMuon == 2")
        df = df.Filter("nExtraLooseMuon == 0")
        df = df.Filter("nLooseElectron == 0")
        df = df.Filter("GoodMuon_charge[0] * GoodMuon_charge[1] < 0") 
        
    if step >= 2:
        df = df.Filter("nGoodJet >= 2")

    if step >= 3:
        df = df.Filter("medium_nbJet >= 2")

    if step >= 4:
        df = df.Filter("abs(ROOT::VecOps::InvariantMass(GoodMuon_pt, GoodMuon_eta, GoodMuon_phi, GoodMuon_mass) - 91.1876)> 15")

    return df

####################################################################################

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

    df = df.Define(
        "GoodJet_Mask",
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

####################################################################################

samples_config_semileptonic = {
    "Data":  ["run2018A_GLegacy_SingleMuon.root", "Data", ROOT.kBlack, True, 188.09],
    "TTbar": ["TTbar.root", "t#bar{t}", ROOT.kOrange-3, False, 100.0],
    "QCD":   ["QCD.root", "QCD Multi-jet", ROOT.kAzure+7, False, 100.0],
    "ST":    ["ST.root", "Single Top", ROOT.kRed-9, False, 100.0],
    "DY":    ["DY.root", "Drell-Yan", ROOT.kSpring+5, False, 100.0],
    "WJets": ["WJets.root", "W+Jets", ROOT.kGreen-3, False, 100.0],
    "WW":    ["WW.root", "WW", ROOT.kYellow-7, False, 100.0],
    "WZ":    ["WZ.root", "WZ", ROOT.kYellow-6, False, 100.0],
    "ZZ":    ["ZZ.root", "ZZ", ROOT.kYellow-5, False, 100.0],
}

####################################################################################

samples_config_dileptonic = {
    "Data":  ["run2018A_GLegacy_DiMuon_merged.root", "Data", ROOT.kBlack, True, 1987.090251629],
    "TTbar": ["TTbar.root", "t#bar{t}", ROOT.kOrange-3, False, 100.0],
    "QCD":   ["QCD.root", "QCD Multi-jet", ROOT.kAzure+7, False, 100.0],
    "ST":    ["ST.root", "Single Top", ROOT.kRed-9, False, 100.0],
    "DY":    ["DY.root", "Drell-Yan", ROOT.kSpring+5, False, 100.0],
    "WJets": ["WJets.root", "W+Jets", ROOT.kGreen-3, False, 100.0],
    "WW":    ["WW.root", "WW", ROOT.kYellow-7, False, 100.0],
    "WZ":    ["WZ.root", "WZ", ROOT.kYellow-6, False, 100.0],
    "ZZ":    ["ZZ.root", "ZZ", ROOT.kYellow-5, False, 100.0],
}
