#!/usr/bin/env python
import ROOT
from ROOT import *
import re
from array import array

import operator
import sys

import argparse
parser = argparse.ArgumentParser("Prepare datacards and run limits")

parser.add_argument(
        "--isGGH",
        action="store",
        dest="isGGH",
        default=0,
        help="Is this ggH measurement (0/1) ?")
parser.add_argument(
        "--path_datacard",
        action="store",
        dest="path_datacard",
        default="",
        help="Path to your datacard?")
parser.add_argument(
        "--name_datacard",
        action="store",
        dest="name_datacard",
        default="",
        help="Datacard name ?")

args = parser.parse_args()
isGGH=int(args.isGGH)
path_datacard=args.path_datacard
name_datacard=args.name_datacard

print " isGGH= ",isGGH
if isGGH==0:
    print "isGGH==0"
elif isGGH==1:
    print "isGGH==1"
else:
    print " is ggh wrong"

if path_datacard!="":
	filename_1 = path_datacard+"/"+name_datacard
else:
	filename_1 = name_datacard

filename_out=filename_1.replace(".root","")
filename_out=filename_out+"_DCPsym.root"

file=ROOT.TFile(filename_1,"r")
file1=ROOT.TFile(filename_out,"recreate")

print "output name: %s"%file1

file.cd()
dirList = gDirectory.GetListOfKeys()

def set_negative_bins_to_0(histo):
    #print " --------->>>>  N bins= %s"%(histo.GetSize())
    for bin in range(1,histo.GetSize()):
        if histo.GetBinContent(bin)<0:
            histo.SetBinContent(bin,0.)
    return histo
    

# loop over dirs (0jet/boosted/symetrized):
for k1 in dirList:

    #print "\n ===> dir %s"%(k1.GetName())
    # do nothing if 0jet/boosted dir: just save histos into new root file:
    if "0jet" in k1.GetName() or "boost" in k1.GetName():
        h1 = k1.ReadObj()
        nom=k1.GetName()
        #print "\nmaking dir %s"%(nom)
        file1.mkdir(nom)
        #print " bkg DCP_plus: ", k1.GetName(), "  -> output: ", nom
        h1.cd()
        histoList = gDirectory.GetListOfKeys()
        for k2 in histoList:
            h2 = k2.ReadObj()
            h3=h2.Clone()
            histo_name=k2.GetName()
            if "DO_NOT_USE" in histo_name or "_vbf_ac_" in histo_name or "data_obs_data" in histo_name:
                continue
            #print "\n====> just save %s  %s"%(nom,histo_name)

            file1.cd(nom)
            h3.SetName(k2.GetName())
	    h3=set_negative_bins_to_0(h3)
            h3.Write()

    # do nothing for data:
    if "DCPp" in k1.GetName():
        if "bin5" in k1.GetName() or "bin6" in k1.GetName() or "bin7" in k1.GetName() or "bin8" in k1.GetName() or "bin9" in k1.GetName() or "bin10" in k1.GetName()  or "bin11" in k1.GetName() or "bin12" in k1.GetName():
                continue

        h1 = k1.ReadObj()
        nom=k1.GetName()
        #print "making dir 2 %s"%(nom)
        file1.mkdir(nom)
        h1.cd()
        histoList = gDirectory.GetListOfKeys()
        for k2 in histoList:
            
            h2 = k2.ReadObj()
            h3=h2.Clone()
            #h3.Sumw2()
            histo_name=k2.GetName()
            if histo_name=="data_obs":
                file1.cd(nom)
                h3.SetName(k2.GetName())
                h3.Write()
                #print "\n====> just save %s  %s"%(nom,histo_name)

    # symetrize all except int and data in DCP bins:
    if "DCPm" in k1.GetName():
        if "bin5" in k1.GetName() or "bin6" in k1.GetName() or "bin7" in k1.GetName() or "bin8" in k1.GetName() or "bin9" in k1.GetName() or "bin10" in k1.GetName()  or "bin11" in k1.GetName() or "bin12" in k1.GetName():
                continue
        h1 = k1.ReadObj()
        nom=k1.GetName()
        #print "making dir 2 %s"%(nom)
        file1.mkdir(nom)
        nom_p=nom.replace("DCPm","DCPp")
        #print "making dir 3 %s"%(nom)
        file1.mkdir(nom_p)
        #print " bkg DCP_plus: ", k1.GetName(), "  -> output: ", nom_p
        h1.cd()
        histoList = gDirectory.GetListOfKeys()
        for k2 in histoList:
            
            h2 = k2.ReadObj()
            h3=h2.Clone()
            #h3.Sumw2()
            histo_name=k2.GetName()

            if histo_name=="data_obs":
                file1.cd(nom)
                h3.SetName(k2.GetName())
                h3.Write()
                #print "\n====> just save %s  %s"%(nom,histo_name)
                
            
            if "DO_NOT_USE" in histo_name or "_vbf_ac_" in histo_name  or "data_obs" in histo_name:
                continue

            '''
            if (("0Mf05ph0125" in histo_name) and ("WH" in histo_name or "ZH" in histo_name or "qqH" in histo_name) and isGGH==0):
                continue
            if (("0Mf05ph0125" in histo_name) and ("GGH" in histo_name) and isGGH==1):
                continue
            '''
            '''
            if (("0Mf05ph0125" in histo_name) and ("WH" in histo_name or "ZH" in histo_name or "qqH" in histo_name)):
                continue
            '''
            if (("0Mf05ph0125" in histo_name) and ("WH" in histo_name or "ZH" in histo_name or "qqH" in histo_name) and (isGGH==0)):
                continue
            elif (("Mf05ph0125" in histo_name) and ("GGH" in histo_name) and (isGGH==1)):
                continue

            
            #print "\n====> sym for  %s"%(histo_name)
            # now read same histo from DCPp and sum them up and divide by 2 --> simetrize
            file.cd(nom.replace("DCPm","DCPp"))
            h3_c_p=gDirectory.Get(k2.GetName())
            h3_p=h3_c_p.Clone()
            #print "\n====> sym for  %s"%(histo_name)
            #print " DCPm histo: %s, yield: %s    min: %s"%(histo_name,h3.Integral(),h3.GetMinimum())
            #print " DCPp histo: %s, yield: %s    min: %s"%(histo_name,h3_p.Integral(),h3_p.GetMinimum())
            
            h3.Add(h3_p)
            h3.Scale(0.5)

            # now save symetrized histo to DCPm and DCPp dirs in the output file:
            file1.cd(nom)
            h3.SetName(k2.GetName())
            h3=set_negative_bins_to_0(h3)
            h3.Write()
            #print "\n====>  save sym %s  %s"%(nom,histo_name)
            #print " ===>  DCPm histo: %s, yield sym: %s    min: %s"%(histo_name,h3.Integral(),h3.GetMinimum())
            #print " ===>  DCPp histo: %s, yield sym: %s    min: %s"%(histo_name,h3.Integral(),h3.GetMinimum())

            file1.cd(nom_p)
            h3.SetName(k2.GetName())
            h3.Write()
            #print "\n====>  save sym %s  %s"%(nom_p,histo_name)
        
# loop over dirs (anti-symetrized):
for k1 in dirList:
    
    #print "\n ===> dir %s"%(k1.GetName())
    # anti-symetrize int in DCP bins:
    if "DCPm" in k1.GetName():
	if "bin5" in k1.GetName() or "bin6" in k1.GetName() or "bin7" in k1.GetName() or "bin8" in k1.GetName() or "bin9" in k1.GetName() or "bin10" in k1.GetName()  or "bin11" in k1.GetName() or "bin12" in k1.GetName():
		continue
        h1 = k1.ReadObj()
        nom=k1.GetName()
        nom_p=nom.replace("DCPm","DCPp")
        h1.cd()
        histoList = gDirectory.GetListOfKeys()
        for k2 in histoList:
            
            h2 = k2.ReadObj()
            h3_m=h2.Clone()
            histo_name=k2.GetName()

            '''
            if not (("0Mf05ph0125" in histo_name) and ("WH" in histo_name or "ZH" in histo_name or "qqH" in histo_name) and isGGH==0):
                continue
            if not (("0Mf05ph0125" in histo_name) and ("GGH" in histo_name) and isGGH==1):
                continue
            '''
            '''
            if not (("0Mf05ph0125" in histo_name) and ("WH" in histo_name or "ZH" in histo_name or "qqH" in histo_name)):
                continue
            '''
            if isGGH==0:
                if not (("0Mf05ph0125" in histo_name) and ("WH" in histo_name or "ZH" in histo_name or "qqH" in histo_name)):
                    continue
            else:
                if not (("Mf05ph0125" in histo_name) and ("GGH" in histo_name )):
                    continue

            
            if "DO_NOT_USE" in histo_name or "_vbf_ac_" in histo_name  or "data_obs" in histo_name:
                continue
            #print "\n====> anti-sym for  %s"%(histo_name)
            #print "\n DCPm histo: %s, yield: %s    min: %s"%(histo_name,h3_m.Integral(),h3_m.GetMinimum())
            if isGGH==0: 
            	name_SM=histo_name.replace("0Mf05ph0125","0PM125")
            	name_PS=histo_name.replace("0Mf05ph0125","0M125")
            else:
                name_SM=histo_name.replace("reweighted_GGH2Jets_Mf05ph0125","reweighted_GGH2Jets_0PM125")
                name_PS=histo_name.replace("reweighted_GGH2Jets_Mf05ph0125","reweighted_GGH2Jets_0M125")

            # take SM and PS from symetrized dir:
            file1.cd(nom)            
            #print " %s from %s"%(name_SM,nom)
	    h3_c_SM_m=gDirectory.Get(name_SM)
            h3_SM_m=h3_c_SM_m.Clone()
            h3_c_PS_m=gDirectory.Get(name_PS)
            h3_PS_m=h3_c_PS_m.Clone()

            maxmix_m=h3_m.Clone()
            #print "\t place 1"
            maxmix_m.Add(h3_SM_m,0.5)
            maxmix_m.Add(h3_PS_m,0.5)

            #h3_m.Sumw2()

            
            # now read same histo from DCPp and sum them up and divide by 2 --> simetrize
            file.cd(nom_p)
            h3_c_p=gDirectory.Get(histo_name)
            h3_p=h3_c_p.Clone()

            #print " DCPp histo: %s, yield: %s    min: %s"%(histo_name,h3_p.Integral(),h3_p.GetMinimum())

            # take SM and PS from symetrized dir:
            #print "\t place 1a"
            file1.cd(nom_p)
            #print gDirectory.ls()
            #print "looking for: %s"%(name_SM)
            h3_c_SM_p=gDirectory.Get(name_SM)
            #print " yield %s"%(h3_c_SM_p.Integral())
            h3_SM_p=h3_c_SM_p.Clone()
            #print "  yield 2 %s"%(h3_SM_p.Integral())
            h3_c_PS_p=gDirectory.Get(name_PS)
            h3_PS_p=h3_c_PS_p.Clone()

            #print "\t place 1b"
            maxmix_p=h3_p.Clone()
            #print "   yield 3 %s"%(maxmix_p.Integral())
            #print "\t place 1c"
            maxmix_p.Add(h3_SM_p,0.5)
            #print "\t place 1d"
            maxmix_p.Add(h3_PS_p,0.5)

            #print "\t place 1e"
            antisym_int=maxmix_p.Clone()
            antisym_int.Add(maxmix_m,-1)
            antisym_int.Scale(0.5)

            #print "\t place 2"
            antisym_int_p=antisym_int.Clone()
            antisym_int_p.Add(h3_SM_p,0.5)
            antisym_int_p.Add(h3_PS_p,0.5)

            #print "\t place 3"
            antisym_int_m=antisym_int.Clone()
            antisym_int_m.Scale(-1)
            antisym_int_m.Add(h3_SM_m,0.5)
            antisym_int_m.Add(h3_PS_m,0.5)

            
            # now save symetrized histo to DCPm and DCPp dirs in the output file:
            file1.cd(nom)
            antisym_int_m.SetName(histo_name)
            antisym_int_m=set_negative_bins_to_0(antisym_int_m)
            antisym_int_m.Write()
            #print "\n====>  save anti-sym %s  %s"%(nom,histo_name)
            #print " ===>  DCPm histo: %s, yield anti-sym: %s    min: %s"%(histo_name,antisym_int_m.Integral(),antisym_int_m.GetMinimum())

            file1.cd(nom_p)
            antisym_int_p.SetName(histo_name)
            antisym_int_p=set_negative_bins_to_0(antisym_int_p)
            antisym_int_p.Write()
            #print "\n====>  save anti-sym %s  %s"%(nom_p,histo_name)
            #print " ===>  DCPp histo: %s, yield: anti-sym %s    min: %s"%(histo_name,antisym_int_p.Integral(),antisym_int_p.GetMinimum())
        

#file1.cd("tt_vbf_ggHMELA_bin4_DCPp")
#print "==================>>> tt_vbf_ggHMELA_bin4_DCPp"
#print gDirectory.ls()

#file1.cd("tt_vbf_ggHMELA_bin4_DCPm")
#print "==================>>> tt_vbf_ggHMELA_bin4_DCPm"
#print gDirectory.ls()
