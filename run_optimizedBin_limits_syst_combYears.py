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
        "--emb",
        action="store",
        dest="emb",
        default=0,
        help="Use embedded (0/1)?")
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
        "--isGGH",
        action="store",
        dest="isGGH",
        default=0,
        help="Is this ggH measurement (0/1) ?")
parser.add_argument(
        "--par",
        action="store",
        dest="par",
        default="fa3",
        help="Which parameter is this (fa3/fa2/fL1/fL1Zg) ?")

args = parser.parse_args()

chn=args.chn # nbins->chn 1
emb=bool(args.emb) # year->emb 3
inputString=args.inputString # emb->inputString 4
useDCP=int(args.useDCP) # ok 6
isGGH=int(args.isGGH)
par=args.par # 7


# make commands string:

# remove all datacards with no inputs (used for mt/et where empty vbf-subdirs are present)
if isGGH:
        cmd="""
        cd output/data_isGGH1_{inputString}_mergedBins_withSyst_MELAVBF
	""".format(inputString=inputString)
else:
	cmd="""
	cd output/data_{inputString}_mergedBins_withSyst_MELAVBF
	""".format(inputString=inputString)
cmd+="""
    	find . -name "*.txt" -size -2k -delete	
	cd {chn}/125
""".format(chn=chn)

# combine txt datacards based on DCP bins
if useDCP:
	cmd+=""" 
combineCards.py htt_{chn}_1_13TeV_2016=htt_{chn}_1_13TeV_2016.txt htt_{chn}_2_13TeV_2016=htt_{chn}_2_13TeV_2016.txt htt_{chn}_3_13TeV_2016=htt_{chn}_3_13TeV_2016.txt htt_{chn}_4_13TeV_2016=htt_{chn}_4_13TeV_2016.txt htt_{chn}_5_13TeV_2016=htt_{chn}_5_13TeV_2016.txt htt_{chn}_6_13TeV_2016=htt_{chn}_6_13TeV_2016.txt htt_{chn}_7_13TeV_2016=htt_{chn}_7_13TeV_2016.txt htt_{chn}_8_13TeV_2016=htt_{chn}_8_13TeV_2016.txt htt_{chn}_9_13TeV_2016=htt_{chn}_9_13TeV_2016.txt htt_{chn}_10_13TeV_2016=htt_{chn}_10_13TeV_2016.txt htt_{chn}_1_13TeV_2017=htt_{chn}_1_13TeV_2017.txt htt_{chn}_2_13TeV_2017=htt_{chn}_2_13TeV_2017.txt htt_{chn}_3_13TeV_2017=htt_{chn}_3_13TeV_2017.txt htt_{chn}_4_13TeV_2017=htt_{chn}_4_13TeV_2017.txt htt_{chn}_5_13TeV_2017=htt_{chn}_5_13TeV_2017.txt htt_{chn}_6_13TeV_2017=htt_{chn}_6_13TeV_2017.txt htt_{chn}_7_13TeV_2017=htt_{chn}_7_13TeV_2017.txt htt_{chn}_8_13TeV_2017=htt_{chn}_8_13TeV_2017.txt htt_{chn}_9_13TeV_2017=htt_{chn}_9_13TeV_2017.txt htt_{chn}_10_13TeV_2017=htt_{chn}_10_13TeV_2017.txt htt_{chn}_1_13TeV_2018=htt_{chn}_1_13TeV_2018.txt htt_{chn}_2_13TeV_2018=htt_{chn}_2_13TeV_2018.txt htt_{chn}_3_13TeV_2018=htt_{chn}_3_13TeV_2018.txt htt_{chn}_4_13TeV_2018=htt_{chn}_4_13TeV_2018.txt htt_{chn}_5_13TeV_2018=htt_{chn}_5_13TeV_2018.txt htt_{chn}_6_13TeV_2018=htt_{chn}_6_13TeV_2018.txt htt_{chn}_7_13TeV_2018=htt_{chn}_7_13TeV_2018.txt htt_{chn}_8_13TeV_2018=htt_{chn}_8_13TeV_2018.txt htt_{chn}_9_13TeV_2018=htt_{chn}_9_13TeV_2018.txt htt_{chn}_10_13TeV_2018=htt_{chn}_10_13TeV_2018.txt &> combined_all.txt.cmb 
""".format(chn=chn) 

else:
	cmd+="""
combineCards.py htt_{chn}_1_13TeV_2016=htt_{chn}_1_13TeV_2016.txt htt_{chn}_2_13TeV_2016=htt_{chn}_2_13TeV_2016.txt htt_{chn}_3_13TeV_2016=htt_{chn}_3_13TeV_2016.txt htt_{chn}_4_13TeV_2016=htt_{chn}_4_13TeV_2016.txt htt_{chn}_5_13TeV_2016=htt_{chn}_5_13TeV_2016.txt htt_{chn}_6_13TeV_2016=htt_{chn}_6_13TeV_2016.txt htt_{chn}_1_13TeV_2017=htt_{chn}_1_13TeV_2017.txt htt_{chn}_2_13TeV_2017=htt_{chn}_2_13TeV_2017.txt htt_{chn}_3_13TeV_2017=htt_{chn}_3_13TeV_2017.txt htt_{chn}_4_13TeV_2017=htt_{chn}_4_13TeV_2017.txt htt_{chn}_5_13TeV_2017=htt_{chn}_5_13TeV_2017.txt htt_{chn}_6_13TeV_2017=htt_{chn}_6_13TeV_2017.txt htt_{chn}_1_13TeV_2018=htt_{chn}_1_13TeV_2018.txt htt_{chn}_2_13TeV_2018=htt_{chn}_2_13TeV_2018.txt htt_{chn}_3_13TeV_2018=htt_{chn}_3_13TeV_2018.txt htt_{chn}_4_13TeV_2018=htt_{chn}_4_13TeV_2018.txt htt_{chn}_5_13TeV_2018=htt_{chn}_5_13TeV_2018.txt htt_{chn}_6_13TeV_2018=htt_{chn}_6_13TeV_2018.txt &> combined_all.txt.cmb
""".format(chn=chn) 

# remove the syst that shows up in the list off all nuisances but is actually not there
cmd+="""
sed -i 's/ CMS_ggH_STXSVBF2j//g' combined_all.txt.cmb

cd -
"""

# make workspace using appropriate signal model
if par=="fa3" or isGGH:
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FA3_Interference_JHU_ggHSyst_rw_MengsMuV:FA3_Interference_JHU_ggHSyst_rw_MengsMuV -i {chn}/125/combined_all.txt.cmb -o fa03_Workspace_MengsMuV_{chn}_all.root 
    """.format(chn=chn,inputString=inputString)
elif par=="fa2":
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FA2_Interference_JHU_rw_MengsMuV:FA2_Interference_JHU_rw_MengsMuV -i {chn}/125/combined_all.txt.cmb -o fa03_Workspace_MengsMuV_{chn}_all.root 
    """.format(chn=chn,inputString=inputString)
elif par=="fL1":
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FL1_Interference_JHU_rw_MengsMuV:FL1_Interference_JHU_rw_MengsMuV -i {chn}/125/combined_all.txt.cmb -o fa03_Workspace_MengsMuV_{chn}_all.root 
    """.format(chn=chn,inputString=inputString)
elif par=="fL1Zg":
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FL1Zg_Interference_JHU_rw_MengsMuV:FL1Zg_Interference_JHU_rw_MengsMuV -i {chn}/125/combined_all.txt.cmb -o fa03_Workspace_MengsMuV_{chn}_all.root 
    """.format(chn=chn,inputString=inputString)

# run limits:
if isGGH:
	cmd+="""
combineTool.py -n 1D_scan_fa3_ggH_{chn}_all  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-0.03,0.03 {chn}/125/fa03_Workspace_MengsMuV_{chn}_all.root --algo=grid --points=41 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P fa3_ggH --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1
	""".format(chn=chn,inputString=inputString)

else:
	cmd+="""
combineTool.py -n 1D_scan_fa3_{chn}_all  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-0.03,0.03 {chn}/125/fa03_Workspace_MengsMuV_{chn}_all.root --algo=grid --points=41 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1
	""".format(chn=chn,inputString=inputString)

cmd+="""
cd ../..
"""

print cmd
os.system(cmd)


