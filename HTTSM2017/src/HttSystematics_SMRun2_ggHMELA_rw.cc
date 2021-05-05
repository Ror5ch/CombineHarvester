#include "CombineHarvester/HTTSM2017/interface/HttSystematics_SMRun2_ggHMELA_rw.h"
#include <vector>
#include <string>
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"

using namespace std;

namespace ch {
    
    using ch::syst::SystMap;
    using ch::syst::SystMapAsymm;
    using ch::syst::era;
    using ch::syst::channel;
    using ch::syst::bin_id;
    using ch::syst::process;
    using ch::syst::bin;
    using ch::JoinStr;
    
void AddSMRun2Systematics_ggHMELA_rw(CombineHarvester & cb, int tt_cate_count, int mt_cate_count, int control_region, bool do_shapeSyst, int year, bool mm_fit, bool ttbar_fit)
{

    if (year != 2016 && year != 2017 && year != 2018)
    {
        std::cout << "Wrong year" << std::endl;
        return;
    }         
        
    //      std::vector<std::string> sig_procs = {"ggH_htt","reweighted_qqH_htt_0PM","reweighted_WH_htt_0PM","reweighted_ZH_htt_0PM","reweighted_qqH_htt_0M","reweighted_WH_htt_0M","reweighted_ZH_htt_0M","reweighted_qqH_htt_0Mf05ph0","reweighted_ZH_htt_0Mf05ph0","reweighted_WH_htt_0Mf05ph0"};
    std::vector<std::string> sig_procs = {"GGH2Jets_sm_M","GGH2Jets_pseudoscalar_M","GGH2Jets_pseudoscalar_Mf05ph0","reweighted_qqH_htt_0PM","reweighted_WH_htt_0PM","reweighted_ZH_htt_0PM","reweighted_qqH_htt_0M","reweighted_WH_htt_0M","reweighted_ZH_htt_0M","reweighted_qqH_htt_0Mf05ph0","reweighted_ZH_htt_0Mf05ph0","reweighted_WH_htt_0Mf05ph0"};
    std::vector<std::string> sig_procs_recoil = {"GGH2Jets_sm_M","GGH2Jets_pseudoscalar_M","GGH2Jets_pseudoscalar_Mf05ph0","reweighted_qqH_htt_0PM","reweighted_qqH_htt_0M","reweighted_qqH_htt_0Mf05ph0"};
    std::vector<std::string> sig_procs_ggh = {"GGH2Jets_sm_M","GGH2Jets_pseudoscalar_M","GGH2Jets_pseudoscalar_Mf05ph0"};
    std::vector<std::string> sig_procs_vbf = {"reweighted_qqH_htt_0PM","reweighted_qqH_htt_0M","reweighted_qqH_htt_0Mf05ph0"};
    std::vector<std::string> sig_procs_wh = {"reweighted_WH_htt_0PM","reweighted_WH_htt_0M","reweighted_WH_htt_0Mf05ph0"};
    std::vector<std::string> sig_procs_zh = {"reweighted_ZH_htt_0PM","reweighted_ZH_htt_0M","reweighted_ZH_htt_0Mf05ph0"};
    //std::vector<std::string> sig_procs = {"ggH_htt","reweighted_qqH_htt_0PM","reweighted_WH_htt_0PM","reweighted_ZH_htt_0PM"};
        
    // N.B. when adding this list of backgrounds to a nuisance, only
    // the backgrounds that are included in the background process
    // defined in MorphingSM2016.cpp are included in the actual DCs
    // This is a list of all MC based backgrounds
    // QCD is explicitly excluded
    std::vector<std::string> all_mc_bkgs = {
    // "ZL","ZJ","ZTT","TTJ","TTT","TT",
    "ZL","ZJ","ZTT","TTJ","TTT","TT","ZLL",
    "W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
    "VVL","ZT","TTL",
    "ggH_hww125","qqH_hww125","EWKZ", "STT", "STL", "TTL", "VVL","HWW","ZH_hww125","WH_hww125","VH_hww125"};
    //std::vector<std::string> all_mc_bkgs_no_ZL = {
    //   "ZTT","TTT"};
    // std::vector<std::string> all_mc_bkgs_no_ZL = { "ZJ","ZTT","TTJ","TTT","TT",
    //   "W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
    //   "ggH_hww125","qqH_hww125","EWKZ"
    //    };
    std::vector<std::string> all_mc_bkgs_realTau = {
    "STT""TTT","VVT"};

    // FIXME SD Sep 30: tauideff syst is missing for et/mt hww samples, so comenting it out for now:
    std::vector<std::string> all_mc_bkgs_no_ZL = { "ZJ","ZTT","TTJ","TTT","TT","STT",
                   "W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
    "ggH_hww125","qqH_hww125","ZH_hww125","WH_hww125","VH_hww125","EWKZ","HWW"
    };
    std::vector<std::string> all_mc_bkgs_no_ZL_noHww = { "ZJ","ZTT","TTJ","TTT","TT","STT",
                                           "W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
                        "EWKZ","HWW"
    };

    std::vector<std::string> all_mc_bkgs_no_W = {
    "ZL","ZJ","ZTT","TTJ","TTT","TT",
    "ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
    "ggH_hww125","qqH_hww125","ZH_hww125","WH_hww125","VH_hww125","EWKZ","HWW"};
    std::vector<std::string> all_mc_bkgs_no_TTJ = {
    "ZL","ZJ","ZTT","TTT","TT",
    "ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ",
    "ggH_hww125","qqH_hww125","ZH_hww125","WH_hww125","VH_hww125","EWKZ","HWW"};

    std::vector<std::string> all_mc_bkgs_recoil = {"ZL", "ZLL"};

    // FIXME: use flat QCD 20% for now
    if (do_shapeSyst)
    {
      cb.cp().process({"QCD"}).channel({"em"}).AddSyst(cb, "QCD", "shape", SystMap<>::init(1.0));
    }
    else
    {
      cb.cp().process({"QCD"}).channel({"em"}).AddSyst(cb, "QCD_unc", "lnN", SystMap<>::init(1.2));
    }
    
    
    // START: lnN
    //    Uncertainty on BR for HTT @ 125 GeV
    cb.cp().process(sig_procs).AddSyst(cb,"BR_htt_THU", "lnN", SystMap<>::init(1.017));
    cb.cp().process(sig_procs).AddSyst(cb,"BR_htt_PU_mq", "lnN", SystMap<>::init(1.0099));
    cb.cp().process(sig_procs).AddSyst(cb,"BR_htt_PU_alphas", "lnN", SystMap<>::init(1.0062));

    cb.cp().process(JoinStr({sig_procs_wh,{"WH_hww125","VH_hww125","WH_htt_nonfid125"}})).AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.008));
    cb.cp().process(JoinStr({sig_procs_zh,{"ZH_hww125","ZH_htt_nonfid125"}})).AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.009));
    //cb.cp().process(JoinStr({qqH_STXS,{"qqH_hww125"}})).AddSyst(cb, "QCDScale_qqH", "lnN", SystMap<>::init(1.005));
    cb.cp().process(JoinStr({sig_procs_wh,{"WH_hww125","VH_hww125","WH_htt_nonfid125"}})).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.018));
    cb.cp().process(JoinStr({sig_procs_zh,{"ZH_hww125","ZH_htt_nonfid125"}})).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.013));
    cb.cp().process(JoinStr({sig_procs_ggh,{"ggH_hww125","ggH_htt_nonfid125"}})).AddSyst(cb, "pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));
    // cb.cp().process(JoinStr({sig_procs_ggh,{"qqH_hww125","qqH_htt_nonfid125"}})).AddSyst(cb, "pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));
    cb.cp().process(JoinStr({sig_procs_vbf,{"qqH_hww125","qqH_htt_nonfid125"}})).AddSyst(cb, "pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));

    cb.cp().process({"ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125"}).AddSyst(cb, "BR_hww_PU_alphas", "lnN", ch::syst::SystMapAsymm<>::init(1.0066,1.0063));
    cb.cp().process({"ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125"}).AddSyst(cb, "BR_hww_PU_mq", "lnN", ch::syst::SystMapAsymm<>::init(1.0099,1.0098));
    cb.cp().process({"ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125"}).AddSyst(cb, "BR_hww_THU", "lnN", SystMap<>::init(1.0099));  


    //Muon ID efficiency: Decorollated in 18-032 datacards.  
    cb.cp().process(JoinStr({{"ZT","TTT","VVT","STT","ZL","TTL","VVL","STL","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).channel({"mt"}).AddSyst(cb,"CMS_eff_m_$ERA","lnN",SystMap<>::init(1.02));

    // b-tagging efficiency
    cb.cp().process({"STT","STL","TTT","TTL","TT"}).AddSyst(cb,"CMS_btag_eta","lnN",SystMap<>::init(1.005));
    cb.cp().process(JoinStr({{"W","ZLL","VV","ZT","VVT","ZL","VVL","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb,"CMS_btag_eta","lnN",SystMap<>::init(1.001));
    
    cb.cp().process({"STT","STL","TTT","TTL","TT"}).AddSyst(cb,"CMS_btag_hf","lnN",SystMap<>::init(0.993));
    cb.cp().process(JoinStr({{"W","ZLL","VV","ZT","VVT","ZL","VVL","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb,"CMS_btag_hf","lnN",SystMap<>::init(1.002));
    
    cb.cp().process({"STT","STL","TTT","TTL","TT"}).AddSyst(cb,"CMS_btag_hfstats1_$ERA","lnN",SystMap<>::init(1.03));
    //cb.cp().process(JoinStr({{"W","ZT","VVT","ZL","VVL","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb,"CMS_btag_hfstats1_$ERA","lnN",SystMap<>::init(1.0000));

    cb.cp().process({"STT","STL","TTT","TTL","TT"}).AddSyst(cb,"CMS_btag_hfstats2_$ERA","lnN",SystMap<>::init(1.015));
    //cb.cp().process(JoinStr({{"W","ZT","VVT","ZL","VVL","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb,"CMS_hfstats2_$ERA","lnN",SystMap<>::init(1.000));
    
    cb.cp().process({"STT","STL","TTT","TTL","TT"}).AddSyst(cb,"CMS_btag_jes","lnN",SystMap<>::init(0.98));
    cb.cp().process(JoinStr({{"W","ZLL","VV","ZT","VVT","ZL","VVL","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb,"CMS_btag_jes","lnN",SystMap<>::init(1.003));
    
    cb.cp().process({"STT","STL","TTT","TTL","TT"}).AddSyst(cb,"CMS_btag_lf","lnN",SystMap<>::init(0.90));
    cb.cp().process(JoinStr({{"W","ZLL","VV","ZT","VVT","ZL","VVL","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb,"CMS_btag_lf","lnN",SystMap<>::init(0.999));

    cb.cp().process({"STT","STL","TTT","TTL","TT"}).AddSyst(cb,"CMS_btag_lfstats1_$ERA","lnN",SystMap<>::init(0.995));
    cb.cp().process(JoinStr({{"W","ZLL","VV","ZT","VVT","ZL","VVL","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb,"CMS_btag_lfstats1_$ERA","lnN",SystMap<>::init(0.999));

    cb.cp().process({"STT","STL","TTT","TTL","TT"}).AddSyst(cb,"CMS_btag_lfstats2_$ERA","lnN",SystMap<>::init(0.995));
    cb.cp().process(JoinStr({{"W","ZLL","VV","ZT","VVT","ZL","VVL","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb,"CMS_btag_lfstats2_$ERA","lnN",SystMap<>::init(1.001));

    // XSection Uncertainties
    // cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_htt_tjXsec", "lnN", SystMap<>::init(1.042));
    cb.cp().process({"TTT","TTL","TT"}).AddSyst(cb,"CMS_htt_tjXsec", "lnN", SystMap<>::init(1.042));
    cb.cp().process({"VVT","VVL","VV"}).AddSyst(cb,"CMS_htt_vvXsec", "lnN", SystMap<>::init(1.05));
    cb.cp().process({"STT","STL"}).AddSyst(cb,"CMS_htt_stXsec", "lnN", SystMap<>::init(1.05));
    // cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_htt_zjXsec", "lnN", SystMap<>::init(1.02));
    cb.cp().process({"ZT","ZL","ZLL"}).AddSyst(cb,"CMS_htt_zjXsec", "lnN", SystMap<>::init(1.02));

    //Luminosity Uncertainty
    // cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_Run_$ERA", "lnN", SystMap<>::init(1.022));
    // cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_XYfactorization", "lnN", SystMap<>::init(1.009));
    // cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_beamBeamDeflection", "lnN", SystMap<>::init(1.004));
    // cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_dynamicBeta", "lnN", SystMap<>::init(1.005));
    // cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_ghostsAndSatellites", "lnN", SystMap<>::init(1.004));
    
    // cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_Run_$ERA", "lnN", SystMap<>::init(1.022));
    // cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_XYfactorization", "lnN", SystMap<>::init(1.009));
    // cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_beamBeamDeflection", "lnN", SystMap<>::init(1.004));
    // cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_dynamicBeta", "lnN", SystMap<>::init(1.005));
    // cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_ghostsAndSatellites", "lnN", SystMap<>::init(1.004));
    
    if (year == 2016)
    {
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_$ERA", "lnN", SystMap<>::init(1.022));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_XY", "lnN", SystMap<>::init(1.009));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_BBD", "lnN", SystMap<>::init(1.004));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_DB", "lnN", SystMap<>::init(1.005));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_GS", "lnN", SystMap<>::init(1.004));
    }
    else if (year == 2017)
    {
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_$ERA", "lnN", SystMap<>::init(1.02));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_XY", "lnN", SystMap<>::init(1.008));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_LS", "lnN", SystMap<>::init(1.003));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_BBD", "lnN", SystMap<>::init(1.004));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_DB", "lnN", SystMap<>::init(1.005));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_BCC", "lnN", SystMap<>::init(1.003));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_GS", "lnN", SystMap<>::init(1.001));
    }
    else
    {
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_$ERA", "lnN", SystMap<>::init(1.015));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_XY", "lnN", SystMap<>::init(1.02));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_LS", "lnN", SystMap<>::init(1.002));
        cb.cp().process(JoinStr({sig_procs,{"W","ZLL","TT","VV","VVL","VVT","STT","STL","ZL","ZLL","ZT","TTL","TTT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb, "lumi_13TeV_BCC", "lnN", SystMap<>::init(1.002));
    }

    cb.cp().process({"jetFakes"}).bin_id({1}).AddSyst(cb,"CMS_jetFakesNorm_0jet_$CHANNEL_$ERA","lnN",SystMap<>::init(1.05));

    //Electron ID efficiency
    cb.cp().process(JoinStr({{"ZT","TTT","VVT","STT","ZL","TTL","VVL","STL","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).channel({"et"}).AddSyst(cb,"CMS_eff_e_$ERA","lnN",SystMap<>::init(1.02));

    // Against ele and against mu for real taus
    // cb.cp().process(JoinStr({{"ZT","TTT","VVT","STT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).AddSyst(cb,"CMS_eff_t_againstemu_$CHANNEL_$ERA","lnN",SystMap<>::init(1.03));

    // Trg efficiency. Can be a single lnN because only single ele trigger
    // cb.cp().process(JoinStr({{"ZT","TTT","VVT","STT","ZL","TTL","VVL","STL","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).channel({"et"}).AddSyst(cb,"CMS_singleeletrg_$ERA","lnN",SystMap<>::init(1.02));

    // END: lnN
    
        
        
        


    if (do_shapeSyst)
    {
        //##############################################################################
        // Tau ID
        //##############################################################################
        //        // FIXME SD Sep 30: tauideff syst is missing for et/mt hww samples, so comenting it out for now:
        //
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_ZL_noHww})).channel({"et","mt"}).AddSyst(cb, "CMS_tauideff_pt30to35_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_ZL_noHww})).channel({"et","mt"}).AddSyst(cb, "CMS_tauideff_pt35to40_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_ZL_noHww})).channel({"et","mt"}).AddSyst(cb, "CMS_tauideff_ptgt40_$ERA", "shape", SystMap<>::init(1.00));

        //##############################################################################
        // Trigger 
        //##############################################################################
        // Trg efficiency. Can be a single lnN because only single ele trigger
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et"}).AddSyst(cb,"CMS_singleeletrg_$ERA","lnN",SystMap<>::init(1.02));


        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt"}).AddSyst(cb,"CMS_singlemutrg_$ERA","shape",SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt"}).AddSyst(cb,"CMS_mutautrg_$ERA","shape",SystMap<>::init(1.00));

        // Trg efficiency. Can be a single lnN because only single ele trigger (Fixed: mt removed)
        cb.cp().process({"embedded"}).channel({"et"}).AddSyst(cb,"CMS_singleeletrg_embedded_$ERA","lnN",SystMap<>::init(1.02));
        // cb.cp().process({"embedded"}).channel({"et"}).AddSyst(cb,"CMS_singleeletrg_$ERA","lnN",SystMap<>::init(1.01));


        //##############################################################################
        // CMS_prefiring NOT FOR 2018!
        //##############################################################################
        if (year != 2018){
            std::cout << "CMS_prefiring" << std::endl;
            cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","em"}).AddSyst(cb, "CMS_prefiring", "shape", SystMap<>::init(1.00));
        }
        //##############################################################################
        // τh energy scale 
        //##############################################################################
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt"}).AddSyst(cb,
                                                  "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt"}).AddSyst(cb,
                                                  "CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"tt"}).AddSyst(cb,
                                                  "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(1.00));
        // SD FIXME: missing 1prong for all except ZTT and TTT:
            
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_realTau})).channel({"et","mt"}).AddSyst(cb,
                                                      "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_realTau})).channel({"et","mt"}).AddSyst(cb,
                                                      "CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_realTau})).channel({"et","mt"}).AddSyst(cb,
                                                      "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_realTau})).channel({"et","mt"}).AddSyst(cb,
                                                      "CMS_scale_t_3prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
    
    // SD 8 Jan
    /*
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt"}).AddSyst(cb,
                                                  "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt"}).AddSyst(cb,
                                                  "CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt"}).AddSyst(cb,
                                                  "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt"}).AddSyst(cb,
                                                  "CMS_scale_t_3prong1pizero_$ERA", "shape", SystMap<>::init(1.00));

        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_ZL})).channel({"et"}).AddSyst(cb,
                                                  "CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_ZL})).channel({"et"}).AddSyst(cb,
                                                  "CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_ZL})).channel({"et"}).AddSyst(cb,
                                                  "CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs_no_ZL})).channel({"et"}).AddSyst(cb,
                                                  "CMS_scale_t_3prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
    */

        //##############################################################################
        // e→τh energy scale 
        //##############################################################################
        
        // FIXME: Tyler need to fix those so comment out for now
          
    cb.cp().process({"W","ZL","TTL","VVL","STL"}).channel({"et"}).AddSyst(cb,
                                                  "CMS_scale_efaket_1prong_barrel_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"W","ZL","TTL","VVL","STL"}).channel({"et"}).AddSyst(cb,
                                                  "CMS_scale_efaket_1prong1pizero_barrel_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"W","ZL","TTL","VVL","STL"}).channel({"et"}).AddSyst(cb,
                                                  "CMS_scale_efaket_1prong_endcap_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"W","ZL","TTL","VVL","STL"}).channel({"et"}).AddSyst(cb,
                                                  "CMS_scale_efaket_1prong1pizero_endcap_$ERA", "shape", SystMap<>::init(1.00));
    

     // FIXME April: missing in Tyler's et datacards!
    cb.cp().process({"W","ZL","TTL","VVL","STL"}).channel({"et"}).AddSyst(cb,
                                                  "CMS_efaket_norm_pt30to40_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"W","ZL","TTL","VVL","STL"}).channel({"et"}).AddSyst(cb,
                                                  "CMS_efaket_norm_pt40to50_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"W","ZL","TTL","VVL","STL"}).channel({"et"}).AddSyst(cb,
                                                  "CMS_efaket_norm_ptgt50_$ERA", "shape", SystMap<>::init(1.00));
    
    
        //##############################################################################
        // μ → τh energy scale THIS ONE IS NOT IN ANDREW's syst list -> check why
        //##############################################################################
    // FIXME: is 0 in all Tyler's files: SD 8 Jun
    

    cb.cp().process({"W","ZL","TTL","VVL","STL"}).channel({"mt"}).AddSyst(cb,
                                                  "CMS_scale_mfaket_1prong_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"W","ZL","TTL","VVL","STL"}).channel({"mt"}).AddSyst(cb,
                                                  "CMS_scale_mfaket_1prong1pizero_$ERA", "shape", SystMap<>::init(1.00));
                         
    cb.cp().process({"W","ZL","TTL","VVL","STL"}).channel({"mt"}).AddSyst(cb,
                                                  "CMS_mfaket_norm_pt30to40_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"W","ZL","TTL","VVL","STL"}).channel({"mt"}).AddSyst(cb,
                                                  "CMS_mfaket_norm_pt40to50_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"W","ZL","TTL","VVL","STL"}).channel({"mt"}).AddSyst(cb,
                                                  "CMS_mfaket_norm_ptgt50_$ERA", "shape", SystMap<>::init(1.00));

        //##############################################################################
        // Electron energy scale
        //##############################################################################
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et"}).AddSyst(cb,
                                           "CMS_scale_e", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_scale_e", "shape", SystMap<>::init(1.00));
      
        cb.cp().process({"embedded"}).channel({"et"}).AddSyst(cb,
                                           "CMS_scale_emb_e", "shape", SystMap<>::init(1.00));
        cb.cp().process({"embedded"}).channel({"em"}).AddSyst(cb, "CMS_scale_emb_e", "shape", SystMap<>::init(1.00));

        //##############################################################################
        // Muon energy scale
        //##############################################################################
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs, {"QCD"}})).channel({"mt"}).AddSyst(cb,
                                                "CMS_scale_m_etalt1p2", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs, {"QCD"}})).channel({"mt"}).AddSyst(cb,
                                                "CMS_scale_m_eta1p2to2p1", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs, {"QCD"}})).channel({"mt"}).AddSyst(cb,
                                                "CMS_scale_m_eta2p1to2p4", "shape", SystMap<>::init(1.00));

        cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,
                                                "CMS_scale_m_etalt1p2", "shape", SystMap<>::init(0.50));
        cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,
                                                "CMS_scale_m_eta1p2to2p1", "shape", SystMap<>::init(0.50));
        cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,
                                                "CMS_scale_m_eta2p1to2p4", "shape", SystMap<>::init(0.50));

        cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,
                                                "CMS_scale_emb_m_etalt1p2", "shape", SystMap<>::init(0.866));
        cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,
                                                "CMS_scale_emb_m_eta1p2to2p1", "shape", SystMap<>::init(0.866));
        cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,
                                                "CMS_scale_emb_m_eta2p1to2p4", "shape", SystMap<>::init(0.866));

        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb,
                                               "muES", "shape", SystMap<>::init(1.00));

        cb.cp().process({"embedded"}).channel({"em"}).AddSyst(cb,
                                               "muES", "shape", SystMap<>::init(0.50));

        cb.cp().process({"embedded"}).channel({"em"}).AddSyst(cb,
                                               "muES_emb", "shape", SystMap<>::init(0.866));
        //##############################################################################
        // Jet energy scale 
        //##############################################################################
        //
        // uncomment below once JET fixed at FSA level!
    
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,"CMS_scale_j_Absolute_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,"CMS_scale_j_Absolute", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,"CMS_scale_j_BBEC1_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,"CMS_scale_j_BBEC1", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,"CMS_scale_j_HF_$ERA", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,"CMS_scale_j_HF", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,"CMS_scale_j_EC2_$ERA", "shape", SystMap<>::init(1.00));
    if (year != 2017)
    { // FIXME: excluded for 2017 because bogus norm Down 0!
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,"CMS_scale_j_RelativeBal", "shape", SystMap<>::init(1.00));
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_scale_j_RelativeBal", "shape", SystMap<>::init(1.00));
        
    }
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,"CMS_scale_j_FlavorQCD", "shape", SystMap<>::init(1.00));
    cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt"}).AddSyst(cb,"CMS_scale_j_EC2", "shape", SystMap<>::init(1.00));
    if (year != 2016){
      cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb,"CMS_scale_j_RelativeSample_$ERA", "shape", SystMap<>::init(1.00)); // FIXME fix name
    }
    if (year != 2016){
      cb.cp().process(sig_procs).channel({"et","mt"}).AddSyst(cb,"CMS_scale_j_RelativeSample_$ERA", "shape", SystMap<>::init(1.00));
    }

          cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_scale_j_Absolute", "shape", SystMap<>::init(1.00));
      cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_scale_j_Absolute_$ERA", "shape", SystMap<>::init(1.00));
      cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_scale_j_BBEC1", "shape", SystMap<>::init(1.00));
      cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_scale_j_BBEC1_$ERA", "shape", SystMap<>::init(1.00));
      cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_scale_j_EC2", "shape", SystMap<>::init(1.00));
      cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_scale_j_EC2_$ERA", "shape", SystMap<>::init(1.00));
      cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_scale_j_FlavorQCD", "shape", SystMap<>::init(1.00));
      cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_scale_j_HF_$ERA", "shape", SystMap<>::init(1.00));
      // Seems to be missing
      cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_scale_j_HF", "shape", SystMap<>::init(1.00));
      // JER uncertainty
      cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_res_j_$ERA", "shape", SystMap<>::init(1.00));
      // cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_JER_$ERA", "shape", SystMap<>::init(1.00));




        //##############################################################################
        // JER
        //##############################################################################
        cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt","tt"}).AddSyst(cb,"CMS_res_j_$ERA", "shape", SystMap<>::init(1.00));
        // cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"mt","tt"}).AddSyst(cb,"CMS_JER_$ERA", "shape", SystMap<>::init(1.00));

    if (year != 2017){
      cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et"}).AddSyst(cb,"CMS_res_j_$ERA", "shape", SystMap<>::init(1.00)); 
      // cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et"}).AddSyst(cb,"CMS_JER_$ERA", "shape", SystMap<>::init(1.00)); 
    }
    else{
      cb.cp().process(JoinStr({{"ZL","ZJ","ZTT","TTJ","TTT","TT","W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ","VVL","ZT","HWW","ggH_hww125","qqH_hww125","ZH_hww125","WH_hww125","VH_hww125","EWKZ", "STT", "STL", "VVL"}, sig_procs})).channel({"et"}).AddSyst(cb,"CMS_res_j_$ERA", "shape", SystMap<>::init(1.00)); // FIXME Bogus norm 0.0 for channel htt_et_6_2017, process TTL, systematic CMS_JER_2017 Down
      // cb.cp().process(JoinStr({{"ZL","ZJ","ZTT","TTJ","TTT","TT","W","W_rest","ZJ_rest","TTJ_rest","VVJ_rest","VV","VVT","VVJ","VVL","ZT","HWW","ggH_hww125","qqH_hww125","ZH_hww125","WH_hww125","VH_hww125","EWKZ", "STT", "STL", "VVL"}, sig_procs})).channel({"et"}).AddSyst(cb,"CMS_JER_$ERA", "shape", SystMap<>::init(1.00)); // FIXME Bogus norm 0.0 for channel htt_et_6_2017, process TTL, systematic CMS_JER_2017 Down
    }
    
        //##############################################################################
        // pmiss unclustered energy scale T 
        //##############################################################################
        // cb.cp().process({"TTT","TTL","VVT","STT","VVL","STL"}).channel({"et","mt","tt","em"}).AddSyst(cb,
        cb.cp().process({"TTT","TTL","VVT","STT","VVL","STL","TT"}).channel({"et","mt","tt","em"}).AddSyst(cb,
                                                      "CMS_scale_met_unclustered_$ERA", "shape", SystMap<>::init(1.00));

        //##############################################################################
        // pmiss recoil corrections T 
        //##############################################################################
    cb.cp().process(JoinStr({sig_procs_recoil, all_mc_bkgs_recoil})).channel({"et","mt","em"}).bin_id({1}).AddSyst(cb,
                               "CMS_htt_boson_scale_met_0jet_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process(JoinStr({sig_procs_recoil, all_mc_bkgs_recoil})).channel({"et","mt","em"}).bin_id({1}).AddSyst(cb,
                               "CMS_htt_boson_reso_met_0jet_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process(JoinStr({sig_procs_recoil, all_mc_bkgs_recoil})).channel({"et","mt","em"}).bin_id({2}).AddSyst(cb,
                               "CMS_htt_boson_scale_met_1jet_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process(JoinStr({sig_procs_recoil, all_mc_bkgs_recoil})).channel({"et","mt","em"}).bin_id({2}).AddSyst(cb,
                               "CMS_htt_boson_reso_met_1jet_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process(JoinStr({sig_procs_recoil, all_mc_bkgs_recoil})).channel({"et","mt","em"}).bin_id({2,3,4,5,6,7,8,9,10}).AddSyst(cb,
                               "CMS_htt_boson_scale_met_2jet_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process(JoinStr({sig_procs_recoil, all_mc_bkgs_recoil})).channel({"et","mt","em"}).bin_id({2,3,4,5,6,7,8,9,10}).AddSyst(cb,
                               "CMS_htt_boson_reso_met_2jet_$ERA", "shape", SystMap<>::init(1.00));
    /*
      cb.cp().process(JoinStr({{"ZL"}, sig_procs_vbf, sig_procs_ggh})).channel({"em"}).AddSyst(cb, "CMS_htt_boson_reso_met_$ERA", "shape", SystMap<>::init(1.00));
      cb.cp().process(JoinStr({{"ZL"}, sig_procs_vbf, sig_procs_ggh})).channel({"em"}).AddSyst(cb, "CMS_htt_boson_scale_met_$ERA", "shape", SystMap<>::init(1.00));
    */
      
        //##############################################################################
        // STXS ggH theory 
        //##############################################################################

        //##############################################################################
        // jet→tau FF // missing unc in 0jet dir
        //##############################################################################

    // cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"et","mt","tt","em"}).bin_id({1,2,3}).AddSyst(cb,"CMS_scale_met_clustered_$ERA", "shape", SystMap<>::init(1.00));  
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).bin_id({1}).AddSyst(cb,"CMS_rawFF_$CHANNEL_qcd_0jet_unc1_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).bin_id({1}).AddSyst(cb,"CMS_rawFF_$CHANNEL_qcd_0jet_unc2_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).bin_id({2}).AddSyst(cb,"CMS_rawFF_$CHANNEL_qcd_1jet_unc1_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).bin_id({2}).AddSyst(cb,"CMS_rawFF_$CHANNEL_qcd_1jet_unc2_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).bin_id({2,3,4,5,6,7,8,9,10}).AddSyst(cb,"CMS_rawFF_$CHANNEL_qcd_2jet_unc1_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).bin_id({2,3,4,5,6,7,8,9,10}).AddSyst(cb,"CMS_rawFF_$CHANNEL_qcd_2jet_unc2_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).bin_id({1}).AddSyst(cb,"CMS_rawFF_$CHANNEL_w_0jet_unc1_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).bin_id({1}).AddSyst(cb,"CMS_rawFF_$CHANNEL_w_0jet_unc2_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).bin_id({2}).AddSyst(cb,"CMS_rawFF_$CHANNEL_w_1jet_unc1_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).bin_id({2}).AddSyst(cb,"CMS_rawFF_$CHANNEL_w_1jet_unc2_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).bin_id({2,3,4,5,6,7,8,9,10}).AddSyst(cb,"CMS_rawFF_$CHANNEL_w_2jet_unc1_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).bin_id({2,3,4,5,6,7,8,9,10}).AddSyst(cb,"CMS_rawFF_$CHANNEL_w_2jet_unc2_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).AddSyst(cb,"CMS_rawFF_$CHANNEL_tt_unc1_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).AddSyst(cb,"CMS_rawFF_$CHANNEL_tt_unc2_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).AddSyst(cb,"CMS_FF_closure_lpt_$CHANNEL_qcd", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).AddSyst(cb,"CMS_FF_closure_lpt_$CHANNEL_w", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).AddSyst(cb,"CMS_FF_closure_lpt_$CHANNEL_tt", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).AddSyst(cb,"CMS_FF_closure_OSSS_mvis_$CHANNEL_qcd_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).AddSyst(cb,"CMS_FF_closure_mt_$CHANNEL_w_unc1_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).AddSyst(cb,"CMS_FF_closure_mt_$CHANNEL_w_unc2_$ERA", "shape", SystMap<>::init(1.00));
    
        //##############################################################################
        // QCD bkg (em channel)
        //##############################################################################

        //##############################################################################
        // dyShape (ZPT Reweighting)
        //##############################################################################
    cb.cp().process( {"ZTT","ZT","ZL"}).channel({"et","mt","tt"}).AddSyst(cb,
                                          "CMS_htt_dyShape_$ERA", "shape", SystMap<>::init(1.00));
    // cb.cp().process({"ZL"}).channel({"em"}).AddSyst(cb, "CMS_htt_dyShape", "shape", SystMap<>::init(1.00));
    cb.cp().process({"ZLL"}).channel({"em"}).AddSyst(cb, "CMS_htt_dyShape", "shape", SystMap<>::init(1.00));

        //##############################################################################
        // ttbarShape
        //##############################################################################
    cb.cp().process( {"TTT"}).channel({"et","mt"}).AddSyst(cb,
                                       "CMS_htt_ttbarShape", "shape", SystMap<>::init(1.00));
    // FIXME: missing in Tyler's datacard! SD 8 Jun
    cb.cp().process( {"TTL"}).channel({"et","mt"}).AddSyst(cb,
                                       "CMS_htt_ttbarShape", "shape", SystMap<>::init(1.00));
        // cb.cp().process({"TTL"}).channel({"tt","em"}).AddSyst(cb, "CMS_htt_ttbarShape", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TT"}).channel({"tt","em"}).AddSyst(cb, "CMS_htt_ttbarShape", "shape", SystMap<>::init(1.00));
    
      
        //##############################################################################
        // embedded uncertainties
        //##############################################################################


    //Tracking Uncertainty // FIXME: missing in Tyler's datacards!: SD 8 Jun
    
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_eff_prong_emb_$ERA","shape",SystMap<>::init(1.00));
    //cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_eff_prong_$ERA","shape",SystMap<>::init(1.00));
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_eff_1prong1pizero_emb_$ERA","shape",SystMap<>::init(1.00));
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_eff_3prong1pizero_emb_$ERA","shape",SystMap<>::init(1.00));
    
    
    //50% correlation with ID unc in MC (Fixed: mt -> em)
    cb.cp().process({"embedded"}).channel({"et","em"}).AddSyst(cb,"CMS_eff_e_$ERA","lnN",SystMap<>::init(1.010));
    cb.cp().process({"embedded"}).channel({"et","em"}).AddSyst(cb,"CMS_eff_e_embedded_$ERA","lnN",SystMap<>::init(1.01732));
    
    cb.cp().process({"embedded"}).channel({"mt","em"}).AddSyst(cb,"CMS_eff_m_$ERA","lnN",SystMap<>::init(1.010));
    cb.cp().process({"embedded"}).channel({"mt","em"}).AddSyst(cb,"CMS_eff_m_embedded_$ERA","lnN",SystMap<>::init(1.01732));

    // Trg efficiency. Can be a single lnN because only single ele trigger
    // cb.cp().process({"embedded"}).channel({"et"}).AddSyst(cb,"CMS_singleeletrg_embedded_$ERA","lnN",SystMap<>::init(1.020));

    // FIXME: missing in Tyler's datacard:
    
    cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_singlemutrg_emb_$ERA","shape",SystMap<>::init(1.00));
    cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_mutautrg_emb_$ERA","shape",SystMap<>::init(1.00));
    
        // FIXME: missing in Tyler's datacard:
        
                 
    // cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_singlemutrg_$ERA","shape",SystMap<>::init(0.500));
    // cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_mutautrg_$ERA","shape",SystMap<>::init(0.500));
    
    //Tau ID eff // in Tyler's datacard:
    // cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_eff_t_embedded_pt30to35_$ERA", "shape", SystMap<>::init(1.00));
    // cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_eff_t_embedded_pt35to40_$ERA", "shape", SystMap<>::init(1.00));
    // cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_eff_t_embedded_ptgt40_$ERA", "shape", SystMap<>::init(1.00));
    
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_eff_t_embedded_pt30to35_$ERA", "shape", SystMap<>::init(0.866));
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_eff_t_embedded_pt35to40_$ERA", "shape", SystMap<>::init(0.866));
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_eff_t_embedded_ptgt40_$ERA", "shape", SystMap<>::init(0.866));

    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb, "CMS_tauideff_pt30to35_$ERA", "shape", SystMap<>::init(0.500));
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb, "CMS_tauideff_pt35to40_$ERA", "shape", SystMap<>::init(0.500));
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb, "CMS_tauideff_ptgt40_$ERA", "shape", SystMap<>::init(0.500));

    // Against ele and against mu for real taus
    // cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_eff_t_againstemu_embedded_$CHANNEL_$ERA","lnN",SystMap<>::init(1.05));
    
    cb.cp().process({"embedded"}).channel({"et","mt","em"}).AddSyst(cb,"CMS_htt_doublemutrg_$ERA", "lnN", SystMap<>::init(1.04));
    
    // TTBar Contamination
    // FIXME: missing in mt 2016 datacards!
    
    cb.cp().process({"embedded"}).channel({"et","mt","em"}).AddSyst(cb,"CMS_htt_emb_ttbar_$ERA", "shape", SystMap<>::init(1.00));
    

    //TES uncertainty // FIXME: missing in Tyler's datacards:
    
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_scale_emb_t_1prong_$ERA", "shape", SystMap<>::init(0.866));
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_scale_emb_t_1prong1pizero_$ERA", "shape", SystMap<>::init(0.866));
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_scale_emb_t_3prong_$ERA", "shape", SystMap<>::init(0.866));
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_scale_emb_t_3prong1pizero_$ERA", "shape", SystMap<>::init(0.866));
    

       //TES uncertainty // FIXME: missing in Tyler's datacards:
          
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_scale_t_1prong_$ERA", "shape", SystMap<>::init(0.500));
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_scale_t_1prong1pizero_$ERA", "shape", SystMap<>::init(0.500));
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_scale_t_3prong_$ERA", "shape", SystMap<>::init(0.500));
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_scale_t_3prong1pizero_$ERA", "shape", SystMap<>::init(0.500));
    
    //electron energy scale // FIXME: missing in Tyler's datacards (not splitted in EE/EB):
    /*
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_scale_emb_e_barrel_$ERA","shape",SystMap<>::init(1.0));      
    cb.cp().process({"embedded"}).channel({"et","mt"}).AddSyst(cb,"CMS_scale_emb_e_endcap_$ERA","shape",SystMap<>::init(1.0));
    */
    
        //##############################################################################
        // 
        //##############################################################################
    
      


    
    // TH ggh unc FIXME: in Abdollahs datacards these are one-sided, so do not use for now!
    
    cb.cp().process(sig_procs_ggh).channel({"em","et","mt"}).AddSyst(cb,
                                           "THU_ggH_VBF2j", "shape", SystMap<>::init(1.00));
    cb.cp().process(sig_procs_ggh).channel({"em","et","mt"}).AddSyst(cb,
                                           "THU_ggH_VBF3j", "shape", SystMap<>::init(1.00));
    cb.cp().process(sig_procs_ggh).channel({"em","et","mt"}).AddSyst(cb,
                                           "THU_ggH_qmtop", "shape", SystMap<>::init(1.00));
    cb.cp().process(sig_procs_ggh).channel({"em","et","mt"}).AddSyst(cb,
                                           "THU_ggH_Mig01", "shape", SystMap<>::init(1.00));
    cb.cp().process(sig_procs_ggh).channel({"em","et","mt"}).AddSyst(cb,
                                           "THU_ggH_Mig12", "shape", SystMap<>::init(1.00));
    cb.cp().process(sig_procs_ggh).channel({"em","et","mt"}).AddSyst(cb,
                                           "THU_ggH_Mu", "shape", SystMap<>::init(1.00));
    cb.cp().process(sig_procs_ggh).channel({"em","et","mt"}).AddSyst(cb,
                                           "THU_ggH_Res", "shape", SystMap<>::init(1.00));
    cb.cp().process(sig_procs_ggh).channel({"em","et","mt"}).AddSyst(cb,
                                           "THU_ggH_PT60", "shape", SystMap<>::init(1.00));
    cb.cp().process(sig_procs_ggh).channel({"em","et","mt"}).AddSyst(cb,
                                           "THU_ggH_PT120", "shape", SystMap<>::init(1.00));

                                           
    }
        
        
        

 
        //##############################################################################
        // Theoretical Uncertainties on signal
        //##############################################################################
        
        // Scale uncertainty on signal Applies to ggH in boosted and VBF. Event-by-event weight applied as a func(on of pth or mjj. Fully correlated between categories and final states.
        
        


        
                        
                        
    if (do_shapeSyst){
            cb.cp().process(JoinStr({sig_procs_vbf,sig_procs_wh,sig_procs_zh})).AddSyst(cb,"JHUvsPow", "lnN", SystMap<>::init(1.05));
            // cb.cp().process(JoinStr({sig_procs_vbf,sig_procs_wh,sig_procs_zh})).AddSyst(cb,"JHUvsPow", "shape", SystMap<>::init(1.00));
    }

    cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_eff_e_$ERA", "lnN", SystMap<>::init(1.02));
    cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb, "CMS_eff_m_$ERA", "lnN", SystMap<>::init(1.02));

    // emu
    cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb,"CMS_htt_emutrg_$ERA","lnN",SystMap<>::init(1.04));
    // cb.cp().process({"embedded"}).channel({"em"}).AddSyst(cb,"CMS_htt_emutrg_$ERA","lnN",SystMap<>::init(1.04));
    cb.cp().process({"embedded"}).channel({"em"}).AddSyst(cb,"CMS_htt_emutrg_emb_$ERA","lnN",SystMap<>::init(1.04));
    // cb.cp().process(JoinStr({sig_procs, all_mc_bkgs})).channel({"em"}).AddSyst(cb,"CMS_htt_emutrg_emb_$ERA","lnN",SystMap<>::init(1.02));
    // cb.cp().process({"QCD"}).channel({"em"}).AddSyst(cb, "QCDsystBkgNorm_$ERA", "shape", SystMap<>::init(1.0));
    cb.cp().process({"QCD"}).channel({"em"}).bin_id({1}).AddSyst(cb, "QCDsystBkgNorm_0jet_$ERA", "shape", SystMap<>::init(1.0));
    cb.cp().process({"QCD"}).channel({"em"}).bin_id({2}).AddSyst(cb, "QCDsystBkgNorm_boosted_$ERA", "shape", SystMap<>::init(1.0));
    cb.cp().process({"QCD"}).channel({"em"}).bin_id({3,4,5,6,7,8,9,10}).AddSyst(cb, "QCDsystBkgNorm_vbf_$ERA", "shape", SystMap<>::init(1.0));

    cb.cp().process({"jetFakes"}).channel({"et","mt"}).AddSyst(cb,"CMS_FF_closure_lpt_xtrg_$CHANNEL_qcd", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).AddSyst(cb,"CMS_FF_closure_lpt_xtrg_$CHANNEL_w", "shape", SystMap<>::init(1.00));
    cb.cp().process({"jetFakes"}).channel({"et","mt"}).AddSyst(cb,"CMS_FF_closure_lpt_xtrg_$CHANNEL_tt", "shape", SystMap<>::init(1.00));
        
    cb.cp().process(JoinStr({{"ZL","ZT","TTT","VVT","STT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).channel({"et"}).AddSyst(cb,"CMS_tauideff_vsmu_vloose_$ERA","lnN",SystMap<>::init(1.03));
    cb.cp().process({"embedded"}).channel({"et"}).AddSyst(cb,"CMS_tauideff_vsmu_vloose_$ERA","lnN",SystMap<>::init(1.025));
    cb.cp().process({"embedded"}).channel({"et"}).AddSyst(cb,"CMS_eff_t_embedded_vsmu_vloose_$ERA","lnN",SystMap<>::init(1.04334));
    
    cb.cp().process(JoinStr({{"ZL","ZT","TTT","VVT","STT","HWW","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","VH_hww125","ggH_htt_nonfid125","qqH_htt_nonfid125","WH_htt_nonfid125","ZH_htt_nonfid125"},sig_procs})).channel({"mt"}).AddSyst(cb,"CMS_tauideff_vse_vvvloose_$ERA","lnN",SystMap<>::init(1.03));
    cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_tauideff_vse_vvvloose_$ERA","lnN",SystMap<>::init(1.025));
    cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_eff_t_embedded_vse_vvvloose_$ERA","lnN",SystMap<>::init(1.04334));

    cb.cp().process({"ZL","VVL","TTL","STL"}).channel({"et"}).AddSyst(cb,"CMS_e_FakeTau_barrel_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"ZL","VVL","TTL","STL"}).channel({"et"}).AddSyst(cb,"CMS_e_FakeTau_endcap_$ERA", "shape", SystMap<>::init(1.00));

    cb.cp().process({"ZL","VVL","TTL","STL"}).channel({"mt"}).AddSyst(cb,"CMS_m_FakeTau_etalt0p4_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"ZL","VVL","TTL","STL"}).channel({"mt"}).AddSyst(cb,"CMS_m_FakeTau_eta0p4to0p8_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"ZL","VVL","TTL","STL"}).channel({"mt"}).AddSyst(cb,"CMS_m_FakeTau_eta0p8to1p2_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"ZL","VVL","TTL","STL"}).channel({"mt"}).AddSyst(cb,"CMS_m_FakeTau_eta1p2to1p7_$ERA", "shape", SystMap<>::init(1.00));
    cb.cp().process({"ZL","VVL","TTL","STL"}).channel({"mt"}).AddSyst(cb,"CMS_m_FakeTau_etagt1p7_$ERA", "shape", SystMap<>::init(1.00));

    // cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_m_FakeTau_etalt0p4_$ERA", "shape", SystMap<>::init(0.500));
    // cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_m_FakeTau_eta0p4to0p8_$ERA", "shape", SystMap<>::init(0.500));
    // cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_m_FakeTau_eta0p8to1p2_$ERA", "shape", SystMap<>::init(0.500));
    // cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_m_FakeTau_eta1p2to1p7_$ERA", "shape", SystMap<>::init(0.500));
    // cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_m_FakeTau_etagt1p7_$ERA", "shape", SystMap<>::init(0.500));

    // cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_m_embedded_FakeTau_etalt0p4_$ERA", "shape", SystMap<>::init(0.866));
    // cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_m_embedded_FakeTau_eta0p4to0p8_$ERA", "shape", SystMap<>::init(0.866));
    // cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_m_embedded_FakeTau_eta0p8to1p2_$ERA", "shape", SystMap<>::init(0.866));
    // cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_m_embedded_FakeTau_eta1p2to1p7_$ERA", "shape", SystMap<>::init(0.866));
    // cb.cp().process({"embedded"}).channel({"mt"}).AddSyst(cb,"CMS_m_embedded_FakeTau_etagt1p7_$ERA", "shape", SystMap<>::init(0.866));

    if (year == 2016) cb.cp().process({"embedded"}).channel({"mt"}).bin_id({1}).AddSyst(cb,"CMS_test","lnN",SystMap<>::init(1.1));

    cb.cp().process({"embedded"}).channel({"em"}).bin_id({1}).AddSyst(cb, "CMS_emb_extra_0jet_$ERA", "lnN",SystMap<>::init(1.20));
    cb.cp().process({"embedded"}).channel({"em"}).bin_id({2}).AddSyst(cb, "CMS_emb_extra_boosted_$ERA","lnN",SystMap<>::init(1.20));
    cb.cp().process({"embedded"}).channel({"em"}).bin_id({3,4,5,6,7,8,9,10}).AddSyst(cb, "CMS_emb_extra_vbf_$ERA","lnN",SystMap<>::init(1.20));
    }
}
