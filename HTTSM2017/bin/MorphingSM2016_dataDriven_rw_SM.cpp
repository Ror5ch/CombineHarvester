#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "boost/algorithm/string/predicate.hpp"
#include "boost/program_options.hpp"
#include "boost/lexical_cast.hpp"
#include "boost/regex.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/CardWriter.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombineTools/interface/Algorithm.h"
#include "CombineHarvester/CombineTools/interface/AutoRebin.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/HTTSM2017/interface/HttSystematics_SMRun2_dataDriven_rw_SM.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"
#include "TF1.h"

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;

template <typename T>
void To1Bin(T* proc)
{
    std::unique_ptr<TH1> originalHist = proc->ClonedScaledShape();
    TH1F *hist = new TH1F("hist","hist",1,0,1);
    double err = 0;
    double rate =
    originalHist->IntegralAndError(0, originalHist->GetNbinsX() + 1, err);
    hist->SetDirectory(0);
    hist->SetBinContent(1, rate);
    hist->SetBinError(1, err);
    proc->set_shape(*hist, true);  // True means adjust the process rate to the
    // integral of the hist
}

bool BinIsControlRegion(ch::Object const* obj)
{
    return (boost::regex_search(obj->bin(),boost::regex{"_cr$"}) || (obj->channel() == std::string("mm")));
}

// Useful to have the inverse sometimes too
bool BinIsNotControlRegion(ch::Object const* obj)
{
    return !BinIsControlRegion(obj);
}



int main(int argc, char** argv) {
    // First define the location of the "auxiliaries" directory where we can
    // source the input files containing the datacard shapes
    string SM125= "";
    string mass = "mA";
    string output_folder = "sm_run2";
    // TODO: option to pick up cards from different dirs depending on channel?
    // ^ Something like line 90?
    string input_folder_em="USCMS/";
    string input_folder_et="USCMS/";
    string input_folder_mt="USCMS/";
    string input_folder_tt="USCMS/";
    string input_folder_mm="USCMS/";
    string input_folder_ttbar="USCMS/";
    string postfix="";
    bool auto_rebin = false;
    bool manual_rebin = false;
    bool real_data = false;
    int control_region = 0;
    bool check_neg_bins = false;
    bool poisson_bbb = false;
    bool do_w_weighting = false;
    bool mm_fit = false;
    bool ttbar_fit = false;
    bool do_jetfakes = true;
    bool do_embedded = true;
    po::variables_map vm;
    po::options_description config("configuration");
    config.add_options()
      ("mass,m", po::value<string>(&mass)->default_value(mass))
      
      ("input_folder_em", po::value<string>(&input_folder_em)->default_value("USCMS"))
      ("input_folder_et", po::value<string>(&input_folder_et)->default_value("USCMS"))
      ("input_folder_mt", po::value<string>(&input_folder_mt)->default_value("USCMS"))
      ("input_folder_tt", po::value<string>(&input_folder_tt)->default_value("USCMS"))
      ("input_folder_mm", po::value<string>(&input_folder_mm)->default_value("USCMS"))
      ("input_folder_ttbar", po::value<string>(&input_folder_ttbar)->default_value("USCMS"))
      
      ("postfix", po::value<string>(&postfix)->default_value(""))
      ("auto_rebin", po::value<bool>(&auto_rebin)->default_value(false))
      ("real_data", po::value<bool>(&real_data)->default_value(false))
      ("manual_rebin", po::value<bool>(&manual_rebin)->default_value(false))
      ("output_folder", po::value<string>(&output_folder)->default_value("sm_run2"))
      ("SM125,h", po::value<string>(&SM125)->default_value(SM125))
      ("control_region", po::value<int>(&control_region)->default_value(0))
      ("mm_fit", po::value<bool>(&mm_fit)->default_value(true))
      ("ttbar_fit", po::value<bool>(&ttbar_fit)->default_value(true))
      ("jetfakes", po::value<bool>(&do_jetfakes)->default_value(false))
      ("embedded", po::value<bool>(&do_embedded)->default_value(false))
      ("check_neg_bins", po::value<bool>(&check_neg_bins)->default_value(false))
      ("poisson_bbb", po::value<bool>(&poisson_bbb)->default_value(false))
      ("w_weighting", po::value<bool>(&do_w_weighting)->default_value(false));
    po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
    po::notify(vm);
    
    
    
    
    
    typedef vector<string> VString;
    typedef vector<pair<int, string>> Categories;
    //! [part1]
    // First define the location of the "auxiliaries" directory where we can
    // source the input files containing the datacard shapes
    //    string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/CombineTools/bin/AllROOT_20fb/";
    std::map<string, string> input_dir;
//    input_dir["em"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTAC2017/shapes/"+input_folder_em+"/";
    input_dir["mt"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTAC2017/shapes/"+input_folder_mt+"/";
    input_dir["et"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTAC2017/shapes/"+input_folder_et+"/";
    input_dir["em"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTAC2017/shapes/"+input_folder_em+"/";
    input_dir["tt"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTAC2017/shapes/"+input_folder_tt+"/";
//    input_dir["mm"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTAC2017/shapes/"+input_folder_mm+"/";
    input_dir["ttbar"]  = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/HTTAC2017/shapes/"+input_folder_ttbar+"/";
    
    
    
    //    VString chns = {"et"};
    	 //  VString chns = {"mt","em","et"};
 //   VString chns = {"mt"};

     //  VString chns = {"mt","et","tt","em"};
  //  VString chns = {"mt","et","tt"};
//    VString chns = {"mt","tt"};
    //VString chns = {"et","tt"};
//    VString chns = {"et","mt"};
 ///   VString chns = {"et"};
//    VString chns = {"mt","tt"};
    VString chns = {"tt"};
    if (mm_fit) chns.push_back("mm");
    if (ttbar_fit) chns.push_back("ttbar");
    
    // ZL, TTT, VVT, jetFakes, embedded <- backgrounds for fake factor & embedded
    // jetFakes replace VVJ, TTJ, ZJ, W, QCD
    // embedded replace ZTT EWKZ
    // remaining background is ZL, TTT, VVT.

    map<string, VString> bkg_procs;
    if (do_jetfakes && do_embedded ){
      bkg_procs["et"] = {"embedded", "ZL", "TTT", "VVT", "jetFakes"};
      bkg_procs["mt"] = {"embedded", "ZL", "TTT", "VVT", "jetFakes"};
      bkg_procs["tt"] = {"embedded", "ZL", "TTT", "VVT", "jetFakes"};
    } else if (do_embedded && !do_jetfakes ) {
      bkg_procs["et"] = {"embedded", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
      bkg_procs["mt"] = {"embedded", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
      bkg_procs["tt"] = {"embedded", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
    } else if (!do_embedded && do_jetfakes ) {
      bkg_procs["et"] = {"ZTT", "EWKZ", "ZL", "TTT", "VVT", "jetFakes"};
      bkg_procs["mt"] = {"ZTT", "EWKZ", "ZL", "TTT", "VVT", "jetFakes"};
      bkg_procs["tt"] = {"ZTT", "EWKZ", "ZL", "TTT", "VVT", "jetFakes"};
    } else if (!do_embedded && !do_jetfakes ) {
      bkg_procs["et"] = {"ZTT", "EWKZ", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
      bkg_procs["mt"] = {"ZTT", "EWKZ", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
      bkg_procs["tt"] = {"ZTT", "EWKZ", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
    } else {
      std::cout << "This shold not have happened !" << std::endl;
      return -1;
    }

    // ym this needs to be updated
    bkg_procs["em"] = {"ZTT", "W", "QCD", "ZL", "TT", "VV", "EWKZ", "ggH_hww125", "qqH_hww125"};
    bkg_procs["mm"] = {"W", "ZL", "TT", "VV"};
    bkg_procs["ttbar"] = {"ZTT", "W", "QCD", "ZL", "TT", "VV", "EWKZ"};
    
    
    
    ch::CombineHarvester cb;
    
    
    
    map<string,Categories> cats;
    cats["em"] = {
        {1, "em_0jet"},
        {2, "em_boosted"},
        {3, "em_vbf"}
    };

    cats["et"] = {
        {1, "et_0jet"},
        {2, "et_boosted"},
        {3, "et_vbf"}
    };
    
    cats["mt"] = {
        {1, "mt_0jet"},
        {2, "mt_boosted"},
        {3, "mt_vbf"}
    };
    
    /*
    cats["em"] = {
        {1, "em_0jet"},
        {2, "em_boosted"},
        {3, "em_vbf"}};
    */
    
    cats["tt"] = {        
        {1, "tt_0jet"},
        {2, "tt_boosted"},
        {3, "tt_vbf"}
    };
    
    
    // ym
    //cats["mm"] = {
    //    {1, "mm_0jet"},
    //    {2, "mm_1jet"},
    //    {3, "mm_vbf"}
    // };
    //cats["ttbar"] = {
    //    {1, "ttbar_all"}
    //};
    
    
    if (control_region > 0){
        // for each channel use the categories >= 10 for the control regions
        // the control regions are ordered in triples (10,11,12),(13,14,15)...
        for (auto chn : chns){
            // for em or tt or mm do nothing
            if (ch::contains({"mt", "et"}, chn)) {
                    
                Categories queue;
                int binid = 20;
                //            for (auto cat:cats[chn]){
                //                queue.push_back(make_pair(binid,chn+"_wjets_cr"));
                //                queue.push_back(make_pair(binid+1,chn+"_qcd_cr"));
                //                queue.push_back(make_pair(binid+2,chn+"_wjets_ss_cr"));
                
                queue.push_back(make_pair(binid,chn+"_wjets_0jet_cr"));
                queue.push_back(make_pair(binid+1,chn+"_wjets_boosted_cr"));
//                queue.push_back(make_pair(binid+2,chn+"_wjets_vbf_cr"));
                queue.push_back(make_pair(binid+3,chn+"_antiiso_0jet_cr"));
                queue.push_back(make_pair(binid+4,chn+"_antiiso_boosted_cr"));
//                queue.push_back(make_pair(binid+5,chn+"_antiiso_vbf_cr"));
                
                cats[chn].insert(cats[chn].end(),queue.begin(),queue.end());
            }
            // Add tautau QCD CRs
            if (ch::contains({"tt"}, chn)) {
                    
                Categories queue;
                int binid = 20;
                
                queue.push_back(make_pair(binid,chn+"_0jet_qcd_cr"));
                queue.push_back(make_pair(binid+1,chn+"_boosted_qcd_cr"));
                queue.push_back(make_pair(binid+2,chn+"_vbf_D0_0to0p2_qcd_cr_DCPm"));
                queue.push_back(make_pair(binid+3,chn+"_vbf_D0_0p2to0p4_qcd_cr_DCPm"));
                queue.push_back(make_pair(binid+4,chn+"_vbf_D0_0p4to0p8_qcd_cr_DCPm"));
                queue.push_back(make_pair(binid+5,chn+"_vbf_D0_0p8to1_qcd_cr_DCPm"));
                queue.push_back(make_pair(binid+6,chn+"_vbf_D0_0to0p2_qcd_cr_DCPp"));
                queue.push_back(make_pair(binid+7,chn+"_vbf_D0_0p2to0p4_qcd_cr_DCPp"));
                queue.push_back(make_pair(binid+8,chn+"_vbf_D0_0p4to0p8_qcd_cr_DCPp"));
                queue.push_back(make_pair(binid+9,chn+"_vbf_D0_0p8to1_qcd_cr_DCPp"));

                
                cats[chn].insert(cats[chn].end(),queue.begin(),queue.end());
            }
        }
    } // end CR et mt > 0

    
    
    
    // Or equivalently, specify the mass points explicitly:
    //vector<string> sig_procs = {"ggH_htt","WH_htt","ZH_htt","qqH_mix"};
    //vector<string> sig_procs = {"ggH_htt","WH_htt","ZH_htt","reweighted_qqH_htt", "reweighted_qqH_htt_0M"};
    //    vector<string> sig_procs = {"ggH_htt","WH_htt","ZH_htt","reweighted_qqH_htt","reweighted_qqH_htt_0M","ZH_htt_0M","WH_htt_0M"};
    //    vector<string> sig_procs = {"ggH_htt","WH_htt","ZH_htt","reweighted_qqH_htt","reweighted_qqH_htt_0M","ZH_htt_0M","WH_htt_0M","reweighted_qqH_htt_0Mf05ph0","ZH_htt_0Mf05ph0","WH_htt_0Mf05ph0"};
    vector<string> sig_procs = {"GGH2Jets_sm_M","reweighted_WH_htt_0PM","reweighted_ZH_htt_0PM","reweighted_qqH_htt_0PM"};
    // just to trick the code to create ttbar dir, since no 0M signal in input root files!
//    vector<string> sig_procs_ttbar = {"ggH_htt","WH_htt","ZH_htt","qqH_htt"};
    vector<string> sig_procs_ttbar = {"GGH2Jets_sm_M","reweighted_WH_htt_0PM","reweighted_ZH_htt_0PM","reweighted_qqH_htt_0PM"};

//    vector<string> masses = {"110","120","125","130","140"};
//    vector<string> masses = {"120","125","130"};
    vector<string> masses = {"125"};
	    
    using ch::syst::bin_id;
    
    //! [part2]
    for (auto chn : chns) {
        cb.AddObservations({"*"}, {"htt"}, {"13TeV"}, {chn}, cats[chn]);
        cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {chn}, bkg_procs[chn], cats[chn], false);
	// don't use signal for ttbar CR because no BSM model in those inout files, and this CR is signal free 
	/*
        if(chn != std::string("ttbar")){
	  cb.AddProcesses(masses,   {"htt"}, {"13TeV"}, {chn}, sig_procs, cats[chn], true);
	}
	*/
	cb.AddProcesses(masses,   {"htt"}, {"13TeV"}, {chn}, sig_procs, cats[chn], true);
    

        //Needed to add ewkz and W as these are not not available/Negative in qcd cR
    }
    

//    //Add EWKZ and W manually !!!!!!
//    
//    cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {"mt"}, {"EWKZ"}, {{1, "mt_0jet"},{2, "mt_boosted"},{3, "mt_vbf"}}, false);
//    cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {"et"}, {"EWKZ"}, {{1, "et_0jet"},{2, "et_boosted"},{3, "et_vbf"}}, false);

    if (control_region > 0){

      cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {"et"}, {"W"},
                         {
                           {1, "et_0jet"},
                             {2, "et_boosted"},
                               {3, "et_vbf"},
                                                   {23, "et_antiiso_0jet_cr"},
                                                     {24, "et_antiiso_boosted_cr"}

                         }, false);



      cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {"mt"}, {"W"}, 
			 {
			   {1, "mt_0jet"},
			     {2, "mt_boosted"},	   
			       {3, "mt_vbf"},	    
					       {20, "mt_wjets_0jet_cr"},
						 {21, "mt_wjets_boosted_cr"},
						   {23, "mt_antiiso_0jet_cr"},
						     {24, "mt_antiiso_boosted_cr"}
			 }, false);
    }
//    else if (!do_jetfakes){
//      cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {"et"}, {"W"}, {{1, "et_0jet"},{2, "et_boosted"},{3, "et_vbf"}}, false);
//      cb.AddProcesses(   {"*"}, {"htt"}, {"13TeV"}, {"mt"}, {"W"}, {{1, "mt_0jet"},{2, "mt_boosted"},{3, "mt_vbf"}}, false);
//    }
//    
    
    
    //! [part4]
    
    
    //Some of the code for this is in a nested namespace, so
    // we'll make some using declarations first to simplify things a bit.
    //    using ch::syst::SystMap;
    //    using ch::syst::era;
    //    using ch::syst::channel;
    //    using ch::syst::bin_id;
    //    using ch::syst::process;
    
    
    
    
    if ((control_region > 0) || mm_fit){
        // Since we now account for QCD in the high mT region we only
        // need to filter signal processes
        cb.FilterAll([](ch::Object const* obj) {
            return (BinIsControlRegion(obj) && obj->signal());
        });
    }
    
    
    ch::AddSMRun2Systematics_dataDriven_rw_SM(cb, control_region, mm_fit, ttbar_fit);
    
    
        
    
    
    //! [part7]
    for (string chn:chns){
      cout << " &&&&&&&& creating root files for ch: "<< chn << "\n";
        cb.cp().channel({chn}).backgrounds().ExtractShapes(
                                                           input_dir[chn] + "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
                                                           "$BIN/$PROCESS",
                                                           "$BIN/$PROCESS_$SYSTEMATIC");
	if(chn != std::string("ttbar")){
	  cout << "           -> it is not ttbar so take also signal shapes..\n";
	  cb.cp().channel({chn}).process(sig_procs).ExtractShapes(
								  input_dir[chn] + "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
								  "$BIN/$PROCESS$MASS",
								  "$BIN/$PROCESS$MASS_$SYSTEMATIC");
	}
	else{
	  cout << "           -> it IS ttbar so take also signal shapes..\n";
	  cb.cp().channel({chn}).process(sig_procs_ttbar).ExtractShapes(
								  input_dir[chn] + "htt_"+chn+".inputs-sm-13TeV"+postfix+".root",
								  "$BIN/$PROCESS$MASS",
								  "$BIN/$PROCESS$MASS_$SYSTEMATIC");
	}
    }
    
    
    
    
    
    //Now delete processes with 0 yield
    cb.FilterProcs([&](ch::Process *p) {
        bool null_yield = !(p->rate() > 0. || BinIsControlRegion(p));
        if (null_yield){
            std::cout << "[Null yield] Removing process with null yield: \n ";
            std::cout << ch::Process::PrintHeader << *p << "\n";
            cb.FilterSysts([&](ch::Systematic *s){
                bool remove_syst = (MatchingProcess(*p,*s));
                return remove_syst;
            });
        }
        return null_yield;
    });
    
    
    
    
    
    // And convert any shapes in the CRs to lnN:
    // Convert all shapes to lnN at this stage
    cb.cp().FilterSysts(BinIsNotControlRegion).syst_type({"shape"}).ForEachSyst([](ch::Systematic *sys) {
        sys->set_type("lnN");
    });
    
    
    //     //Merge to one bin for control region bins
    //    cb.cp().FilterAll(BinIsNotControlRegion).ForEachProc(To1Bin<ch::Process>);
    //    cb.cp().FilterAll(BinIsNotControlRegion).ForEachObs(To1Bin<ch::Observation>);
    
    
    
    
    //! [part8]
    auto bbb = ch::BinByBinFactory()
    .SetAddThreshold(0.05)
    .SetMergeThreshold(0.8)
    .SetFixNorm(false);
    bbb.MergeBinErrors(cb.cp().backgrounds());
    bbb.AddBinByBin(cb.cp().backgrounds(), cb);
    
    
    
    // And now do bbb for the control region with a slightly different config:
    auto bbb_ctl = ch::BinByBinFactory()
    .SetPattern("CMS_$ANALYSIS_$BIN_$ERA_$PROCESS_bin_$#")
    .SetAddThreshold(0.)
    .SetMergeThreshold(0.8)
    .SetFixNorm(false)  // contrary to signal region, bbb *should* change yield here
    .SetVerbosity(1);
    // Will merge but only for non W and QCD processes, to be on the safe side
    bbb_ctl.MergeBinErrors(cb.cp().process({"QCD", "W"}, false).FilterProcs(BinIsNotControlRegion));
    bbb_ctl.AddBinByBin(cb.cp().process({"QCD", "W"}, false).FilterProcs(BinIsNotControlRegion), cb);
    cout << " done\n";
    
    
    
    
    // This function modifies every entry to have a standardised bin name of
    // the form: {analysis}_{channel}_{bin_id}_{era}
    // which is commonly used in the htt analyses
    ch::SetStandardBinNames(cb);
    //! [part8]
    
    //! [part9]
    // First we generate a set of bin names:
    //    set<string> bins = cb.bin_set();
    // This method will produce a set of unique bin names by considering all
    // Observation, Process and Systematic entries in the CombineHarvester
    // instance.
    
    // We create the output root file that will contain all the shapes.
    // Here we define a CardWriter with a template for how the text datacard
    // and the root files should be named.
    //    ch::CardWriter writer("$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt",
    //                          "$TAG/common/$ANALYSIS_$CHANNEL.input_$ERA.root");
    //    // writer.SetVerbosity(1);
    //    writer.WriteCards("output/htt_cards8_20fb_22Sep/cmb", cb);
    //    for (auto chn : cb.channel_set()) {
    //        writer.WriteCards("output/htt_cards8_20fb_22Sep/" + chn, cb.cp().channel({chn}));
    //    }
    //    TFile output("output/htt_cards8_20fb_22Sep/htt.input.root", "RECREATE");
    
    
    // Add a theory group to the bottom of the DCs for use with CH Uncertainty Breakdown
    cb.SetGroup("all", {".*"});
    cb.SetGroup("nonThySyst", {".*"});
//    string theoryUncertsString = "CMS_scale_gg_.*|CMS_qqH_QCDUnc.*|CMS_ggH_PDF.*|CMS_qqH_PDF.*|CMS_ggH_UEPS.*|CMS_qqH_UEPS.*|BR_htt_THU.*|BR_htt_PU_mq.*|BR_htt_PU_alphas.*|BR_hww_THU.*|BR_hww_PU_mq.*|BR_hww_PU_alphas.*|QCDScale_ggH.*|QCDScale_qqH.*|QCDScale_VH.*|QCDScale_VH.*|pdf_Higgs_gg.*|pdf_Higgs_qq.*|pdf_Higgs_VH.*|pdf_Higgs_VH.*|";
//    cb.SetGroup("theory", {theoryUncertsString});
//    cb.RemoveGroup("nonThySyst", {theoryUncertsString});
//    cb.SetGroup("JES", {"CMS_scale_j.*"});
//    cb.SetGroup("BinByBin", {"CMS_htt_.*_bin_.*"});
    
    
    
    
    
    //! [part9]
    // First we generate a set of bin names:
    
    
    //Write out datacards. Naming convention important for rest of workflow. We
    //make one directory per chn-cat, one per chn and cmb. In this code we only
    //store the individual datacards for each directory to be combined later, but
    //note that it's also possible to write out the full combined card with CH
    string output_prefix = "output/";
    if(output_folder.compare(0,1,"/") == 0) output_prefix="";
    ch::CardWriter writer(output_prefix + output_folder + "/$TAG/$MASS/$BIN.txt",
                          output_prefix + output_folder + "/$TAG/common/htt_input.root");
    
    
    // We're not using mass as an identifier - which we need to tell the CardWriter
    // otherwise it will see "*" as the mass value for every object and skip it
    //    writer.SetWildcardMasses({});
    //    writer.SetVerbosity(1);
    
    writer.WriteCards("cmb", cb);
    for (auto chn : chns) {
        if(chn == std::string("mm"))
        {
            continue;
        }
        // per-channel
        writer.WriteCards(chn, cb.cp().channel({chn, "mm"}));
        // And per-channel-category
        //  THERE IS A FLAW IN COMBINEHARVESTER
        //        writer.WriteCards("htt_"+chn+"_1_13TeV", cb.cp().channel({chn,"mm"}).bin_id({1,10,13}));
        //        writer.WriteCards("htt_"+chn+"_2_13TeV", cb.cp().channel({chn,"mm"}).bin_id({2,10,13}));
        //        writer.WriteCards("htt_"+chn+"_3_13TeV", cb.cp().channel({chn,"mm"}).bin_id({3,11,14}));
        //        writer.WriteCards("htt_"+chn+"_4_13TeV", cb.cp().channel({chn,"mm"}).bin_id({4,11,14}));
        //        writer.WriteCards("htt_"+chn+"_5_13TeV", cb.cp().channel({chn,"mm"}).bin_id({5,12,15}));
        //        writer.WriteCards("htt_"+chn+"_6_13TeV", cb.cp().channel({chn,"mm"}).bin_id({6,12,15}));
        writer.WriteCards("htt_"+chn+"_1_13TeV", cb.cp().channel({chn}).bin_id({1}));
        writer.WriteCards("htt_"+chn+"_2_13TeV", cb.cp().channel({chn}).bin_id({2}));
        writer.WriteCards("htt_"+chn+"_3_13TeV", cb.cp().channel({chn}).bin_id({3}));
        
        
        for (auto mmm : masses){
            
            if (mm_fit){
                cb.cp().channel({"mm"}).bin_id({1}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_mm_1_13TeV.txt", output_prefix + output_folder +"/"+chn+"/common/htt_input_mm1.root");
                cb.cp().channel({"mm"}).bin_id({2}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_mm_2_13TeV.txt", output_prefix + output_folder +"/"+chn+"/common/htt_input_mm2.root");
                cb.cp().channel({"mm"}).bin_id({3}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_mm_3_13TeV.txt", output_prefix + output_folder +"/"+chn+"/common/htt_input_mm3.root");
            }
            
            if (ttbar_fit){
	      cout << " %%%%%%%%%%%%%%%%%%% making ttbar cards\n";
	      cb.cp().channel({"ttbar"}).bin_id({1}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_ttbar_1_13TeV.txt", output_prefix + output_folder +"/"+chn+"/common/htt_input_ttbar1.root");
            }
            
            
            if (control_region > 0){
                
                if (ch::contains({"et", "mt"}, chn)) {
                    
                
                    cb.cp().channel({chn}).bin_id({20}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_20_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"20.root");
                    cb.cp().channel({chn}).bin_id({21}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_21_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"21.root");
//                    cb.cp().channel({chn}).bin_id({12}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_12_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"12.root");
                    cb.cp().channel({chn}).bin_id({23}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_23_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"23.root");
                    cb.cp().channel({chn}).bin_id({24}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_24_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"24.root");
//                    cb.cp().channel({chn}).bin_id({15}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_15_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"15.root");
                    
                        
                    cb.cp().channel({chn}).bin_id({20}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_20_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"20.root");
                    cb.cp().channel({chn}).bin_id({21}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_21_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"21.root");
//                    cb.cp().channel({chn}).bin_id({12}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_12_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"12.root");
                    cb.cp().channel({chn}).bin_id({23}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_23_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"23.root");
                    cb.cp().channel({chn}).bin_id({24}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_24_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"24.root");
//                    cb.cp().channel({chn}).bin_id({15}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_15_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"15.root");
                    
                } // end et mt
                if (ch::contains({"tt"}, chn)) {
                    
                    cb.cp().channel({chn}).bin_id({20}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_20_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"20.root");
                    cb.cp().channel({chn}).bin_id({21}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_21_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"21.root");
                    cb.cp().channel({chn}).bin_id({22}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_22_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"22.root");
                    cb.cp().channel({chn}).bin_id({23}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_23_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"23.root");
                    cb.cp().channel({chn}).bin_id({24}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_24_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"24.root");
                    cb.cp().channel({chn}).bin_id({25}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_25_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"25.root");
		    //                    cb.cp().channel({chn}).bin_id({16}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/"+chn+"/"+mmm+ "/htt_"+chn+"_16_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"16.root");
                        
                        
                    cb.cp().channel({chn}).bin_id({20}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_20_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"20.root");
                    cb.cp().channel({chn}).bin_id({21}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_21_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"21.root");
                    cb.cp().channel({chn}).bin_id({22}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_22_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"22.root");
                    cb.cp().channel({chn}).bin_id({23}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_23_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"23.root");
                    cb.cp().channel({chn}).bin_id({24}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_24_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"24.root");
                    cb.cp().channel({chn}).bin_id({25}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_25_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"25.root");
		    //                    cb.cp().channel({chn}).bin_id({16}).mass({"$MASS", "*"}).WriteDatacard(output_prefix + output_folder +"/cmb/"+mmm+ "/htt_"+chn+"_16_13TeV.txt", output_prefix + output_folder +"/"+chn+ "/common/htt_input"+chn+"16.root");
                } // end tt
            } // end CR
        }
    }
    
    // This part is required in case we need to have limit for each separted categories
    // For all categories want to include control regions. This will
    // work even if the extra categories aren't there.
    //    writer.WriteCards("htt_cmb_1_13TeV", cb.cp().bin_id({1,10,13}));
    //    writer.WriteCards("htt_cmb_2_13TeV", cb.cp().bin_id({2,10,13}));
    //    writer.WriteCards("htt_cmb_3_13TeV", cb.cp().bin_id({3,11,14}));
    //    writer.WriteCards("htt_cmb_4_13TeV", cb.cp().bin_id({4,11,14}));
    //    writer.WriteCards("htt_cmb_5_13TeV", cb.cp().bin_id({5,12,15}));
    //    writer.WriteCards("htt_cmb_6_13TeV", cb.cp().bin_id({6,12,15}));
    
    //
    //
    //
    //
    //    set<string> bins = cb.cp().channel({"mt","mm"}).bin_id({1,10,13}).bin_set();
    //    std::set<string>::iterator it;
    //    for (it=bins.begin(); it!=bins.end(); ++it){
    //        std::cout << " ==================>>>>>>>>   " << *it<<"\n\n\n\n";   //htt_et_10_13TeV
    //    }
    
    
    
    cb.PrintAll();
    cout << " done\n";
    cout << "\n\n" << "Yurii sanity check" << endl;
    
}
