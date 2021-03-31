import ROOT
from ROOT import *
import re
from array import array

import operator
import sys

import argparse
parser = argparse.ArgumentParser("Compare total template to stage 1.1 templates")
parser.add_argument(
        "--par",
        action="store",
        dest="par",
        default="fa3",
        help="Which channel is this ?")
parser.add_argument(
        "--inputFile",
        action="store",
        dest="inputFile",
        default="file.root",
        help="Which channel is this ?")
args = parser.parse_args()

par=args.par #
inputFile=args.inputFile #

file=ROOT.TFile(inputFile,"r")
filename_out=inputFile.replace(".root","_renamed.root")
file1=ROOT.TFile(filename_out,"recreate")


file.cd()
dirList = gDirectory.GetListOfKeys()

print " ====> %s"%(par)
print " ====> %s"%(inputFile)

#if (par!="fa2" and par!="fL1" and par!="fL1Zg"):
#    print "   ===> this is not fa2/fL1/fL1Zg => NO RENAMING"
#    sys.exit(0)
#else:
#    print "   ===> this is fa2/fL1/fL1Zg => rename..."


for k1 in dirList:
    #print "\n signal DCP_minus: ", k1.GetName()
    h1 = k1.ReadObj()
    nom=k1.GetName()
    file1.mkdir(nom)
    print " ===> renaming ... %s"%(nom)
    #file.cd(nom)

    h1.cd()
    histoList = gDirectory.GetListOfKeys()
    #print " =====> histos ... %s"%(histoList)
    file.cd(nom)

    for k2 in histoList:
        h2 = k2.ReadObj()
        h3=h2.Clone()
        histo_name=k2.GetName()
        #print " ===> histo ... %s"%(histo_name)
 
	if "0M" in histo_name and ("WH" in histo_name or "ZH" in histo_name or "qqH" in histo_name):
		continue

        if par=="fa2":
            #print " ====> par is fa2 %s !!!!!!!!"%(histo_name)  
            histo_name=histo_name.replace("0PH","0M")
            #print " =======> new name %s !!!!!!!!"%(histo_name)            
        elif par=="fL1":
            histo_name=histo_name.replace("0L1","0M")
        elif par=="fL1Zg":
            histo_name=histo_name.replace("0L1Zg","0M")
        h3.SetName(histo_name)
        file1.cd(nom)
        #print " save in dir %s as %s"%(nom,histo_name)
        h3.Write()
        if par=="fL1Zg" and "reweighted_WH_htt_0PM125" in histo_name:
	    name_WH_fL1Zg=histo_name.replace("reweighted_WH_htt_0PM125","reweighted_WH_htt_0M125")
            h3.Write(name_WH_fL1Zg)
            name_WH_fL1Zg_2=histo_name.replace("reweighted_WH_htt_0PM125","reweighted_WH_htt_0Mf05ph0125")
            h3.Write(name_WH_fL1Zg_2)


    print " ==> done"
        
