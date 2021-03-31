import ROOT
from ROOT import *

import re
from array import array
from optparse import OptionParser
import sys

#parser = OptionParser()
import argparse
parser = argparse.ArgumentParser("Compare total template to stage 1.1 templates")
parser.add_argument(
        "--inputfile",
        action="store",
        dest="inputfile",
        default="X.root",
        help="Which file1name to run over?")
parser.add_argument(
        "--outputfile",
        action="store",
        dest="outputfile",
        default="Y.root",
        help="Which file1name to run over?")
args = parser.parse_args()

inputfile =args.inputfile
outputfile=args.outputfile

file=ROOT.TFile(inputfile,"r")
file.cd()
dirList = gDirectory.GetListOfKeys()

ofile=ROOT.TFile(outputfile,"recreate")
categories_list= file.GetListOfKeys()
categories=[]
for k2 in categories_list:
	categories.append(k2.GetName())
ncat=len(categories)
for k1 in dirList: # loop over categories

    names_histos_used=[]

    h1 = k1.ReadObj()
    nom=k1.GetName()
    ofile.mkdir(nom)
    h1.cd()
    histoList = gDirectory.GetListOfKeys()
    name_last=""
    N_histo=0

    for histo in histoList:
        h1.cd()
        h2 = histo.ReadObj()
        h3=h2.Clone()
        histo_name=h2.GetName()
        if (h2.GetName()==name_last):
            continue
        name_last=histo_name
        if 'reweighted_ggH' in histo_name:
            histo_name=histo_name.replace('reweighted_ggH_htt_0PM','GGH2Jets_sm_M')
            histo_name=histo_name.replace('reweighted_ggH_htt_0Mf05ph0','GGH2Jets_pseudoscalar_Mf05ph0')
            histo_name=histo_name.replace('reweighted_ggH_htt_0M','GGH2Jets_pseudoscalar_M')
        ofile.cd(nom)
        h3.Write(histo_name)
