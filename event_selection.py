
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
