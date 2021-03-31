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
        "--inputString",
        action="store",
        dest="inputString",
        default="MANUAL_optBins_syst",
        help="Input datacard string (also used for the name of output directory) ")

args = parser.parse_args()

par=args.par 
isGGH=int(args.isGGH)
inputString=args.inputString 

outputFile="commands.txt"
outputFile=outputFile.replace('.txt','_'+inputString+'_'+par+'_cmb.txt')
f_out = open(outputFile, 'w')

cmd="""

cd $CMSSW_BASE/src/CombineHarvester/output/data_MANUAL_optBins_{par}_ggHint_AutoRebin_swaped_newFSA_HWWSMPowheg_Syst_mergedBins_withSyst_MELAVBF/cmb
cp /data6/Users/knam/13TeV/HTTAC/doyeong/output_Nov23/data_2D_htt_tt_emb_sys_{par}/cmb/125/*txt 125/

cp ../em/common/htt_input_2016.root common/htt_em_input_2016.root
cp ../em/common/htt_input_2017.root common/htt_em_input_2017.root
cp ../em/common/htt_input_2018.root common/htt_em_input_2018.root

cp ../et/common/htt_input_2016.root common/htt_et_input_2016.root
cp ../et/common/htt_input_2017.root common/htt_et_input_2017.root
cp ../et/common/htt_input_2018.root common/htt_et_input_2018.root

cp ../mt/common/htt_input_2016.root common/htt_mt_input_2016.root
cp ../mt/common/htt_input_2017.root common/htt_mt_input_2017.root
cp ../mt/common/htt_input_2018.root common/htt_mt_input_2018.root

cp /data6/Users/knam/13TeV/HTTAC/doyeong/output_Nov23/data_2D_htt_tt_emb_sys_{par}/cmb/common/htt_input_2016.root common/htt_tt_input_2016.root
cp /data6/Users/knam/13TeV/HTTAC/doyeong/output_Nov23/data_2D_htt_tt_emb_sys_{par}/cmb/common/htt_input_2017.root common/htt_tt_input_2017.root
cp /data6/Users/knam/13TeV/HTTAC/doyeong/output_Nov23/data_2D_htt_tt_emb_sys_{par}/cmb/common/htt_input_2018.root common/htt_tt_input_2018.root

cd 125

sed -i 's/htt_input_/htt_em_input_/g' htt_em_*.txt
sed -i 's/htt_input_/htt_et_input_/g' htt_et_*.txt
sed -i 's/htt_input_/htt_mt_input_/g' htt_mt_*.txt
sed -i 's/htt_input_/htt_tt_input_/g' htt_tt_*.txt

""".format(inputString=inputString,par=par)

if "fa3" not in par:
    
    cmd+="""

cd ../..
source ../../run_rename_ggH_tt

sed -i 's/reweighted_ggH_htt_0PM/GGH2Jets_sm_M/g' cmb/125/*_tt*.txt*

cd cmb/125 

combineCards.py htt_em_1_2016=htt_em_1_2016.txt htt_em_2_2016=htt_em_2_2016.txt htt_em_3_2016=htt_em_3_2016.txt htt_em_4_2016=htt_em_4_2016.txt htt_em_5_2016=htt_em_5_2016.txt htt_em_6_2016=htt_em_6_2016.txt htt_em_1_2017=htt_em_1_2017.txt htt_em_2_2017=htt_em_2_2017.txt htt_em_3_2017=htt_em_3_2017.txt htt_em_4_2017=htt_em_4_2017.txt htt_em_5_2017=htt_em_5_2017.txt htt_em_6_2017=htt_em_6_2017.txt htt_em_1_2018=htt_em_1_2018.txt htt_em_2_2018=htt_em_2_2018.txt htt_em_3_2018=htt_em_3_2018.txt htt_em_4_2018=htt_em_4_2018.txt htt_em_5_2018=htt_em_5_2018.txt htt_em_6_2018=htt_em_6_2018.txt &> combined_test_cmb_em_years.txt.cmb
combineCards.py htt_tt_1_2016=htt_tt_1_2016.txt htt_tt_2_2016=htt_tt_2_2016.txt htt_tt_3_2016=htt_tt_3_2016.txt htt_tt_4_2016=htt_tt_4_2016.txt htt_tt_5_2016=htt_tt_5_2016.txt htt_tt_6_2016=htt_tt_6_2016.txt htt_tt_1_2017=htt_tt_1_2017.txt htt_tt_2_2017=htt_tt_2_2017.txt htt_tt_3_2017=htt_tt_3_2017.txt htt_tt_4_2017=htt_tt_4_2017.txt htt_tt_5_2017=htt_tt_5_2017.txt htt_tt_6_2017=htt_tt_6_2017.txt htt_tt_1_2018=htt_tt_1_2018.txt htt_tt_2_2018=htt_tt_2_2018.txt htt_tt_3_2018=htt_tt_3_2018.txt htt_tt_4_2018=htt_tt_4_2018.txt htt_tt_5_2018=htt_tt_5_2018.txt htt_tt_6_2018=htt_tt_6_2018.txt &> combined_test_cmb_tt_years.txt.cmb
combineCards.py htt_et_1_2016=htt_et_1_2016.txt htt_et_2_2016=htt_et_2_2016.txt htt_et_3_2016=htt_et_3_2016.txt htt_et_4_2016=htt_et_4_2016.txt htt_et_5_2016=htt_et_5_2016.txt htt_et_6_2016=htt_et_6_2016.txt htt_et_1_2017=htt_et_1_2017.txt htt_et_2_2017=htt_et_2_2017.txt htt_et_3_2017=htt_et_3_2017.txt htt_et_4_2017=htt_et_4_2017.txt htt_et_5_2017=htt_et_5_2017.txt htt_et_6_2017=htt_et_6_2017.txt htt_et_1_2018=htt_et_1_2018.txt htt_et_2_2018=htt_et_2_2018.txt htt_et_3_2018=htt_et_3_2018.txt htt_et_4_2018=htt_et_4_2018.txt htt_et_5_2018=htt_et_5_2018.txt htt_et_6_2018=htt_et_6_2018.txt &> combined_test_cmb_et_years.txt.cmb
combineCards.py htt_mt_1_2016=htt_mt_1_2016.txt htt_mt_2_2016=htt_mt_2_2016.txt htt_mt_3_2016=htt_mt_3_2016.txt htt_mt_4_2016=htt_mt_4_2016.txt htt_mt_5_2016=htt_mt_5_2016.txt htt_mt_6_2016=htt_mt_6_2016.txt htt_mt_1_2017=htt_mt_1_2017.txt htt_mt_2_2017=htt_mt_2_2017.txt htt_mt_3_2017=htt_mt_3_2017.txt htt_mt_4_2017=htt_mt_4_2017.txt htt_mt_5_2017=htt_mt_5_2017.txt htt_mt_6_2017=htt_mt_6_2017.txt htt_mt_1_2018=htt_mt_1_2018.txt htt_mt_2_2018=htt_mt_2_2018.txt htt_mt_3_2018=htt_mt_3_2018.txt htt_mt_4_2018=htt_mt_4_2018.txt htt_mt_5_2018=htt_mt_5_2018.txt htt_mt_6_2018=htt_mt_6_2018.txt &> combined_test_cmb_mt_years.txt.cmb

combineCards.py htt_em_1_2016=htt_em_1_2016.txt htt_em_2_2016=htt_em_2_2016.txt htt_em_3_2016=htt_em_3_2016.txt htt_em_4_2016=htt_em_4_2016.txt htt_em_5_2016=htt_em_5_2016.txt htt_em_6_2016=htt_em_6_2016.txt htt_em_1_2017=htt_em_1_2017.txt htt_em_2_2017=htt_em_2_2017.txt htt_em_3_2017=htt_em_3_2017.txt htt_em_4_2017=htt_em_4_2017.txt htt_em_5_2017=htt_em_5_2017.txt htt_em_6_2017=htt_em_6_2017.txt htt_em_1_2018=htt_em_1_2018.txt htt_em_2_2018=htt_em_2_2018.txt htt_em_3_2018=htt_em_3_2018.txt htt_em_4_2018=htt_em_4_2018.txt htt_em_5_2018=htt_em_5_2018.txt htt_em_6_2018=htt_em_6_2018.txt htt_et_1_2016=htt_et_1_2016.txt htt_et_2_2016=htt_et_2_2016.txt htt_et_3_2016=htt_et_3_2016.txt htt_et_4_2016=htt_et_4_2016.txt htt_et_5_2016=htt_et_5_2016.txt htt_et_6_2016=htt_et_6_2016.txt htt_et_1_2017=htt_et_1_2017.txt htt_et_2_2017=htt_et_2_2017.txt htt_et_3_2017=htt_et_3_2017.txt htt_et_4_2017=htt_et_4_2017.txt htt_et_5_2017=htt_et_5_2017.txt htt_et_6_2017=htt_et_6_2017.txt htt_et_1_2018=htt_et_1_2018.txt htt_et_2_2018=htt_et_2_2018.txt htt_et_3_2018=htt_et_3_2018.txt htt_et_4_2018=htt_et_4_2018.txt htt_et_5_2018=htt_et_5_2018.txt htt_et_6_2018=htt_et_6_2018.txt htt_mt_1_2016=htt_mt_1_2016.txt htt_mt_2_2016=htt_mt_2_2016.txt htt_mt_3_2016=htt_mt_3_2016.txt htt_mt_4_2016=htt_mt_4_2016.txt htt_mt_5_2016=htt_mt_5_2016.txt htt_mt_6_2016=htt_mt_6_2016.txt htt_mt_1_2017=htt_mt_1_2017.txt htt_mt_2_2017=htt_mt_2_2017.txt htt_mt_3_2017=htt_mt_3_2017.txt htt_mt_4_2017=htt_mt_4_2017.txt htt_mt_5_2017=htt_mt_5_2017.txt htt_mt_6_2017=htt_mt_6_2017.txt htt_mt_1_2018=htt_mt_1_2018.txt htt_mt_2_2018=htt_mt_2_2018.txt htt_mt_3_2018=htt_mt_3_2018.txt htt_mt_4_2018=htt_mt_4_2018.txt htt_mt_5_2018=htt_mt_5_2018.txt htt_mt_6_2018=htt_mt_6_2018.txt htt_tt_1_2016=htt_tt_1_2016.txt htt_tt_2_2016=htt_tt_2_2016.txt htt_tt_3_2016=htt_tt_3_2016.txt htt_tt_4_2016=htt_tt_4_2016.txt htt_tt_5_2016=htt_tt_5_2016.txt htt_tt_6_2016=htt_tt_6_2016.txt htt_tt_1_2017=htt_tt_1_2017.txt htt_tt_2_2017=htt_tt_2_2017.txt htt_tt_3_2017=htt_tt_3_2017.txt htt_tt_4_2017=htt_tt_4_2017.txt htt_tt_5_2017=htt_tt_5_2017.txt htt_tt_6_2017=htt_tt_6_2017.txt htt_tt_1_2018=htt_tt_1_2018.txt htt_tt_2_2018=htt_tt_2_2018.txt htt_tt_3_2018=htt_tt_3_2018.txt htt_tt_4_2018=htt_tt_4_2018.txt htt_tt_5_2018=htt_tt_5_2018.txt htt_tt_6_2018=htt_tt_6_2018.txt &> combined_test_cmb_emetmttt_years.txt.cmb

    """.format(inputString=inputString,par=par)
else:
    cmd+="""

cd ../..
source ../../run_rename_ggH_tt

sed -i 's/reweighted_ggH_htt_0PM/GGH2Jets_sm_M/g' cmb/125/*_tt*.txt*
sed -i 's/reweighted_ggH_htt_0M/GGH2Jets_pseudoscalar_M/g' cmb/125/*_tt*.txt*
sed -i 's/reweighted_ggH_htt_0Mf05ph0/GGH2Jets_pseudoscalar_Mf05ph0/g' cmb/125/*_tt*.txt*

cd cmb/125 

combineCards.py htt_em_1_2016=htt_em_1_2016.txt htt_em_2_2016=htt_em_2_2016.txt htt_em_3_2016=htt_em_3_2016.txt htt_em_4_2016=htt_em_4_2016.txt htt_em_5_2016=htt_em_5_2016.txt htt_em_6_2016=htt_em_6_2016.txt htt_em_7_2016=htt_em_7_2016.txt htt_em_8_2016=htt_em_8_2016.txt htt_em_9_2016=htt_em_9_2016.txt htt_em_10_2016=htt_em_10_2016.txt htt_em_1_2017=htt_em_1_2017.txt htt_em_2_2017=htt_em_2_2017.txt htt_em_3_2017=htt_em_3_2017.txt htt_em_4_2017=htt_em_4_2017.txt htt_em_5_2017=htt_em_5_2017.txt htt_em_6_2017=htt_em_6_2017.txt htt_em_7_2017=htt_em_7_2017.txt htt_em_8_2017=htt_em_8_2017.txt htt_em_9_2017=htt_em_9_2017.txt htt_em_10_2017=htt_em_10_2017.txt htt_em_1_2018=htt_em_1_2018.txt htt_em_2_2018=htt_em_2_2018.txt htt_em_3_2018=htt_em_3_2018.txt htt_em_4_2018=htt_em_4_2018.txt htt_em_5_2018=htt_em_5_2018.txt htt_em_6_2018=htt_em_6_2018.txt htt_em_7_2018=htt_em_7_2018.txt htt_em_8_2018=htt_em_8_2018.txt htt_em_9_2018=htt_em_9_2018.txt htt_em_10_2018=htt_em_10_2018.txt  &> combined_test_cmb_em_years.txt.cmb

combineCards.py htt_et_1_2016=htt_et_1_2016.txt htt_et_2_2016=htt_et_2_2016.txt htt_et_3_2016=htt_et_3_2016.txt htt_et_4_2016=htt_et_4_2016.txt htt_et_5_2016=htt_et_5_2016.txt htt_et_6_2016=htt_et_6_2016.txt htt_et_7_2016=htt_et_7_2016.txt htt_et_8_2016=htt_et_8_2016.txt htt_et_9_2016=htt_et_9_2016.txt htt_et_10_2016=htt_et_10_2016.txt htt_et_1_2017=htt_et_1_2017.txt htt_et_2_2017=htt_et_2_2017.txt htt_et_3_2017=htt_et_3_2017.txt htt_et_4_2017=htt_et_4_2017.txt htt_et_5_2017=htt_et_5_2017.txt htt_et_6_2017=htt_et_6_2017.txt htt_et_7_2017=htt_et_7_2017.txt htt_et_8_2017=htt_et_8_2017.txt htt_et_9_2017=htt_et_9_2017.txt htt_et_10_2017=htt_et_10_2017.txt htt_et_1_2018=htt_et_1_2018.txt htt_et_2_2018=htt_et_2_2018.txt htt_et_3_2018=htt_et_3_2018.txt htt_et_4_2018=htt_et_4_2018.txt htt_et_5_2018=htt_et_5_2018.txt htt_et_6_2018=htt_et_6_2018.txt htt_et_7_2018=htt_et_7_2018.txt htt_et_8_2018=htt_et_8_2018.txt htt_et_9_2018=htt_et_9_2018.txt htt_et_10_2018=htt_et_10_2018.txt  &> combined_test_cmb_et_years.txt.cmb

combineCards.py htt_mt_1_2016=htt_mt_1_2016.txt htt_mt_2_2016=htt_mt_2_2016.txt htt_mt_3_2016=htt_mt_3_2016.txt htt_mt_4_2016=htt_mt_4_2016.txt htt_mt_5_2016=htt_mt_5_2016.txt htt_mt_6_2016=htt_mt_6_2016.txt htt_mt_7_2016=htt_mt_7_2016.txt htt_mt_8_2016=htt_mt_8_2016.txt htt_mt_9_2016=htt_mt_9_2016.txt htt_mt_10_2016=htt_mt_10_2016.txt htt_mt_1_2017=htt_mt_1_2017.txt htt_mt_2_2017=htt_mt_2_2017.txt htt_mt_3_2017=htt_mt_3_2017.txt htt_mt_4_2017=htt_mt_4_2017.txt htt_mt_5_2017=htt_mt_5_2017.txt htt_mt_6_2017=htt_mt_6_2017.txt htt_mt_7_2017=htt_mt_7_2017.txt htt_mt_8_2017=htt_mt_8_2017.txt htt_mt_9_2017=htt_mt_9_2017.txt htt_mt_10_2017=htt_mt_10_2017.txt htt_mt_1_2018=htt_mt_1_2018.txt htt_mt_2_2018=htt_mt_2_2018.txt htt_mt_3_2018=htt_mt_3_2018.txt htt_mt_4_2018=htt_mt_4_2018.txt htt_mt_5_2018=htt_mt_5_2018.txt htt_mt_6_2018=htt_mt_6_2018.txt htt_mt_7_2018=htt_mt_7_2018.txt htt_mt_8_2018=htt_mt_8_2018.txt htt_mt_9_2018=htt_mt_9_2018.txt htt_mt_10_2018=htt_mt_10_2018.txt &> combined_test_cmb_mt_years.txt.cmb

combineCards.py htt_tt_1_2016=htt_tt_1_2016.txt htt_tt_2_2016=htt_tt_2_2016.txt htt_tt_3_2016=htt_tt_3_2016.txt htt_tt_4_2016=htt_tt_4_2016.txt htt_tt_5_2016=htt_tt_5_2016.txt htt_tt_6_2016=htt_tt_6_2016.txt htt_tt_7_2016=htt_tt_7_2016.txt htt_tt_8_2016=htt_tt_8_2016.txt htt_tt_9_2016=htt_tt_9_2016.txt htt_tt_10_2016=htt_tt_10_2016.txt htt_tt_1_2017=htt_tt_1_2017.txt htt_tt_2_2017=htt_tt_2_2017.txt htt_tt_3_2017=htt_tt_3_2017.txt htt_tt_4_2017=htt_tt_4_2017.txt htt_tt_5_2017=htt_tt_5_2017.txt htt_tt_6_2017=htt_tt_6_2017.txt htt_tt_7_2017=htt_tt_7_2017.txt htt_tt_8_2017=htt_tt_8_2017.txt htt_tt_9_2017=htt_tt_9_2017.txt htt_tt_10_2017=htt_tt_10_2017.txt htt_tt_1_2018=htt_tt_1_2018.txt htt_tt_2_2018=htt_tt_2_2018.txt htt_tt_3_2018=htt_tt_3_2018.txt htt_tt_4_2018=htt_tt_4_2018.txt htt_tt_5_2018=htt_tt_5_2018.txt htt_tt_6_2018=htt_tt_6_2018.txt htt_tt_7_2018=htt_tt_7_2018.txt htt_tt_8_2018=htt_tt_8_2018.txt htt_tt_9_2018=htt_tt_9_2018.txt htt_tt_10_2018=htt_tt_10_2018.txt &> combined_test_cmb_tt_years.txt.cmb

combineCards.py htt_em_1_2016=htt_em_1_2016.txt htt_em_2_2016=htt_em_2_2016.txt htt_em_3_2016=htt_em_3_2016.txt htt_em_4_2016=htt_em_4_2016.txt htt_em_5_2016=htt_em_5_2016.txt htt_em_6_2016=htt_em_6_2016.txt htt_em_7_2016=htt_em_7_2016.txt htt_em_8_2016=htt_em_8_2016.txt htt_em_9_2016=htt_em_9_2016.txt htt_em_10_2016=htt_em_10_2016.txt htt_em_1_2017=htt_em_1_2017.txt htt_em_2_2017=htt_em_2_2017.txt htt_em_3_2017=htt_em_3_2017.txt htt_em_4_2017=htt_em_4_2017.txt htt_em_5_2017=htt_em_5_2017.txt htt_em_6_2017=htt_em_6_2017.txt htt_em_7_2017=htt_em_7_2017.txt htt_em_8_2017=htt_em_8_2017.txt htt_em_9_2017=htt_em_9_2017.txt htt_em_10_2017=htt_em_10_2017.txt htt_em_1_2018=htt_em_1_2018.txt htt_em_2_2018=htt_em_2_2018.txt htt_em_3_2018=htt_em_3_2018.txt htt_em_4_2018=htt_em_4_2018.txt htt_em_5_2018=htt_em_5_2018.txt htt_em_6_2018=htt_em_6_2018.txt htt_em_7_2018=htt_em_7_2018.txt htt_em_8_2018=htt_em_8_2018.txt htt_em_9_2018=htt_em_9_2018.txt htt_em_10_2018=htt_em_10_2018.txt  htt_et_1_2016=htt_et_1_2016.txt htt_et_2_2016=htt_et_2_2016.txt htt_et_3_2016=htt_et_3_2016.txt htt_et_4_2016=htt_et_4_2016.txt htt_et_5_2016=htt_et_5_2016.txt htt_et_6_2016=htt_et_6_2016.txt htt_et_7_2016=htt_et_7_2016.txt htt_et_8_2016=htt_et_8_2016.txt htt_et_9_2016=htt_et_9_2016.txt htt_et_10_2016=htt_et_10_2016.txt htt_et_1_2017=htt_et_1_2017.txt htt_et_2_2017=htt_et_2_2017.txt htt_et_3_2017=htt_et_3_2017.txt htt_et_4_2017=htt_et_4_2017.txt htt_et_5_2017=htt_et_5_2017.txt htt_et_6_2017=htt_et_6_2017.txt htt_et_7_2017=htt_et_7_2017.txt htt_et_8_2017=htt_et_8_2017.txt htt_et_9_2017=htt_et_9_2017.txt htt_et_10_2017=htt_et_10_2017.txt htt_et_1_2018=htt_et_1_2018.txt htt_et_2_2018=htt_et_2_2018.txt htt_et_3_2018=htt_et_3_2018.txt htt_et_4_2018=htt_et_4_2018.txt htt_et_5_2018=htt_et_5_2018.txt htt_et_6_2018=htt_et_6_2018.txt htt_et_7_2018=htt_et_7_2018.txt htt_et_8_2018=htt_et_8_2018.txt htt_et_9_2018=htt_et_9_2018.txt htt_et_10_2018=htt_et_10_2018.txt  htt_mt_1_2016=htt_mt_1_2016.txt htt_mt_2_2016=htt_mt_2_2016.txt htt_mt_3_2016=htt_mt_3_2016.txt htt_mt_4_2016=htt_mt_4_2016.txt htt_mt_5_2016=htt_mt_5_2016.txt htt_mt_6_2016=htt_mt_6_2016.txt htt_mt_7_2016=htt_mt_7_2016.txt htt_mt_8_2016=htt_mt_8_2016.txt htt_mt_9_2016=htt_mt_9_2016.txt htt_mt_10_2016=htt_mt_10_2016.txt htt_mt_1_2017=htt_mt_1_2017.txt htt_mt_2_2017=htt_mt_2_2017.txt htt_mt_3_2017=htt_mt_3_2017.txt htt_mt_4_2017=htt_mt_4_2017.txt htt_mt_5_2017=htt_mt_5_2017.txt htt_mt_6_2017=htt_mt_6_2017.txt htt_mt_7_2017=htt_mt_7_2017.txt htt_mt_8_2017=htt_mt_8_2017.txt htt_mt_9_2017=htt_mt_9_2017.txt htt_mt_10_2017=htt_mt_10_2017.txt htt_mt_1_2018=htt_mt_1_2018.txt htt_mt_2_2018=htt_mt_2_2018.txt htt_mt_3_2018=htt_mt_3_2018.txt htt_mt_4_2018=htt_mt_4_2018.txt htt_mt_5_2018=htt_mt_5_2018.txt htt_mt_6_2018=htt_mt_6_2018.txt htt_mt_7_2018=htt_mt_7_2018.txt htt_mt_8_2018=htt_mt_8_2018.txt htt_mt_9_2018=htt_mt_9_2018.txt htt_mt_10_2018=htt_mt_10_2018.txt  htt_tt_1_2016=htt_tt_1_2016.txt htt_tt_2_2016=htt_tt_2_2016.txt htt_tt_3_2016=htt_tt_3_2016.txt htt_tt_4_2016=htt_tt_4_2016.txt htt_tt_5_2016=htt_tt_5_2016.txt htt_tt_6_2016=htt_tt_6_2016.txt htt_tt_7_2016=htt_tt_7_2016.txt htt_tt_8_2016=htt_tt_8_2016.txt htt_tt_9_2016=htt_tt_9_2016.txt htt_tt_10_2016=htt_tt_10_2016.txt htt_tt_1_2017=htt_tt_1_2017.txt htt_tt_2_2017=htt_tt_2_2017.txt htt_tt_3_2017=htt_tt_3_2017.txt htt_tt_4_2017=htt_tt_4_2017.txt htt_tt_5_2017=htt_tt_5_2017.txt htt_tt_6_2017=htt_tt_6_2017.txt htt_tt_7_2017=htt_tt_7_2017.txt htt_tt_8_2017=htt_tt_8_2017.txt htt_tt_9_2017=htt_tt_9_2017.txt htt_tt_10_2017=htt_tt_10_2017.txt htt_tt_1_2018=htt_tt_1_2018.txt htt_tt_2_2018=htt_tt_2_2018.txt htt_tt_3_2018=htt_tt_3_2018.txt htt_tt_4_2018=htt_tt_4_2018.txt htt_tt_5_2018=htt_tt_5_2018.txt htt_tt_6_2018=htt_tt_6_2018.txt htt_tt_7_2018=htt_tt_7_2018.txt htt_tt_8_2018=htt_tt_8_2018.txt htt_tt_9_2018=htt_tt_9_2018.txt htt_tt_10_2018=htt_tt_10_2018.txt &> combined_test_cmb_emetmttt_years.txt.cmb      
    """.format(inputString=inputString,par=par)

signal_model=""
if par=="fa3":
    # signal_model="FA3_Interference_JHU_ggHSyst_rw_MengsMuV_HeshyXsec_ggHInt"
    signal_model="FA3_Interference_JHU_ggHSyst_rw_MengsMuV"
elif par=="fa2":
    signal_model="FA2_Interference_JHU_rw_MengsMuV"
elif par=="fL1":
    signal_model="FL1_Interference_JHU_rw_MengsMuV"
elif par=="fL1Zg":
    signal_model="FL1Zg_Interference_JHU_rw_MengsMuV"

cmd+="""

ulimit -s unlimited

text2workspace.py -P HiggsAnalysis.CombinedLimit.{signal_model}:{signal_model} -o fa03_Workspace_MengsMuV_cmb_em_years.root -m 125 combined_test_cmb_em_years.txt.cmb
text2workspace.py -P HiggsAnalysis.CombinedLimit.{signal_model}:{signal_model} -o fa03_Workspace_MengsMuV_cmb_et_years.root -m 125 combined_test_cmb_et_years.txt.cmb
text2workspace.py -P HiggsAnalysis.CombinedLimit.{signal_model}:{signal_model} -o fa03_Workspace_MengsMuV_cmb_mt_years.root -m 125 combined_test_cmb_mt_years.txt.cmb
text2workspace.py -P HiggsAnalysis.CombinedLimit.{signal_model}:{signal_model} -o fa03_Workspace_MengsMuV_cmb_tt_years.root -m 125 combined_test_cmb_tt_years.txt.cmb
text2workspace.py -P HiggsAnalysis.CombinedLimit.{signal_model}:{signal_model} -o fa03_Workspace_MengsMuV_cmb_emetmttt_years.root -m 125 combined_test_cmb_emetmttt_years.txt.cmb

""".format(inputString=inputString,par=par,signal_model=signal_model)

cmd+="""

cd ../..

# combineTool.py -n 1D_scan_cmb_em_years -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:CMS_zz4l_fai1=-0.1,0.1 cmb/125/fa03_Workspace_MengsMuV_cmb_em_years.root --algo=grid --points=11 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo "Minuit2,0:1." --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1. -t -1 --expectSignal=1

# combineTool.py -n 1D_scan_cmb_et_years -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:CMS_zz4l_fai1=-0.1,0.1 cmb/125/fa03_Workspace_MengsMuV_cmb_et_years.root --algo=grid --points=11 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo "Minuit2,0:1." --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1. -t -1 --expectSignal=1

# combineTool.py -n 1D_scan_cmb_mt_years -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:CMS_zz4l_fai1=-0.1,0.1 cmb/125/fa03_Workspace_MengsMuV_cmb_mt_years.root --algo=grid --points=11 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo "Minuit2,0:1." --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1. -t -1 --expectSignal=1

# combineTool.py -n 1D_scan_cmb_tt_years -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:CMS_zz4l_fai1=-0.1,0.1 cmb/125/fa03_Workspace_MengsMuV_cmb_tt_years.root --algo=grid --points=11 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo "Minuit2,0:1." --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1. -t -1 --expectSignal=1


# combineTool.py -n 1D_scan_cmb_chn_years -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:CMS_zz4l_fai1=-0.1,0.1 cmb/125/fa03_Workspace_MengsMuV_cmb_emetmttt_years.root --algo=grid --points=11 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo "Minuit2,0:1." --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1. -t -1 --expectSignal=1


""".format(inputString=inputString,par=par)

print " >>>> writing commands to %s >>> execute: source  %s"%(outputFile,outputFile)
f_out.write(cmd)
f_out.close()
