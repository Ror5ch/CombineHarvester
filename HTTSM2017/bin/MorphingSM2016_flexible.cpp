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
#include "CombineHarvester/HTTSM2017/interface/HttSystematics_SMRun2_ggHMELA_rw.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"
#include "TF1.h"
#include "TKey.h"
#include "TFile.h"
#include "TROOT.h"

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
  string vbfcateStr_tt="tt_vbf_ggHMELA_bin";
  string vbfcateStr_mt="mt_vbf_ggHMELA_bin";
  string vbfcateStr_et="et_vbf_ggHMELA_bin";
  string vbfcateStr_em="em_vbf_ggHMELA_bin";
  bool auto_rebin = false;
  bool manual_rebin = false;
  bool real_data = false;
  int control_region = 0;
  string year = "2016";
  bool check_neg_bins = false;
  bool poisson_bbb = false;
  bool do_w_weighting = false;
  bool mm_fit = false;
  bool ttbar_fit = false;
  bool do_jetfakes = true;
  bool do_embedded = true;
  bool do_shapeSyst = false;
  bool do_sync = false;
  bool useSingleVBFdir = false;
  string do_chn = "tt";
  bool is_2017 = false;
  bool use_ggHint = false;
  string par = "fa3";
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
    ("vbfcateStr_tt", po::value<string>(&vbfcateStr_tt)->default_value("tt_vbf_ggHMELA_bin"))
    ("vbfcateStr_mt", po::value<string>(&vbfcateStr_mt)->default_value("mt_vbf_ggHMELA_bin"))
    ("auto_rebin", po::value<bool>(&auto_rebin)->default_value(false))
    ("real_data", po::value<bool>(&real_data)->default_value(false))
    ("manual_rebin", po::value<bool>(&manual_rebin)->default_value(false))
    ("output_folder", po::value<string>(&output_folder)->default_value("sm_run2"))
    ("SM125,h", po::value<string>(&SM125)->default_value(SM125))
    ("control_region", po::value<int>(&control_region)->default_value(0))
    ("year", po::value<string>(&year)->default_value("2016"))
    ("mm_fit", po::value<bool>(&mm_fit)->default_value(true))
    ("ttbar_fit", po::value<bool>(&ttbar_fit)->default_value(true))
    ("jetfakes", po::value<bool>(&do_jetfakes)->default_value(false))
    ("embedded", po::value<bool>(&do_embedded)->default_value(false))
    ("shapeSyst", po::value<bool>(&do_shapeSyst)->default_value(false))
    ("sync", po::value<bool>(&do_sync)->default_value(false))
    ("useSingleVBFdir", po::value<bool>(&useSingleVBFdir)->default_value(false))
    ("chn", po::value<string>(&do_chn)->default_value("tt"))
    ("par", po::value<string>(&par)->default_value("fa3"))
    ("is2017", po::value<bool>(&is_2017)->default_value(false))
    ("use_ggHint", po::value<bool>(&use_ggHint)->default_value(false))
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
  
  VString chns = {"mt","et","tt","em"};
  //VString chns = {"tt"};
  if (do_chn!="all"){
    chns.clear();
    chns.push_back(do_chn);
  }
  
  
  
  if (mm_fit) chns.push_back("mm");
  if (ttbar_fit) chns.push_back("ttbar");
  
  
  map<string, VString> bkg_procs;
  if (do_jetfakes && do_embedded ){
    //bkg_procs["em"] = {"embedded", "W", "QCD", "ZLL", "TT", "VV", "EWKZ","ZJ"};
    //bkg_procs["em"] = {"embedded", "W", "QCD", "ZLL", "TT", "VV","hww125"};
    //bkg_procs["em"] = {"embedded", "W", "QCD", "ZLL", "TT", "VV"};
    
    bkg_procs["em"] = {"embedded", "W", "QCD", "ZLL", "TT", "VV", "ggH_hww125", "qqH_hww125","VH_hww125"};
    //bkg_procs["em"] = {"embedded", "W", "QCD", "ZLL", "TT", "VV","JJHiggs_hww125_a1", "VBFHiggs_hww125_a1","VH_hww125"};
    //bkg_procs["em"] = {"embedded", "W", "QCD", "ZLL", "TT", "VV","JJHiggs_hww125_a3", "VBFHiggs_hww125_a3","VH_hww125"};

    //bkg_procs["em"] = {"embedded", "W", "QCD", "ZLL", "TT", "VV", "EWKZ"};
    bkg_procs["et"] = {"embedded", "ZL", "TTT", "VVT", "jetFakes", "STT", "STL", "TTL", "VVL", "ggH_hww125", "qqH_hww125","ZH_hww125","WH_hww125"};
    bkg_procs["mt"] = {"embedded", "ZL", "TTT", "VVT", "jetFakes", "STT", "STL", "TTL", "VVL", "ggH_hww125", "qqH_hww125","ZH_hww125","WH_hww125"};
    bkg_procs["tt"] = {"embedded", "ZL", "TTL", "VVL", "jetFakes"};
    //bkg_procs["tt"] = {"embedded", "ZL", "TTT", "VVT", "jetFakes"};
  } else if (do_embedded && !do_jetfakes ) {
    bkg_procs["et"] = {"embedded", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
    bkg_procs["mt"] = {"embedded", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
    bkg_procs["tt"] = {"embedded", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
  } else if (!do_embedded && do_jetfakes ) {
    bkg_procs["em"] = {"ZTT", "W", "QCD", "ZLL", "TT", "VV", "EWKZ","ZJ"};
    //bkg_procs["et"] = {"ZTT", "EWKZ", "ZL", "TTT", "VVT", "jetFakes"};
    bkg_procs["et"] = {"ZTT", "ZL", "TTT", "VVT", "jetFakes"};      
    //bkg_procs["mt"] = {"ZTT", "EWKZ", "ZL", "TTT", "VVT", "jetFakes"};
    bkg_procs["mt"] = {"ZTT", "ZL", "TTT", "VVT", "jetFakes"};
    //bkg_procs["tt"] = {"ZTT", "EWKZ", "ZL", "TTT", "VVT", "jetFakes"};
    bkg_procs["tt"] = {"ZTT", "EWKZ", "ZL", "TTL","TTT","VVL", "VVT", "jetFakes"};
  } else if (!do_embedded && !do_jetfakes ) {
    bkg_procs["em"] = {"ZTT", "W", "QCD", "ZLL", "TT", "VV", "EWKZ","ZJ"};	
    bkg_procs["et"] = {"ZTT", "EWKZ", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
    bkg_procs["mt"] = {"ZTT", "EWKZ", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
    //bkg_procs["mt"] = {"ZTT", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
    bkg_procs["tt"] = {"ZTT", "EWKZ", "ZL", "TTT", "VVT", "VVJ", "TTJ", "ZJ", "W", "QCD"};
  } else {
    std::cout << "This shold not have happened !" << std::endl;
    return -1;
  }

  
  // ym this needs to be updated
  //bkg_procs["em"] = {"ZTT", "W", "QCD", "ZL", "TT", "VV", "EWKZ", "ggH_hww125", "qqH_hww125"};
  //bkg_procs["em"] = {"ZTT", "W", "QCD", "ZLL", "TT", "VV", "EWKZ"};
  bkg_procs["mm"] = {"W", "ZL", "TT", "VV"};
  bkg_procs["ttbar"] = {"ZTT", "W", "QCD", "ZL", "TT", "VV", "EWKZ"};
  
  
  
  ch::CombineHarvester cb;
  
  
  
  map<string,Categories> cats;
  cats["em"] = {
    {1, "em_0jet"},
    {2, "em_boosted"},
    {3, "em_vbf_ggHMELA_bin1"},
    {4, "em_vbf_ggHMELA_bin2"},
    {5, "em_vbf_ggHMELA_bin3"},
    {6, "em_vbf_ggHMELA_bin4"}
  };
  
  cats["et"] = {
    {1, "et_0jet"},
    {2, "et_boosted"},
    {3, "et_vbf_ggHMELA_bin1"},
    {4, "et_vbf_ggHMELA_bin2"},
    {5, "et_vbf_ggHMELA_bin3"},
    {6, "et_vbf_ggHMELA_bin4"}
  };
  
  cats["mt"] = {
    {1, "mt_0jet"},
    {2, "mt_boosted"},
    {3, "mt_vbf_ggHMELA_bin1"},
    {4, "mt_vbf_ggHMELA_bin2"},
    {5, "mt_vbf_ggHMELA_bin3"},
    {6, "mt_vbf_ggHMELA_bin4"}
  };
  
  
  
  int tt_cate_count =2;
  int mt_cate_count =2;
  int et_cate_count =2;
  int em_cate_count =2;
  
  for (auto chn : chns){
    if (ch::contains({"tt"}, chn)) {
      
      Categories tt_cate;
      tt_cate.push_back(make_pair(1,"tt_0jet"));
      tt_cate.push_back(make_pair(2,"tt_boosted"));
      TString fname_tt = input_dir["tt"] + "htt_tt.inputs-sm-13TeV_"+year+postfix+".root";
      TFile *ftemp_tt = new TFile( fname_tt);
      TIter next_tt(ftemp_tt->GetListOfKeys());
      TKey *key_tt;
      //tt_cate_count =2;
      while ((key_tt = (TKey*)next_tt())) {
	TClass *cl = gROOT->GetClass(key_tt->GetClassName());
	if (!cl->InheritsFrom("TDirectory")) continue;
	TString keyname = key_tt->GetName();
	if(keyname.Contains(vbfcateStr_tt)){
	  tt_cate_count++;
	  tt_cate.push_back(make_pair(tt_cate_count,keyname.Data()));
	  cout << " testing" ;
	  //cout << " ==========================================> tt cat: "<< make_pair(tt_cate_count,keyname.Data());
	}
      }
      cats["tt"] = {
	tt_cate
      };
    }
    
    else if (ch::contains({"mt"}, chn)) {
      
      Categories mt_cate;
      mt_cate.push_back(make_pair(1,"mt_0jet"));
      mt_cate.push_back(make_pair(2,"mt_boosted"));
      TString fname_mt = input_dir["mt"] + "htt_mt.inputs-sm-13TeV_"+year+postfix+".root";
      TFile *ftemp_mt = new TFile( fname_mt);
      TIter next_mt(ftemp_mt->GetListOfKeys());
      TKey *key_mt;
      //tt_cate_count =2;
      while ((key_mt = (TKey*)next_mt())) {
	TClass *cl = gROOT->GetClass(key_mt->GetClassName());
	if (!cl->InheritsFrom("TDirectory")) continue;
	TString keyname = key_mt->GetName();
	//if(keyname.Contains(vbfcateStr_mt) and (keyname.Contains("bin1") or keyname.Contains("bin2") or keyname.Contains("bin3") or keyname.Contains("bin4") or keyname.Contains("bin5") ) and not (keyname.Contains("bin10") or  keyname.Contains("bin11") or keyname.Contains("bin12")) ){ // when using 5 MELA_D0 bins
        if(keyname.Contains(vbfcateStr_mt) and (keyname.Contains("bin1") or keyname.Contains("bin2") or keyname.Contains("bin3") or keyname.Contains("bin4") ) and not (keyname.Contains("bin10") or  keyname.Contains("bin11") or keyname.Contains("bin12")) ){ // nominal
	  mt_cate_count++;
	  mt_cate.push_back(make_pair(mt_cate_count,keyname.Data()));
	  cout << " ++++++++.........     adding "<<keyname <<" -> " <<keyname.Data() ;
	  //cout << " ==========================================> tt cat: "<< make_pair(tt_cate_count,keyname.Data());
	}
      }
      cats["mt"] = {
	mt_cate
      };
    }
    
    else if (ch::contains({"et"}, chn)) {
      
      Categories et_cate;
      et_cate.push_back(make_pair(1,"et_0jet"));
      et_cate.push_back(make_pair(2,"et_boosted"));
      TString fname_et = input_dir["et"] + "htt_et.inputs-sm-13TeV_"+year+postfix+".root";
      TFile *ftemp_et = new TFile( fname_et);
      TIter next_et(ftemp_et->GetListOfKeys());
      TKey *key_et;
      //tt_cate_count =2;
      while ((key_et = (TKey*)next_et())) {
	TClass *cl = gROOT->GetClass(key_et->GetClassName());
	if (!cl->InheritsFrom("TDirectory")) continue;
	TString keyname = key_et->GetName();
	if(keyname.Contains(vbfcateStr_et) and (keyname.Contains("bin1") or keyname.Contains("bin2") or keyname.Contains("bin3") or keyname.Contains("bin4") ) and not (keyname.Contains("bin10") or  keyname.Contains("bin11") or keyname.Contains("bin12"))  ){
	  et_cate_count++;
	  et_cate.push_back(make_pair(et_cate_count,keyname.Data()));
	  cout << " testing adding cat: "<<keyname.Data() ;
	  //cout << " ==========================================> tt cat: "<< make_pair(tt_cate_count,keyname.Data());
	}
      }
      cats["et"] = {
	et_cate
      };
    }
    
    else if (ch::contains({"em"}, chn)) {
      
      Categories em_cate;
      em_cate.push_back(make_pair(1,"em_0jet"));
      em_cate.push_back(make_pair(2,"em_boosted"));
      TString fname_em = input_dir["em"] + "htt_em.inputs-sm-13TeV_"+year+postfix+".root";
      TFile *ftemp_em = new TFile( fname_em);
      TIter next_em(ftemp_em->GetListOfKeys());
      TKey *key_em;
      //tt_cate_count =2;
      while ((key_em = (TKey*)next_em())) {
	TClass *cl = gROOT->GetClass(key_em->GetClassName());
	if (!cl->InheritsFrom("TDirectory")) continue;
	TString keyname = key_em->GetName();
	if(keyname.Contains(vbfcateStr_em) and (keyname.Contains("bin1") or keyname.Contains("bin2") or keyname.Contains("bin3") or keyname.Contains("bin4")  or keyname.Contains("bin5") or keyname.Contains("bin6") or keyname.Contains("bin7") or keyname.Contains("bin8")) ){
	  em_cate_count++;
	  em_cate.push_back(make_pair(em_cate_count,keyname.Data()));
	  cout << " testing" ;
	  //cout << " ==========================================> tt cat: "<< make_pair(tt_cate_count,keyname.Data());
	}
      }

      cats["em"] = {
	em_cate
      };
        // for single VBF dir (for sync)
        if (do_sync or useSingleVBFdir){
                cats["em"] = {
                        {1, "em_0jet"},
                        {2, "em_boosted"},
                        {3, "em_vbf"}
                };
        }


    }

 // comment when using DCP bins!	
 /*
    if (do_sync){
      cats["mt"] = {
	{1, "mt_0jet"},
	{2, "mt_boosted"},
      {3, "mt_vbf"}
      };
    }
*/
    
    
    
  }
  
  
  
  vector<string> sig_procs = {"GGH2Jets_sm_M","reweighted_WH_htt_0PM","reweighted_ZH_htt_0PM","reweighted_qqH_htt_0PM","reweighted_qqH_htt_0M","reweighted_ZH_htt_0M","reweighted_WH_htt_0M","reweighted_qqH_htt_0Mf05ph0","reweighted_ZH_htt_0Mf05ph0","reweighted_WH_htt_0Mf05ph0"};
  // FIXME: missing int histos in tt:
  vector<string> sig_procs_tt = {"GGH2Jets_sm_M","GGH2Jets_pseudoscalar_M","reweighted_WH_htt_0PM","reweighted_ZH_htt_0PM","reweighted_qqH_htt_0PM","reweighted_qqH_htt_0M","reweighted_ZH_htt_0M","reweighted_WH_htt_0M"};
  
  if (par=="fa3"){
    sig_procs.push_back("GGH2Jets_pseudoscalar_M");
    sig_procs_tt.push_back("GGH2Jets_pseudoscalar_M");
  }
  
/*
  if (use_ggHint and par=="fa3"){
    sig_procs.push_back("GGH2Jets_pseudoscalar_Mf05ph0");
    sig_procs_tt.push_back("GGH2Jets_pseudoscalar_Mf05ph0");
    
  }
*/
  if (do_sync){
    //bkg_procs["mt"] = {"embed", "ZL", "TTT", "VVT", "jetFakes","EWKZ"}; // Danny
    bkg_procs["mt"] = {"embed", "ZL", "TTT", "VVT", "jetFakes"}; // Tyler
    bkg_procs["et"] = {"embed", "ZL", "TTT", "VVT", "jetFakes"}; // Tyler
    bkg_procs["em"] = {"embed", "W","QCD","ZLL","TT","VV","EWKZ"}; // Tyler
    //sig_procs = {"reweighted_ggH_htt_0M","reweighted_ggH_htt_0PM","reweighted_WH_htt_0PM","reweighted_ZH_htt_0PM","reweighted_qqH_htt_0PM","reweighted_qqH_htt_0M","reweighted_ZH_htt_0M","reweighted_WH_htt_0M","reweighted_qqH_htt_0Mf05ph0","reweighted_ZH_htt_0Mf05ph0","reweighted_WH_htt_0Mf05ph0"};
    sig_procs = {"GGH2Jets_sm_M","GGH2Jets_pseudoscalar_M","reweighted_WH_htt_0PM","reweighted_ZH_htt_0PM","reweighted_qqH_htt_0PM","reweighted_qqH_htt_0M","reweighted_ZH_htt_0M","reweighted_WH_htt_0M","reweighted_qqH_htt_0Mf05ph0","reweighted_ZH_htt_0Mf05ph0","reweighted_WH_htt_0Mf05ph0"};
  }

  if (use_ggHint and par=="fa3"){
    sig_procs.push_back("GGH2Jets_pseudoscalar_Mf05ph0");
} 
 
  vector<string> sig_procs_ttbar = {"GGH2Jets_sm_M","reweighted_WH_htt_0PM","reweighted_ZH_htt_0PM","reweighted_qqH_htt_0PM"};
  
  vector<string> masses = {"125"};
  
  using ch::syst::bin_id;
  
  //! [part2]
  for (auto chn : chns) {
    cb.AddObservations({"*"}, {"htt"}, {year}, {chn}, cats[chn]);
    cb.AddProcesses(   {"*"}, {"htt"}, {year}, {chn}, bkg_procs[chn], cats[chn], false);
    cb.AddProcesses(masses,   {"htt"}, {year}, {chn}, sig_procs, cats[chn], true);
  }
  
  // if (year=="2018") is_2017=true;
  // ch::AddSMRun2Systematics_ggHMELA_rw(cb,tt_cate_count,mt_cate_count, control_region, do_shapeSyst, is_2017,  mm_fit, ttbar_fit);
  ch::AddSMRun2Systematics_ggHMELA_rw(cb,tt_cate_count,mt_cate_count, control_region, do_shapeSyst, std::stoi(year),  mm_fit, ttbar_fit);
  
  
  
  //! [part7]
  for (string chn:chns){
    cout << " &&&&&&&& creating root files for ch: "<< chn << "\n";
    cb.cp().channel({chn}).backgrounds().ExtractShapes(
						       input_dir[chn] + "htt_"+chn+".inputs-sm-13TeV_"+year+postfix+".root",
						       "$BIN/$PROCESS",
						       "$BIN/$PROCESS_$SYSTEMATIC");
    if(chn != std::string("ttbar")){
      cout << "           -> it is not ttbar so take also signal shapes..\n";
      cb.cp().channel({chn}).process(sig_procs).ExtractShapes(
							      input_dir[chn] + "htt_"+chn+".inputs-sm-13TeV_"+year+postfix+".root",
							      "$BIN/$PROCESS$MASS",
							      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
    }
    else{
      cout << "           -> it IS ttbar so take also signal shapes..\n";
      cb.cp().channel({chn}).process(sig_procs_ttbar).ExtractShapes(
								    input_dir[chn] + "htt_"+chn+".inputs-sm-13TeV_"+year+postfix+".root",
								    "$BIN/$PROCESS$MASS",
								    "$BIN/$PROCESS$MASS_$SYSTEMATIC");
    }
  }
  
  
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
  
  cb.cp().FilterSysts(BinIsNotControlRegion).syst_type({"shape"}).ForEachSyst([](ch::Systematic *sys) {
      sys->set_type("lnN");
    });

  
  ///////// START
 
  // auto rebin = ch::AutoRebin()
  //   .SetBinUncertFraction(0.5);
  //   //.SetBinThreshold(0.);
  // rebin.Rebin(cb.cp().channel({"em","et","mt"}), cb);

  auto rebin_etmt = ch::AutoRebin().SetBinUncertFraction(0.5);
  rebin_etmt.Rebin(cb.cp().channel({"et","mt"}), cb);

  auto rebin_em = ch::AutoRebin().SetBinUncertFraction(0.5);
  rebin_em.Rebin(cb.cp().channel({"em"}), cb);

  //rebin.Rebin(cb.cp().channel({"mt"}), cb);
  //rebin.Rebin(cb.cp().process({"embedded"}).channel({"em"}), cb);
  //rebin.Rebin(cb.cp().process({"GGH2Jets_sm_M"}).channel({"em"}), cb);

  ///////// END

  
  auto bbb = ch::BinByBinFactory()
    .SetAddThreshold(0.05)
    .SetMergeThreshold(0.8)
    .SetFixNorm(false);
  bbb.MergeBinErrors(cb.cp().backgrounds());
  // uncomment below! SD
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
  
  ch::SetStandardBinNames(cb);
  
  cb.SetGroup("all", {".*"});
  cb.SetGroup("nonThySyst", {".*"});
  
  string output_prefix = "output/";
  if(output_folder.compare(0,1,"/") == 0) output_prefix="";
  //ch::CardWriter writer(output_prefix + output_folder + "/$TAG/$MASS/$BIN.txt",
  //		output_prefix + output_folder + "/$TAG/common/htt_input.root");
  ch::CardWriter writer(output_prefix + output_folder + "/$TAG/$MASS/$BIN.txt",
			output_prefix + output_folder + "/$TAG/common/htt_input_"+year+".root");

  writer.SetVerbosity(3);
  
  writer.WriteCards("cmb", cb);
  for (auto chn : chns) {
    if(chn == std::string("mm"))
      {
	continue;
      }
    // per-channel
    writer.WriteCards(chn, cb.cp().channel({chn, "mm"}));
    writer.WriteCards("htt_"+chn+"_1_"+year, cb.cp().channel({chn}).bin_id({1}));
    writer.WriteCards("htt_"+chn+"_2_"+year, cb.cp().channel({chn}).bin_id({2}));
    writer.WriteCards("htt_"+chn+"_3_"+year, cb.cp().channel({chn}).bin_id({3}));
    writer.WriteCards("htt_"+chn+"_4_"+year, cb.cp().channel({chn}).bin_id({4}));
    writer.WriteCards("htt_"+chn+"_5_"+year, cb.cp().channel({chn}).bin_id({5}));
    writer.WriteCards("htt_"+chn+"_6_"+year, cb.cp().channel({chn}).bin_id({6}));
    writer.WriteCards("htt_"+chn+"_7_"+year, cb.cp().channel({chn}).bin_id({7}));
    
    
    
  }
  
  
  //cb.PrintAll();
  cout << " done\n";
  cout << "\n\n" << "Kyungwook sanity check" << endl;
  
}
