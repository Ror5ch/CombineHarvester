# CombineHarvester

Full documentation: http://cms-analysis.github.io/CombineHarvester

## Quick start

This pacakge requires HiggsAnalysis/CombinedLimit to be in your local CMSSW area. We follow the release recommendations of the combine developers which can be found [here](https://cms-hcomb.gitbooks.io/combine/content/part1/#for-end-users-that-dont-need-to-commit-or-do-any-development). The CombineHarvester framework is  compatible with the CMSSW 7_4_X and 8_1_X series releases.

A new full release area can be set up and compiled in the following steps:

    cmsrel CMSSW_8_1_0
    cd CMSSW_8_1_0/src
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    git clone -b lt_chn ssh://git@gitlab.cern.ch:7999/KState-HEP-HTT/CombineHarvester.git CombineHarvester
    scram b

Copy the singal models from /hdfs/store/user/senka/HTT_2016and2017/signalModels/* to HiggsAnalysis/CombinedLimit/python.

    cp /hdfs/store/user/senka/HTT_2016and2017/signalModels/* HiggsAnalysis/CombinedLimit/python/.


## Do AC

First normalize your JHU samples to Powheg yield and do appropriate histo renaming:

    python CombineHarvester/HTTSM2017/scripts/normToPowheg.py <input datacard> <output datacard> <ch>

Now Unroll 2D distributions to 1D distribution:

    python CombineHarvester/HTTSM2017/scripts/Unroll_2Drelaxed_FF.py <input datacard> <ch> <outName>

if you want to use shape systematics then add "-y True":

    python CombineHarvester/HTTSM2017/scripts/Unroll_2Drelaxed_FF.py <input datacard> <ch> <outName> -y True


Now move the resulting datacard to CombineHarvester/HTTAC2017/shapes/USCMS/. Copy the singal models from /hdfs/store/user/senka/HTT_2016and2017/signalModels/* to HiggsAnalysis/CombinedLimit/python.
Setup for limit setting (et and tt channels):

    cp <unrolled datacard> CombineHarvester/HTTAC2017/shapes/USCMS/.
    cp /hdfs/store/user/senka/HTT_2016and2017/signalModels/* HiggsAnalysis/CombinedLimit/python/.

To use MELA_VBF bins:

    MorphingSM2016_D0merged_DCP_ggHSyst_rw --output_folder="data_embedded_noStst_AC" --postfix="-2D" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false --embedded=true  --jetfakes=true
    cd output/data_embedded_noStst_AC
    combineTool.py -M T2W -i {cmb,et,tt}/* -o workspace.root --parallel 18
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.HVV_fa3_withInt_ggH_fa3_withInt_rw:HVV_fa3_withInt_ggH_fa3_withInt_rw -i et/125/combined.txt.cmb -o fa03_Workspace_MengsMuV_et.root
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.HVV_fa3_withInt_ggH_fa3_withInt_rw:HVV_fa3_withInt_ggH_fa3_withInt_rw -i tt/125/combined.txt.cmb -o fa03_Workspace_MengsMuV_tt.root


or to use MELA_ggH bins (flexi bins for tt and mt channels) (use --shapeSyst=false if not using shapeSyst, use --is2017=true if running 2017):

    MorphingSM2016_flexible --output_folder="data_embedded_noStst_AC" --postfix="-2D" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false --embedded=true  --jetfakes=true --shapeSyst=true
    cd output/data_embedded_noStst_AC
    combineTool.py -M T2W -i {cmb,et,tt}/* -o workspace.root --parallel 18
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.HVV_fa3_withInt_ggH_fa3_withInt_rw:HVV_fa3_withInt_ggH_fa3_withInt_rw -i et/125/combined.txt.cmb -o fa03_Workspace_MengsMuV_et.root
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.HVV_fa3_withInt_ggH_fa3_withInt_rw:HVV_fa3_withInt_ggH_fa3_withInt_rw -i tt/125/combined.txt.cmb -o fa03_Workspace_MengsMuV_tt.root


Runing limits:
Scan fa3_VBF (et channel):

    combineTool.py -n 1D_scan_fa3_VBF -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-1.,1. et/125/fa03_Workspace_MengsMuV_et.root --algo=grid --points=51 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1
Scan fa3_VBF w/o syst (et channel):

    combineTool.py -n 1D_scan_fa3_VBF_S0 -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-1.,1. et/125/fa03_Workspace_MengsMuV_et.root --algo=grid --points=51 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1 -S 0
Scan fa3_ggH (et channel):

    combineTool.py -n 1D_scan_fa3_ggH -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-1.,1. et/125/fa03_Workspace_MengsMuV_et.root --algo=grid --points=51 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P fa3_ggH --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1
Scan fa3_ggH w/o syst (et channel):

    combineTool.py -n 1D_scan_fa3_ggH_S0 -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-1.,1. et/125/fa03_Workspace_MengsMuV_et.root --algo=grid --points=51 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P fa3_ggH --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1 -S 0

## Using muVmuF for SM with MG samples:

    MorphingSM2016_dataDriven_rw_SM --output_folder="data_muVmuF" --postfix="-2D" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false --embedded=true  --jetfakes=true
    cd output/data_muVmuF
    combineTool.py -M T2W -i {tt}/* -o workspace.root --parallel 18
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.muVmuF_SM:muVmuF_SM -i tt/125/combined.txt.cmb -o muVmuF_Workspace_tt.root

## Check signal model in every bin using input histograms:

Using datacard as input check to make sure signal model (ggH and VBF) does not have bins with negative yield. Writes out info for the bins where signal model is negative.
Signal model is checked for several predefined fa3_ggH and fa3_VBF points.
Can use ggH signal model with (using "-g 0" option) or without (using "-g 1" option) interefrence. 
For running define the channel ("-c tt" for tautau). If you want to see yield in every bin run in verbose mode ("-p 1" option). 
Example for tautau channel:
    

    python HTTSM2017/scripts/checkSignal.py -i ./HTTAC2017/shapes/USCMS/htt_tt.inputs-sm-13TeV-2D_tt2016_baseline-with-msv_Meng_vbfTrain_NOtoss.root -o tests.root -g 1 -c tt
    
# Signal model

Signal model defines the signal definition and describes how the signal depends on the POI (parameter of interest).
There are several signal models that have been used in HVV and ggH analysis. 

## muVmuF signal model (muVmuF.py)

This signal model does NOT contain anomalous couplings, only SM couplings are included. POI's are muV and muf. muV is the scaling factor affecting HVV couplings, 
so VBF and VH production. muf is the scaling factor affecting ggH couplings, so ggH production. The total signal model is: muV*(VBF+VH) and muf*(ggH).

    combineTool.py -M T2W -m 125 -P CombineHarvester.HTTSM2017.muVmuF:muVmuF -i tt/125/combined.txt.cmb -o muVmuF_Workspace_tt.root
    
## r signal model (mu_SM.py)

This signal model does NOT contain anomalous couplings, only SM couplings are included. POI is mu. mu is the scaling factor affecting all higgs couplings, HVV and ggH. 
mu is the scaling factor affecting ggH, VH and VBF production. The total signal model is: mu*(VBF+VH+ggH).

    combineTool.py -M T2W -m 125 -P CombineHarvester.HTTSM2017.mu_SM:mu_SM -i tt/125/combined.txt.cmb -o mu_Workspace_tt.root

## Anomalous coupling signal model with ggH interference (HVV_fa3_withInt_ggH_fa3_withInt_rw.py)

This signal model does contain anomalous HVV and ggH couplings. POIs are muV, muf, fa3_ggH and CMS_zz4l_fai1(=fa3_HVV). muV is the scaling factor affecting HVV couplings, 
so VBF and VH production. muf is the scaling factor affecting ggH couplings, so ggH production. fa3_ggH is the ggH PS fa3 parameter and CMS_zz4l_fai1 
is the HVV PS fa3 parameter. Interference between SM and PS for both HVV and ggH is included. 
Input histograms are SM, PS and maxmix for each process (ggH, VBF, WH, ZH). The signal model for each process in any point in parameter space is a function
of fa parameter and all three input histograms.  SM corresponds to muV=1, muf=1, fa3_ggH=0 and CMS_zz4l_fai1=0.

    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.HVV_fa3_withInt_ggH_fa3_withInt_rw:HVV_fa3_withInt_ggH_fa3_withInt_rw -i tt/125/combined.txt.cmb -o fa03_Workspace_Int_tt.root

## Anomalous coupling signal model without ggH interference (HVV_fa3_withInt_ggH_fa3_woInt_rw.py)

This signal model does contain anomalous HVV and ggH couplings. POIs are muV, muf, fa3_ggH and CMS_zz4l_fai1(=fa3_HVV). muV is the scaling factor affecting HVV couplings, 
so VBF and VH production. muf is the scaling factor affecting ggH couplings, so ggH production. fa3_ggH is the ggH PS fa3 parameter and CMS_zz4l_fai1
is the HVV PS fa3 parameter. Interference between SM and PS for HVV is included. Interference in ggH is NOT included. 
Input histograms are SM, PS and maxmix for VBF, WH and ZH processes. Input histograms for ggH proces are only SM and PS The signal model for each process in any point in parameter space is a function
of fa parameter and all three (two) input histograms for HVV and ggH production. SM corresponds to muV=1, muf=1, fa3_ggH=0 and CMS_zz4l_fai1=0.

    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.HVV_fa3_withInt_ggH_fa3_woInt_rw:HVV_fa3_withInt_ggH_fa3_woInt_rw -i tt/125/combined.txt.cmb -o fa03_Workspace_woggHInt_tt.root


## How to read a signal model in workspace

One can check the signal model directly in the workspace. Relevant objects: "ModelConfig_POI" objects are POIs, "model_s" is the signal+bkg model, "model_b" is the bkg model,
"n_exp_binhtt_*_13TeV_proc_reweighted_*_htt_*M" are relevant contributions for signal model.

    root tt/125/fa03_Workspace_Int_tt.root
    gSystem->Load("libHiggsAnalysisCombinedLimit")   
    w->Print()
    w->cd()
    # get parameter values:
    fa3_ggH->getVal()
    # set parameter values:
    fa3_ggH->setVal(1.0)
    # get ggH components:
    n_exp_binhtt_tt_3_13TeV_proc_GGH2Jets_sm_M->getVal()
    n_exp_binhtt_tt_3_13TeV_proc_GGH2Jets_pseudoscalar_M->getVal()
 
## The code description (September 2020)

### 1) Renaming for fa2/fL1/fL1Zg
   This is the code that simply renames signal fa2/fL1/fL1Zg histograms to the same names as fa3 signal histograms have. This is done so that 
   we can use the same Morphing and Syst (takes long time to compile anyway) script for all coupling scenarios. 
   It needs to be run before normToPowheg script. It creased a renamed datacard with name "input_datacard_renamed.root". 

    python HTTSM2017/scripts/rename_HVV_histos.py --par={par} --input=input_datacard.root
    
   {par}=fa2/fL1/fL1Zg/fa3. Script does not rename for fa3 case.    

### 2) Normalize to Powheg
   This code rescales JHU SM histograms to have the same yield as Powheg for each category (0jet/boosted/VBF). This is done for VBF, WH and ZH processes.
   The scaling is done by applying the ratios of (Powheg_yield)/(JHU_SM_yield) to all JHU histograms. So BSM histograms are also scaled with the same ratio.

    python HTTSM2017/scripts/normToPowheg.py input_datacard.root output_datacard.root {chn} {year} {useDCP} {par}   
   
   {par}=fa2/fL1/fL1Zg/fa3, {year}=2016/2017/2018, {useDCP}=0/1, {chn}=tt/mt/et/em.
   
### 3) DCP bins
   We use two DCP bins for fa3 measurements. The VBF/ggH maxmix signal is anti-symmetic in DCP(VBF/ggH) observable, and all other processes are symmetric.
   This information is used in the analysis. Corresponding symmetrization and anti-symmetrization is done in the code.
   

    python Symmetrize_DCP.py input_datacard.root

   The code produces new datacard "input_datacard_DCPsym.root". 
   Other then the symmetrization of the histograms we also need to make sure that the stat uncertainties are correlated between DCP bins. This is done
   by adding these lines of code into the nominal BinByBin [code](https://gitlab.cern.ch/KState-HEP-HTT/CombineHarvester/blob/master/CombineTools/src/BinByBin.cc#L179-186).
   This correlation of stat uncertainties can not be done using the automatic Combine tool (using "autoMCStats" in the txt datacard).
   
### 4) Morphing
   This is the code that prepares txt datacards and corresponding root files for each category. It uses the shape systematics defined [here](https://gitlab.cern.ch/KState-HEP-HTT/CombineHarvester/blob/master/HTTSM2017/src/HttSystematics_SMRun2_ggHMELA_rw.cc)
   and also the BinByBin uncertainties defined [here](https://gitlab.cern.ch/KState-HEP-HTT/CombineHarvester/blob/master/CombineTools/src/BinByBin.cc). 

    MorphingSM2016_flexible --output_folder="data_{inputString}_mergedBins_withSyst_MELAVBF" --postfix="-2D_MELAVBF_{inputString}_mergedBins" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false --embedded={emb} --jetfakes=true --shapeSyst=false --year={year} --chn={chn} --par={par}

### 5) Toy tossing
   To estimate the effect of stat fluctuations in templates on the limit we toss toys to create new signal template and then using this new templates 
   we rerun the full workflow. So first create new templates by tossing, then run nomToPowheg and all other steps. Tossing needs to be done before normToPowheg.
   The scirpt for tossing toys is [here](https://gitlab.cern.ch/KState-HEP-HTT/CombineHarvester/blob/master/HTTSM2017/scripts/TossToys_VBF.py), one can
   define which processes (histograms) to toss in [these lines](https://gitlab.cern.ch/KState-HEP-HTT/CombineHarvester/blob/master/HTTSM2017/scripts/TossToys_VBF.py#L37-38).
   Tossing is done by simple Gaussian with bin content (mu) and bin uncertainty (sigma) in every bin. To run the tossing:
   

    python HTTSM2017/scripts/TossToys_VBF.py input_datacard.root output_datacard_toss_1.root {chn}


   Simple shell script to run 30 toys and run limits:
   

    source run_optimizedBin_limits_toss.sh {chn} {year} 0 {datacard_name_string} 30

### 6) Impact plots
   Script to run impact plots for VBF:

    source run_impacts.sh {chn} {year}
    
   Script to run impact plots for ggH:

    source run_impacts_ggH.sh {chn} {year}
    
   Scripts need to be run from the dir where the outputs are, output/output_name. In case some of the fits for individual nuisance fail, [this step](https://gitlab.cern.ch/KState-HEP-HTT/CombineHarvester/blob/master/run_impacts.sh#L2) needs 
   to be resubmitted only for the failed nuisances. One can do that by adding "  --named failed_nuisance_1,failed_nuisance_2 ..." at the end. 

### 7) Unrolled plots
   Unrolled postfit plots are derived using the workspace as starting point. Postfit histograms, and uncertainties, are extracted from the workspace and then plotted.
   The histograms do not have the info about observables or bin edges, so these are hardcoded in the DrawUnrolled_Run2.py script. 
   Please make sure these correspond to the bin edges from the datacard.
   
   First get the needed histograms and uncertainties from the workspace (run from the CombineHarvester dir):
    
   for fa3_VBF:

    source make_postfit.sh {chn} {year} {datacard_string}
 
   for fa3_ggH:

    source make_postfit_ggH.sh {chn} {year} {datacard_string}

   Now plot the unrolled distribution:    

    python DrawUnrolled_Run2.py --variable {var} --channel {chn} --year {year} --isEmbed 1
    
   variable={a3_ggh/a3}

### 8) Combination across years

   The combination across years for a particular channel can be done using this script:

    python run_optimizedBin_limits_syst_combYears.py --chn={chn} --emb=1 --inputString={datacard_string} --useDCP={0/1} --par={par} --isGGH={0/1}

### 9) Combination across channels and years

   The combination across channels and years (overall combination):

    python run_optimizedBin_limits_syst_combinedYears_combChn.py --emb=1 --inputString={datacard_string} --par={par} --isGGH={0/1}



## Run all in one (September 2020)

Run for ggH/VBF/other_par:

    cd CombineHarvester/
    python run_optimizedBin_limits_noSyst.py --chn=tt --year=2018 --emb=1 --inputString=MANUAL_optBins_syst_par --useDCP=1 --par={par} --path_datacard={path_datacard} --name_datacard={name_datacard} --path_CMSSW94={path_CMSSW94} --isGGH={0/1} --use_ggHint={0/1}

use par=fa3 for ggH!
