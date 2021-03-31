

cd /afs/cern.ch/work/s/senka/HTT_2016and2017/Harvester_gitlab_Aug13/CMSSW_8_1_0/src/CombineHarvester
cmsenv
cd /afs/cern.ch/work/s/senka/HTT_2016and2017/CMSSW_9_4_4/src
cmsenv
cd -
python HTTSM2017/scripts/normToPowheg.py /afs/cern.ch/work/s/senka/HTT_2016and2017/code/htt_$1.inputs-sm-13TeV-2D_$2_isGGH1_$4_mergedBins.root output_withSuperNN_$1$2_isGGH1_$4_VBFfa3-3d-baseline_mergedBins.root $1 $2
cmsenv

if [ ${5} = "1" ]; then
	if [ ${3} = "0" ]; then
		python HTTSM2017/scripts/Unroll_2Drelaxed_FF.py output_withSuperNN_$1$2_isGGH1_$4_VBFfa3-3d-baseline_mergedBins.root $1 "$1$2_isGGH1_$4_VBFfa3-3d-baseline_mergedBins_unrolled" -z True
	else
                python HTTSM2017/scripts/Unroll_2Drelaxed_FF.py output_withSuperNN_$1$2_isGGH1_$4_VBFfa3-3d-baseline_mergedBins.root $1 "$1$2_isGGH1_$4_VBFfa3-3d-baseline_mergedBins_unrolled"
        fi
mv htt_$1.inputs-sm-13TeV-2D$1$2_isGGH1_$4_VBFfa3-3d-baseline_mergedBins_unrolled.root output_withSuperNN_$1$2_isGGH1_$4_VBFfa3-3d-baseline_mergedBins.root

fi

mv output_withSuperNN_$1$2_isGGH1_$4_VBFfa3-3d-baseline_mergedBins.root HTTAC2017/shapes/USCMS/htt_$1.inputs-sm-13TeV_$2-2D_MELAVBF_isGGH1_$4_mergedBins.root

if [ ${3} = "0" ]; then
    MorphingSM2016_flexible --output_folder="data_isGGH1_$4_mergedBins_MELAVBF" --postfix="-2D_MELAVBF_isGGH1_$4_mergedBins" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false --embedded=false --jetfakes=true --shapeSyst=false --year=$2
else
    MorphingSM2016_flexible --output_folder="data_isGGH1_$4_mergedBins_MELAVBF" --postfix="-2D_MELAVBF_isGGH1_$4_mergedBins" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false --embedded=true --jetfakes=true --shapeSyst=false --year=$2
fi

cd output/data_isGGH1_$4_mergedBins_MELAVBF
    find . -name "*.txt" -size -2k -delete

combineTool.py -M T2W -i $1/* -o workspace.root --parallel 18
sed -i 's/ CMS_ggH_STXSVBF2j//g' $1/125/combined.txt.cmb

cd $1/125

combineCards.py htt_$1_1_13TeV_$2=htt_$1_1_13TeV_$2.txt htt_$1_2_13TeV_$2=htt_$1_2_13TeV_$2.txt htt_$1_3_13TeV_$2=htt_$1_3_13TeV_$2.txt htt_$1_4_13TeV_$2=htt_$1_4_13TeV_$2.txt htt_$1_5_13TeV_$2=htt_$1_5_13TeV_$2.txt htt_$1_6_13TeV_$2=htt_$1_6_13TeV_$2.txt &> combined_$2.txt.cmb

sed -i 's/ CMS_ggH_STXSVBF2j//g' combined_$2.txt.cmb

cd -

combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FA3_Interference_JHU_ggHSyst_rw_MengsMuV:FA3_Interference_JHU_ggHSyst_rw_MengsMuV -i $1/125/combined_$2.txt.cmb -o fa03_Workspace_MengsMuV_$1_$2.root 

combineTool.py -n 1D_scan_fa3_ggH_$1_$2 -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-1.,1. $1/125/fa03_Workspace_MengsMuV_$1_$2.root --algo=grid --points=11 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P fa3_ggH --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1
#combineTool.py -n 1D_scan_fa3_$1_$2  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-1.,1. $1/125/fa03_Workspace_MengsMuV_$1_$2.root --algo=grid --points=11 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1

#cp higgsCombine1D_scan_fa3_$1_$2.MultiDimFit.mH125.root /eos/home-s/senka/HTT/scans/htt_newSkims/higgsCombine1D_scan_fa3_VBF_$1_$2_isGGH1_$4_withSyst_optimized.MultiDimFit.mH125.root
cp higgsCombine1D_scan_fa3_ggH_$1_$2.MultiDimFit.mH125.root /eos/home-s/senka/HTT/scans/htt_newSkims/higgsCombine1D_scan_fa3_$1_$2_isGGH1_$4_optimized.MultiDimFit.mH125.root

cd ../..
