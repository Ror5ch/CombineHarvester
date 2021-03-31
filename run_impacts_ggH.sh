cd output/data_isGGH1_MANUAL_optBins_fa3_ggHint_AutoRebin_swaped_newFSA_HWWSMPowheg_Syst_mergedBins_withSyst_MELAVBF
combineTool.py -M Impacts -d $1/125/fa03_Workspace_MengsMuV_$1_$2.root -m 125 --doInitialFit --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-1,1  --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.0,muf=1.,fa3_ggH=0.5  -t -1 --expectSignal=1
nice combineTool.py -M Impacts -d $1/125/fa03_Workspace_MengsMuV_$1_$2.root -m 125 --doFits --parallel 8 -t -1 --setParameters muV=1.,fa3_ggH=0.5,CMS_zz4l_fai1=0.0,muf=1. --setParameterRanges muV=0.0,2.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-1.,1. --setRobustFitAlgo=Minuit2,Migrad --robustFit=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\"
combineTool.py -M Impacts -d $1/125/fa03_Workspace_MengsMuV_$1_$2.root -m 125 -t -1 --setParameters muV=1.,fa3_ggH=0.5,CMS_zz4l_fai1=0.0,muf=1. --setParameterRanges muV=0.0,2.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-1,1 --setRobustFitAlgo=Minuit2,Migrad --robustFit=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" -o impacts_ggH_$1_$2.json
plotImpacts_ggH.py -i impacts_ggH_$1_$2.json -o impacts_ggH_$1_$2 --POI fa3_ggH
rm higgsCombine_paramFit*root
rm higgsCombine_initialFit_Test.MultiDimFit.mH125.root
cp impacts_ggH_$1_$2.pdf ../../
cd ../..

