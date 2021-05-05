#!/usr/bin/env python
import ROOT
from ROOT import *

import re
from array import array
from optparse import OptionParser
import sys

import os


import argparse
parser = argparse.ArgumentParser("Prepare datacards and run limits")
parser.add_argument(
        "--chn",
        action="store",
        dest="chn",
        default="tt",
        help="Which channel is this (tt/mt/et/em) ?")
parser.add_argument(
        "--year",
        action="store",
        dest="year",
        default="2018",
        help="Which yeas is this (2016/2017/2018)?")
parser.add_argument(
        "--emb",
        action="store",
        dest="emb",
        default=0,
        help="Use embedded (0/1)?")
parser.add_argument(
        "--use_ggHint",
        action="store",
        dest="use_ggHint",
        default=0,
        help="Use ggH int (0/1)?")
parser.add_argument(
        "--use_ggHphase",
        action="store",
        dest="use_ggHphase",
        default=0,
        help="Use ggH phase (0/1)?")
parser.add_argument(
        "--inputString",
        action="store",
        dest="inputString",
        default="MANUAL_optBins_syst",
        help="Input datacard string (also used for the name of output directory) ")
parser.add_argument(
        "--useDCP",
        action="store",
        dest="useDCP",
        default=0,
        help="Use DCP bins or not (0/1) ?")
parser.add_argument(
        "--par",
        action="store",
        dest="par",
        default="fa3",
        help="Which parameter is this (fa3/fa2/fL1/fL1Zg) ?")
parser.add_argument(
        "--isGGH",
        action="store",
        dest="isGGH",
        default=0,
        help="Is this ggH measurement (0/1) ?")
parser.add_argument(
        "--useShapeSyst",
        action="store",
        dest="useShapeSyst",
        default=0,
        help="Use shape syst or not (0/1) ?")
parser.add_argument(
        "--path_datacard",
        action="store",
        dest="path_datacard",
        default=0,
        help="Path to your datacard?")
parser.add_argument(
        "--path_CMSSW94",
        action="store",
        dest="path_CMSSW94",
        default=0,
        help="Path to your harvester (.../src/CombineHarvester)?")
parser.add_argument(
        "--name_datacard",
        action="store",
        dest="name_datacard",
        default=0,
        help="Datacard name ?")
parser.add_argument(
        "--scaleGGH",
        action="store",
        dest="scaleGGH",
        default="1",
        help="Which file1name to run over?")
parser.add_argument(
        "--usePhiJJ",
        action="store",
        dest="usePhiJJ",
        default=0,
        help="Use ggH int (0/1)?")
parser.add_argument(
        "--mergeMSV",
        action="store",
        dest="mergeMSV",
        default="0",
        help="Which file1name to run over?")
parser.add_argument(
        "--symDCP",
        action="store",
        dest="symDCP",
        default="0",
        help="Which file1name to run over?")
parser.add_argument(
        "--freezeAll",
        action="store",
        dest="freezeAll",
        default="0",
        help="Which file1name to run over?")

args = parser.parse_args()

chn=args.chn 
year=int(args.year) 
emb=bool(args.emb) 
use_ggHint=bool(int(args.use_ggHint))
use_ggHphase=bool(int(args.use_ggHphase))
inputString=args.inputString 
useDCP=int(args.useDCP) 
par=args.par 
isGGH=int(args.isGGH)
useShapeSyst=int(args.useShapeSyst)
path_datacard=args.path_datacard
path_CMSSW94=args.path_CMSSW94
name_datacard=args.name_datacard
scaleGGH =float(args.scaleGGH)
usePhiJJ=int(args.usePhiJJ)
mergeMSV=int(args.mergeMSV)
symDCP=int(args.symDCP)
freezeAll=int(args.freezeAll)

print "use_ggHint= ",use_ggHint
print "use_ggHphase= ",use_ggHphase
print "bool(False) ",bool(False)
print "bool(0) ",bool(0)
#print "bool(false) ",bool(false)

ggH_string=""
if isGGH:
	ggH_string="_isGGH1"

outputFile="commands.txt"
outputFile=outputFile.replace('ds','ds_%s_%s%s_%s_%s'%(chn,year,ggH_string,inputString,par))
f_out = open(outputFile, 'w')

        
# make commands string:
## please use your own local paths !
## for the normToPowheg.py code you have to use CMSSW setup >= 9_4_4, for some to me unknown reason the py code does not run for the earlier versions
## after Morphing delete all the small size datacards (find . -name "*.txt" -size -2k -delete), these are produced for example for the empty subdirectories (et/mt)

nbins = 64 if not chn == "em" else 24

cmd="""
python merge_bins.py --inputfile {path_datacard}/{name_datacard} --channel {chn} --outputfile htt_{chn}.inputs-sm-13TeV-2D_{year}{ggH_string}_{inputString}_mergedBins.root --nbins {nbins} --year {year} --scaleGGH {scaleGGH} --usePhiJJ {usePhiJJ}  --mergeMSV {mergeMSV} --useDCP {useDCP}
""".format(chn=chn,path_datacard=path_datacard,name_datacard=name_datacard,nbins=nbins,year=year,inputString=inputString,useDCP=useDCP,par=par,ggH_string=ggH_string,scaleGGH=scaleGGH,usePhiJJ=usePhiJJ,mergeMSV=mergeMSV)

cmd+="""

eval `scramv1 runtime -sh`
cd {path_CMSSW94}/src
eval `scramv1 runtime -sh`
cd -
""".format(path_CMSSW94=path_CMSSW94)

if par!="fa3":
	cmd+="""
python HTTSM2017/scripts/rename_HVV_histos.py --par={par} --input=htt_{chn}.inputs-sm-13TeV-2D_{year}_{inputString}_mergedBins.root

mv htt_{chn}.inputs-sm-13TeV-2D_{year}_{inputString}_mergedBins_renamed.root htt_{chn}.inputs-sm-13TeV-2D_{year}_{inputString}_mergedBins.root
""".format(chn=chn,year=year,emb=emb,inputString=inputString,useDCP=useDCP,par=par,ggH_string=ggH_string)
elif symDCP:
        cmd+="""
python Symmetrize_DCP.py --name_datacard=htt_{chn}.inputs-sm-13TeV-2D_{year}{ggH_string}_{inputString}_mergedBins.root --isGGH={isGGH}
mv htt_{chn}.inputs-sm-13TeV-2D_{year}{ggH_string}_{inputString}_mergedBins_DCPsym.root htt_{chn}.inputs-sm-13TeV-2D_{year}{ggH_string}_{inputString}_mergedBins.root
""".format(chn=chn,year=year,emb=emb,inputString=inputString,useDCP=useDCP,par=par,ggH_string=ggH_string,isGGH=isGGH)


                
cmd+="""
python negativeBinRemover.py htt_{chn}.inputs-sm-13TeV-2D_{year}{ggH_string}_{inputString}_mergedBins.root
mv htt_{chn}.inputs-sm-13TeV-2D_{year}{ggH_string}_{inputString}_mergedBins_noNegativeBins.root htt_{chn}.inputs-sm-13TeV-2D_{year}{ggH_string}_{inputString}_mergedBins.root 
""".format(chn=chn,year=year,emb=emb,inputString=inputString,useDCP=useDCP,par=par,ggH_string=ggH_string,isGGH=isGGH)
        

        
cmd+="""
python HTTSM2017/scripts/normToPowheg.py htt_{chn}.inputs-sm-13TeV-2D_{year}{ggH_string}_{inputString}_mergedBins.root output_withSuperNN_{chn}{year}{ggH_string}_{inputString}_VBFfa3-3d-baseline_mergedBins.root {chn} {year} {useDCP} {par}


""".format(chn=chn,year=year,emb=emb,inputString=inputString,useDCP=useDCP,par=par,ggH_string=ggH_string,use_ggHint=int(use_ggHint))

cmd+="""


eval `scramv1 runtime -sh`

mv output_withSuperNN_{chn}{year}{ggH_string}_{inputString}_VBFfa3-3d-baseline_mergedBins.root HTTAC2017/shapes/USCMS/htt_{chn}.inputs-sm-13TeV_{year}-2D_MELAVBF{ggH_string}_{inputString}_mergedBins.root

""".format(chn=chn,year=year,emb=emb,inputString=inputString,useDCP=useDCP,par=par,ggH_string=ggH_string,use_ggHint=int(use_ggHint))

if useShapeSyst:

        cmd+="""
MorphingSM2016_flexible --output_folder="data{ggH_string}_{inputString}_mergedBins_withSyst_MELAVBF" --postfix="-2D_MELAVBF{ggH_string}_{inputString}_mergedBins" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false --embedded={emb} --jetfakes=true --shapeSyst=true --year={year} --chn={chn} --par={par} --use_ggHint={use_ggHint} --useSingleVBFdir=0
""".format(chn=chn,year=year,emb=emb,inputString=inputString,useDCP=useDCP,par=par,ggH_string=ggH_string,use_ggHint=use_ggHint)

else:
        cmd+="""
MorphingSM2016_flexible --output_folder="data{ggH_string}_{inputString}_mergedBins_withSyst_MELAVBF" --postfix="-2D_MELAVBF{ggH_string}_{inputString}_mergedBins" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false --embedded={emb} --jetfakes=true --shapeSyst=false --year={year} --chn={chn} --par={par} --use_ggHint={use_ggHint} --useSingleVBFdir=0
""".format(chn=chn,year=year,emb=emb,inputString=inputString,useDCP=useDCP,par=par,ggH_string=ggH_string,use_ggHint=use_ggHint)

cmd+="""

eval `scramv1 runtime -sh`
cd {path_CMSSW94}/src
eval `scramv1 runtime -sh`
cd -
""".format(path_CMSSW94=path_CMSSW94)


cmd+="""

python HTTSM2017/scripts/checkSignal.py -i output/data{ggH_string}_{inputString}_mergedBins_withSyst_MELAVBF/{chn}/common/htt_input_{year}.root -o data{ggH_string}_{inputString}_{year}_mergedBins_withSyst_MELAVBF_afterCheckSignal.root -g {use_ggHint} -p 0 -c {chn} -u {par}

echo "second checkSignal"

python HTTSM2017/scripts/checkSignal.py -i data{ggH_string}_{inputString}_{year}_mergedBins_withSyst_MELAVBF_afterCheckSignal.root -o tests.root -g {use_ggHint} -p 0 -c {chn} -u {par} | tee output_checkSignal_data{ggH_string}_{inputString}_{year}_mergedBins_withSyst_MELAVBF_afterCheckSignal

rm data{ggH_string}_{inputString}_{year}_mergedBins_withSyst_MELAVBF_afterCheckSignal.root

""".format(chn=chn,year=year,emb=emb,inputString=inputString,useDCP=useDCP,par=par,ggH_string=ggH_string,use_ggHint=int(use_ggHint))

cmd+="""


eval `scramv1 runtime -sh`
"""


cmd+="""
cd output/data{ggH_string}_{inputString}_mergedBins_withSyst_MELAVBF
    find . -name "*.txt" -size -2k -delete

cd {chn}/125

""".format(chn=chn,year=year,emb=emb,inputString=inputString,useDCP=useDCP,par=par,ggH_string=ggH_string)

# if em 2018 channel remove the zmumuShape systematics, buggy
if chn=="em":
    if year==2018:
        cmd+=""" 
        sed -i '/zmumuShape/d' "*{chn}*{year}*.txt"
        """.format(chn=chn,year=year)

# to be safe define which datacards you merge by hads, for case of use of DCP bins or not
if useDCP:
    cmd+=""" 
	combineCards.py htt_{chn}_1_{year}=htt_{chn}_1_{year}.txt htt_{chn}_2_{year}=htt_{chn}_2_{year}.txt htt_{chn}_3_{year}=htt_{chn}_3_{year}.txt htt_{chn}_4_{year}=htt_{chn}_4_{year}.txt htt_{chn}_5_{year}=htt_{chn}_5_{year}.txt htt_{chn}_6_{year}=htt_{chn}_6_{year}.txt  htt_{chn}_7_{year}=htt_{chn}_7_{year}.txt  htt_{chn}_8_{year}=htt_{chn}_8_{year}.txt  htt_{chn}_9_{year}=htt_{chn}_9_{year}.txt  htt_{chn}_10_{year}=htt_{chn}_10_{year}.txt &> combined_{chn}_{year}.txt.cmb
    """.format(chn=chn,year=year)
else:
    cmd+=""" 
        combineCards.py htt_{chn}_1_{year}=htt_{chn}_1_{year}.txt htt_{chn}_2_{year}=htt_{chn}_2_{year}.txt htt_{chn}_3_{year}=htt_{chn}_3_{year}.txt htt_{chn}_4_{year}=htt_{chn}_4_{year}.txt htt_{chn}_5_{year}=htt_{chn}_5_{year}.txt htt_{chn}_6_{year}=htt_{chn}_6_{year}.txt &> combined_{chn}_{year}.txt.cmb
    """.format(chn=chn,year=year)

# remove from the list of all systematics the CMS_ggH_STXSVBF2j, for some reason this syst appears in the list but it is not there. Not sure why it gets listed there..
cmd+=""" 
cd -

sed -i 's/ CMS_ggH_STXSVBF2j//g' {chn}/125/combined_{chn}_{year}.txt.cmb

""".format(chn=chn,year=year)

# make the final workspace, depending which parameter you measure use the appropriate signal model (the only difference between different models is the cross section of the BSM model)

if par=="fa3" and not use_ggHint:
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FA3_Interference_JHU_ggHSyst_rw_MengsMuV:FA3_Interference_JHU_ggHSyst_rw_MengsMuV -i {chn}/125/combined_{chn}_{year}.txt.cmb -o fa03_Workspace_MengsMuV_{chn}_{year}.root 
    """.format(chn=chn,year=year,inputString=inputString,ggH_string=ggH_string)
elif par=="fa3" and use_ggHint and use_ggHphase:
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FA3_Interference_JHU_ggHSyst_rw_MengsMuV_HeshyXsec_ggHInt_ggHphase:FA3_Interference_JHU_ggHSyst_rw_MengsMuV_HeshyXsec_ggHInt_ggHphase -i {chn}/125/combined_{chn}_{year}.txt.cmb -o fa03_Workspace_MengsMuV_{chn}_{year}.root 
    """.format(chn=chn,year=year,inputString=inputString,ggH_string=ggH_string)
elif par=="fa3" and use_ggHint:
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FA3_Interference_JHU_ggHSyst_rw_MengsMuV_HeshyXsec_ggHInt:FA3_Interference_JHU_ggHSyst_rw_MengsMuV_HeshyXsec_ggHInt -i {chn}/125/combined_{chn}_{year}.txt.cmb -o fa03_Workspace_MengsMuV_{chn}_{year}.root 
    """.format(chn=chn,year=year,inputString=inputString,ggH_string=ggH_string)
elif par=="fa2":
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FA2_Interference_JHU_rw_MengsMuV:FA2_Interference_JHU_rw_MengsMuV -i {chn}/125/combined_{chn}_{year}.txt.cmb -o fa03_Workspace_MengsMuV_{chn}_{year}.root 
    """.format(chn=chn,year=year,inputString=inputString,ggH_string=ggH_string)
elif par=="fL1":
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FL1_Interference_JHU_rw_MengsMuV:FL1_Interference_JHU_rw_MengsMuV -i {chn}/125/combined_{chn}_{year}.txt.cmb -o fa03_Workspace_MengsMuV_{chn}_{year}.root 
    """.format(chn=chn,year=year,inputString=inputString,ggH_string=ggH_string)
elif par=="fL1Zg":
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FL1Zg_Interference_JHU_rw_MengsMuV:FL1Zg_Interference_JHU_rw_MengsMuV -i {chn}/125/combined_{chn}_{year}.txt.cmb -o fa03_Workspace_MengsMuV_{chn}_{year}.root 
    """.format(chn=chn,year=year,inputString=inputString,ggH_string=ggH_string)

# run the limits and copy output
if isGGH and use_ggHphase:
        cmd+=""" 

# combineTool.py -n 1D_scan_fa3_ggH_{chn}_{year}  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=-1.,1.:CMS_zz4l_fai1=-0.1,0.1 {chn}/125/fa03_Workspace_MengsMuV_{chn}_{year}.root --algo=grid --points=101 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P fa3_ggH --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1

""".format(chn=chn,year=year,inputString=inputString,ggH_string=ggH_string)

elif isGGH:
	if freezeAll:
                cmd+=""" 

# combineTool.py -n 1D_scan_fa3_ggH_{chn}_{year}_freeze  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-0.1,0.1 {chn}/125/fa03_Workspace_MengsMuV_{chn}_{year}.root --algo=grid --points=101 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P fa3_ggH --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1  --freezeNuisanceGroups all

""".format(chn=chn,year=year,inputString=inputString,ggH_string=ggH_string)
	else:
        	cmd+=""" 

# combineTool.py -n 1D_scan_fa3_ggH_{chn}_{year}  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-0.1,0.1 {chn}/125/fa03_Workspace_MengsMuV_{chn}_{year}.root --algo=grid --points=101 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P fa3_ggH --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1


# combineTool.py -n 1D_scan_fa3_ggH_{chn}_{year}_freeze  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-0.1,0.1 {chn}/125/fa03_Workspace_MengsMuV_{chn}_{year}.root --algo=grid --points=101 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P fa3_ggH --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1  --freezeNuisanceGroups all



""".format(chn=chn,year=year,inputString=inputString,ggH_string=ggH_string)

else:
	cmd+=""" 

# combineTool.py -n 1D_scan_fa3_{chn}_{year}  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-0.1,0.1 {chn}/125/fa03_Workspace_MengsMuV_{chn}_{year}.root --algo=grid --points=101 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1

""".format(chn=chn,year=year,inputString=inputString,ggH_string=ggH_string)

cmd+=""" 
cd ../..

""".format(chn=chn,year=year,inputString=inputString,ggH_string=ggH_string)

#print cmd

print " >>>> writing commands to commands.txt>>> execute:"
print " source %s"%(outputFile)

f_out.write(cmd)
f_out.close()
#os.system(cmd)
