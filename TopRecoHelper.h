
#ifndef TOP_RECO_HELPER_H
#define TOP_RECO_HELPER_H

#include <cmath>
#include <algorithm>
#include <limits>
#include "ROOT/RVec.hxx"
#include "Math/Vector4D.h"

namespace TopReco {

using RVecF = ROOT::VecOps::RVec<float>;
using P4 = ROOT::Math::PxPyPzEVector;

inline P4 MakeP4(float pt, float eta, float phi, float mass) {
    ROOT::Math::PtEtaPhiMVector v(pt, eta, phi, mass);
    return P4(v.Px(), v.Py(), v.Pz(), v.E());
}

inline float Wmt(
    const RVecF& mu_pt,
    const RVecF& mu_phi,
    float met_pt,
    float met_phi
) {
    if (mu_pt.size() < 1) return -999.f;

    float dphi = ROOT::VecOps::DeltaPhi(mu_phi[0], met_phi);
    float mt2 = 2.f * mu_pt[0] * met_pt * (1.f - std::cos(dphi));

    return std::sqrt(std::max(0.f, mt2));
}

inline double NeutrinoPzFromW(
    const P4& lep,
    float met_pt,
    float met_phi
) {
    const double mW = 80.379; // GeV

    double pxnu = met_pt * std::cos(met_phi);
    double pynu = met_pt * std::sin(met_phi);

    double pxl = lep.Px();
    double pyl = lep.Py();
    double pzl = lep.Pz();
    double El  = lep.E();

    double met2 = pxnu * pxnu + pynu * pynu;

    double lambda =
        0.5 * (mW * mW - lep.M2()) + pxl * pxnu + pyl * pynu;

    double a = El * El - pzl * pzl;

    if (std::abs(a) < 1e-9) return 0.0;

    double discriminant = lambda * lambda - a * met2;

    double pznu;

    if (discriminant >= 0.0) {
        double sqrt_disc = std::sqrt(discriminant);

        double pz1 = (lambda * pzl + El * sqrt_disc) / a;
        double pz2 = (lambda * pzl - El * sqrt_disc) / a;

        pznu = std::abs(pz1) < std::abs(pz2) ? pz1 : pz2;
    } else {
        pznu = lambda * pzl / a;
    }

    return pznu;
}

inline P4 NeutrinoP4FromW(
    const P4& lep,
    float met_pt,
    float met_phi
) {
    double pxnu = met_pt * std::cos(met_phi);
    double pynu = met_pt * std::sin(met_phi);
    double pznu = NeutrinoPzFromW(lep, met_pt, met_phi);

    double Enu = std::sqrt(pxnu * pxnu + pynu * pynu + pznu * pznu);

    return P4(pxnu, pynu, pznu, Enu);
}

inline int BestBtagJetIndex(
    const RVecF& jet_pt,
    const RVecF& jet_btag
) {
    if (jet_pt.size() < 1) return -1;

    if (jet_btag.size() != jet_pt.size()) return 0;

    int best = 0;
    float best_score = jet_btag[0];

    for (size_t i = 1; i < jet_btag.size(); i++) {
        if (jet_btag[i] > best_score) {
            best_score = jet_btag[i];
            best = i;
        }
    }

    return best;
}

inline float NeutrinoPz(
    const RVecF& mu_pt,
    const RVecF& mu_eta,
    const RVecF& mu_phi,
    const RVecF& mu_mass,
    float met_pt,
    float met_phi
) {
    if (mu_pt.size() < 1) return -999.f;

    P4 lep = MakeP4(mu_pt[0], mu_eta[0], mu_phi[0], mu_mass[0]);

    return static_cast<float>(NeutrinoPzFromW(lep, met_pt, met_phi));
}

inline float LeptonicTopMass(
    const RVecF& mu_pt,
    const RVecF& mu_eta,
    const RVecF& mu_phi,
    const RVecF& mu_mass,

    const RVecF& jet_pt,
    const RVecF& jet_eta,
    const RVecF& jet_phi,
    const RVecF& jet_mass,
    const RVecF& jet_btag,

    float met_pt,
    float met_phi
) {
    if (mu_pt.size() < 1) return -999.f;
    if (jet_pt.size() < 1) return -999.f;

    int ib = BestBtagJetIndex(jet_pt, jet_btag);
    if (ib < 0) return -999.f;

    P4 lep  = MakeP4(mu_pt[0], mu_eta[0], mu_phi[0], mu_mass[0]);
    P4 nu   = NeutrinoP4FromW(lep, met_pt, met_phi);
    P4 bjet = MakeP4(jet_pt[ib], jet_eta[ib], jet_phi[ib], jet_mass[ib]);

    return static_cast<float>((lep + nu + bjet).M());
}

inline float LeptonicTopMassLeadingJet(
    const RVecF& mu_pt,
    const RVecF& mu_eta,
    const RVecF& mu_phi,
    const RVecF& mu_mass,

    const RVecF& jet_pt,
    const RVecF& jet_eta,
    const RVecF& jet_phi,
    const RVecF& jet_mass,

    float met_pt,
    float met_phi
) {
    if (mu_pt.size() < 1) return -999.f;
    if (jet_pt.size() < 1) return -999.f;

    P4 lep  = MakeP4(mu_pt[0], mu_eta[0], mu_phi[0], mu_mass[0]);
    P4 nu   = NeutrinoP4FromW(lep, met_pt, met_phi);
    P4 jet  = MakeP4(jet_pt[0], jet_eta[0], jet_phi[0], jet_mass[0]);

    return static_cast<float>((lep + nu + jet).M());
}

struct HadronicRecoIndices {
    int lepB = -1;
    int wj1  = -1;
    int wj2  = -1;
    int hadB = -1;
};

inline HadronicRecoIndices PickHadronicTopIndices(
    const RVecF& jet_pt,
    const RVecF& jet_eta,
    const RVecF& jet_phi,
    const RVecF& jet_mass,
    const RVecF& jet_btag,
    float light_btag_max = 0.2783f
) {
    HadronicRecoIndices idx;

    const size_t n = jet_pt.size();

    if (
        n < 4 ||
        jet_eta.size()  != n ||
        jet_phi.size()  != n ||
        jet_mass.size() != n
    ) {
        return idx;
    }

    const bool has_btag = jet_btag.size() == n;
    const double mW = 80.379;

    idx.lepB = BestBtagJetIndex(jet_pt, jet_btag);
    if (idx.lepB < 0) return idx;

    auto chooseWPair = [&](bool require_light_btag) -> bool {
        double best_diff = std::numeric_limits<double>::max();
        int best_i = -1;
        int best_j = -1;

        for (size_t i = 0; i < n; i++) {
            if ((int)i == idx.lepB) continue;

            if (
                require_light_btag &&
                has_btag &&
                jet_btag[i] >= light_btag_max
            ) {
                continue;
            }

            for (size_t j = i + 1; j < n; j++) {
                if ((int)j == idx.lepB) continue;

                if (
                    require_light_btag &&
                    has_btag &&
                    jet_btag[j] >= light_btag_max
                ) {
                    continue;
                }

                P4 ji = MakeP4(jet_pt[i], jet_eta[i], jet_phi[i], jet_mass[i]);
                P4 jj = MakeP4(jet_pt[j], jet_eta[j], jet_phi[j], jet_mass[j]);

                double mjj = (ji + jj).M();
                double diff = std::abs(mjj - mW);

                if (diff < best_diff) {
                    best_diff = diff;
                    best_i = static_cast<int>(i);
                    best_j = static_cast<int>(j);
                }
            }
        }

        if (best_i < 0 || best_j < 0) return false;

        idx.wj1 = best_i;
        idx.wj2 = best_j;
        return true;
    };

    bool found_w_pair = false;

    if (has_btag) {
        found_w_pair = chooseWPair(true);
    }

    if (!found_w_pair) {
        found_w_pair = chooseWPair(false);
    }

    if (!found_w_pair) return idx;

    int best_hadB = -1;

    if (has_btag) {
        float best_score = -1e9;

        for (size_t i = 0; i < n; i++) {
            if ((int)i == idx.lepB) continue;
            if ((int)i == idx.wj1)  continue;
            if ((int)i == idx.wj2)  continue;

            if (jet_btag[i] > best_score) {
                best_score = jet_btag[i];
                best_hadB = static_cast<int>(i);
            }
        }
    } else {
        float best_pt = -1.f;

        for (size_t i = 0; i < n; i++) {
            if ((int)i == idx.lepB) continue;
            if ((int)i == idx.wj1)  continue;
            if ((int)i == idx.wj2)  continue;

            if (jet_pt[i] > best_pt) {
                best_pt = jet_pt[i];
                best_hadB = static_cast<int>(i);
            }
        }
    }

    idx.hadB = best_hadB;

    return idx;
}

inline float HadronicWMass(
    const RVecF& jet_pt,
    const RVecF& jet_eta,
    const RVecF& jet_phi,
    const RVecF& jet_mass,
    const RVecF& jet_btag,
    float light_btag_max = 0.2783f
) {
    HadronicRecoIndices idx = PickHadronicTopIndices(
        jet_pt,
        jet_eta,
        jet_phi,
        jet_mass,
        jet_btag,
        light_btag_max
    );

    if (idx.wj1 < 0 || idx.wj2 < 0) return -999.f;

    P4 j1 = MakeP4(jet_pt[idx.wj1], jet_eta[idx.wj1], jet_phi[idx.wj1], jet_mass[idx.wj1]);
    P4 j2 = MakeP4(jet_pt[idx.wj2], jet_eta[idx.wj2], jet_phi[idx.wj2], jet_mass[idx.wj2]);

    return static_cast<float>((j1 + j2).M());
}

inline float HadronicTopMass(
    const RVecF& jet_pt,
    const RVecF& jet_eta,
    const RVecF& jet_phi,
    const RVecF& jet_mass,
    const RVecF& jet_btag,
    float light_btag_max = 0.2783f
) {
    HadronicRecoIndices idx = PickHadronicTopIndices(
        jet_pt,
        jet_eta,
        jet_phi,
        jet_mass,
        jet_btag,
        light_btag_max
    );

    if (idx.wj1 < 0 || idx.wj2 < 0 || idx.hadB < 0) return -999.f;

    P4 j1 = MakeP4(jet_pt[idx.wj1], jet_eta[idx.wj1], jet_phi[idx.wj1], jet_mass[idx.wj1]);
    P4 j2 = MakeP4(jet_pt[idx.wj2], jet_eta[idx.wj2], jet_phi[idx.wj2], jet_mass[idx.wj2]);
    P4 b  = MakeP4(jet_pt[idx.hadB], jet_eta[idx.hadB], jet_phi[idx.hadB], jet_mass[idx.hadB]);

    return static_cast<float>((b + j1 + j2).M());
}

} // namespace TopReco

#endif
