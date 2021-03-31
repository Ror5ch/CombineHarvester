
END=$5
for ((i=1;i<=END;i++)); do

echo ' running toys $END'
cd /afs/cern.ch/work/s/senka/HTT_2016and2017/Harvester_gitlab_Aug13/CMSSW_8_1_0/src/CombineHarvester
cmsenv
cd /afs/cern.ch/work/s/senka/HTT_2016and2017/CMSSW_9_4_4/src
cmsenv
cd -


    python HTTSM2017/scripts/TossToys_VBF.py /afs/cern.ch/work/s/senka/HTT_2016and2017/code/htt_$1.inputs-sm-13TeV-2D_$2_$4_mergedBins.root output_htt_$1.inputs-sm-13TeV-2D_$2_$4_mergedBins_toss_$i.root tt

python HTTSM2017/scripts/normToPowheg.py output_htt_$1.inputs-sm-13TeV-2D_$2_$4_mergedBins_toss_$i.root output_withSuperNN_$1$2_$4_VBFfa3-3d-baseline_mergedBins_toss_$i.root $1
rm output_htt_$1.inputs-sm-13TeV-2D_$2_$4_mergedBins_toss_$i.root
cmsenv
mv output_withSuperNN_$1$2_$4_VBFfa3-3d-baseline_mergedBins_toss_$i.root HTTAC2017/shapes/USCMS/htt_$1.inputs-sm-13TeV-2D_MELAVBF_$2_$4_mergedBins_toss_$i.root

if [ ${3} = "0" ]; then
    MorphingSM2016_flexible --output_folder="data_$1_$2_$4_mergedBins_MELAVBF_toss_$i" --postfix="-2D_MELAVBF_$2_$4_mergedBins_toss_$i" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false --embedded=false --jetfakes=true --shapeSyst=false
else
    MorphingSM2016_flexible --output_folder="data_$1_$2_$4_mergedBins_MELAVBF_toss_$i" --postfix="-2D_MELAVBF_$2_$4_mergedBins_toss_$i" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false --embedded=true --jetfakes=true --shapeSyst=false
fi

cd output/data_$1_$2_$4_mergedBins_MELAVBF_toss_$i
combineTool.py -M T2W -i $1/* -o workspace.root --parallel 18
combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FA3_Interference_JHU_ggHSyst_rw_MengsMuV:FA3_Interference_JHU_ggHSyst_rw_MengsMuV -i $1/125/combined.txt.cmb -o fa03_Workspace_MengsMuV_$1.root 

combineTool.py -n 1D_scan_fa3 -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-1.,1. $1/125/fa03_Workspace_MengsMuV_$1.root --algo=grid --points=11 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1

cp higgsCombine1D_scan_fa3.MultiDimFit.mH125.root /eos/home-s/senka/HTT/scans/htt_newSkims/higgsCombine1D_scan_fa3_VBF_$1_$2_$4_optimized_toss_$i.MultiDimFit.mH125.root

cd ../..

mv output/data_$1_$2_$4_mergedBins_MELAVBF_toss_$i /data/senka/HTT_2016and2017/tossingToys/
 
done
