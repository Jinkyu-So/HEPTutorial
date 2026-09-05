import ROOT

############ need to replace TopRecoHelper ##############
ROOT.gInterpreter.Declare('#include "TopRecoHelper.h"')

from object_definition import define_objects
from event_selection import applycuts_semileptonic, applycuts_dileptonic

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

