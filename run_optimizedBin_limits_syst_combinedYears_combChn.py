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

emb=bool(args.emb) # year->emb 3
inputString=args.inputString # emb->inputString 4
isGGH=int(args.isGGH)
par=args.par # 7


# make commands string:

# remove all datacards with no inputs (used for mt/et where empty vbf-subdirs are present)
if isGGH:
        cmd="""
        output/data_isGGH1_{inputString}_mergedBins_withSyst_MELAVBF
	"""
else:
	cmd="""
	output/data_{inputString}_mergedBins_withSyst_MELAVBF
	"""
cmd+="""
    	find . -name "*.txt" -size -2k -delete	
        rm cmb/125/combined.txt.cmb
	combineTool.py -M T2W -i cmb/* -o workspace.root --parallel 18

"""


# make workspace using appropriate signal model
if par=="fa3" or isGGH:
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FA3_Interference_JHU_ggHSyst_rw_MengsMuV:FA3_Interference_JHU_ggHSyst_rw_MengsMuV -i cmb/125/combined.txt.cmb -o fa03_Workspace_MengsMuV_cmb_all.root 
    """.format(inputString=inputString)
elif par=="fa2":
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FA2_Interference_JHU_rw_MengsMuV:FA2_Interference_JHU_rw_MengsMuV -i cmb/125/combined.txt.cmb -o fa03_Workspace_MengsMuV_cmb_all.root 
    """.format(inputString=inputString)
elif par=="fL1":
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FL1_Interference_JHU_rw_MengsMuV:FL1_Interference_JHU_rw_MengsMuV -i cmb/125/combined.txt.cmb -o fa03_Workspace_MengsMuV_cmb_all.root 
    """.format(inputString=inputString)
elif par=="fL1Zg":
    cmd+="""  
    combineTool.py -M T2W -m 125 -P HiggsAnalysis.CombinedLimit.FL1Zg_Interference_JHU_rw_MengsMuV:FL1Zg_Interference_JHU_rw_MengsMuV -i cmb/125/combined.txt.cmb -o fa03_Workspace_MengsMuV_cmb_all.root 
    """.format(inputString=inputString)

# run limits:
if isGGH:
	cmd+="""
combineTool.py -n 1D_scan_fa3_ggH_cmb_all  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-0.03,0.03 cmb/125/fa03_Workspace_MengsMuV_cmb_all.root --algo=grid --points=41 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P fa3_ggH --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1
	"""

else:
	cmd+="""
combineTool.py -n 1D_scan_fa3_cmb_all  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-0.03,0.03 cmb/125/fa03_Workspace_MengsMuV_cmb_all.root --algo=grid --points=41 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo \"Minuit2,0:1.\" --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1
	"""

cmd+="""
cd ../..
""".format(emb=emb,inputString=inputString,par=par)

print cmd
os.system(cmd)


