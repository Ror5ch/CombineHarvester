#!/usr/bin/env python
import ROOT
from ROOT import *
import re
from array import array
from optparse import OptionParser
import math
import numpy as np

import operator
import sys


parser = OptionParser()
parser.add_option('--input', '-i', action='store',
                  default="./HTTAC2017/shapes/USCMS/htt_tt.inputs-sm-13TeV-2D_tt2016_baseline-with-msv_Meng_vbfTrain_NOtoss.root", dest='filename_in',
                  help='input filename'
                  )
parser.add_option('--output', '-o', action='store',
                  default="tests.root", dest='filename_out',
                  help='output filename'
                  )
parser.add_option('--chn', '-c', action='store',
                  default="tt", dest='chn',
                  help='output filename'
                  )
parser.add_option('--par', '-u', action='store',
                  default="a3", dest='par',
                  help='parameters'
                  )
parser.add_option('--do_ggh_int', '-g', action='store',
                  default="0", dest='do_ggh_int',
                  help='do ggH signal model with interference'
                  )
parser.add_option('--print', '-p', action='store',
                  default="0", dest='do_print',
                  help='do print '
                  )
parser.add_option('--sync', '-s', action='store',
                  default="0", dest='sync',
                  help='use sync bkg '
                  )
parser.add_option('--useSingleVBFdir', '-v', action='store',
                  default="0", dest='useSingleVBFdir',
                  help='use single VBF dir '
                  )
(options, args) = parser.parse_args()


filename_out = options.filename_out
filename_in = options.filename_in
chn=options.chn
par=options.par
sync=int(options.sync)
useSingleVBFdir=int(options.useSingleVBFdir)

print "options.do_ggh_int=%s"%(options.do_ggh_int)
if int(options.do_ggh_int)==0:
    print "\t================\t using ggH signal model WITHOUT intreference !"
if int(options.do_ggh_int)==1:
    print "\t================\t using ggH signal model WITH intreference !"


islog=1
unrollSV=1

file=ROOT.TFile(filename_in,"r")
file.cd()
dirList = gDirectory.GetListOfKeys()

file1=ROOT.TFile(filename_out,"recreate")


# histogram names:
name_SM_qqH_powheg="VBF125"
name_SM_qqH_JHU="reweighted_qqH_htt_0PM125"
name_PS_qqH_JHU="reweighted_qqH_htt_0M125"
name_int_qqH_JHU="reweighted_qqH_htt_0Mf05ph0125"

name_SM_WH_powheg="WH125"
name_SM_WH_JHU="reweighted_WH_htt_0PM125"
name_PS_WH_JHU="reweighted_WH_htt_0M125"
name_int_WH_JHU="reweighted_WH_htt_0Mf05ph0125"

name_SM_ZH_powheg="ZH125"
name_SM_ZH_JHU="reweighted_ZH_htt_0PM125"
name_PS_ZH_JHU="reweighted_ZH_htt_0M125"
name_int_ZH_JHU="reweighted_ZH_htt_0Mf05ph0125"

name_SM_ggH_powheg="ggH125"
name_SM_ggH_JHU="GGH2Jets_sm_M125"
name_PS_ggH_JHU="GGH2Jets_pseudoscalar_M125"
name_int_ggH_JHU="GGH2Jets_pseudoscalar_Mf05ph0125"

# define bkg names to calculate total bkg:
name_bkg=[]
if chn=='et' or chn=='mt':
    name_bkg=["embedded", "ZL", "TTT", "VVT", "jetFakes","STT", "STL", "TTL", "VVL" ]
elif chn=='em':
    #name_bkg=["embedded","W","QCD","ZLL","TT","VV","EWKZ","ZJ"]
    name_bkg=["embedded","W","QCD","ZLL","TT","VV"]
    #name_bkg=["embedded","W","QCD","ZLL","TT","VV","EWKZ"]
if sync:
    name_bkg=["embed", "ZL", "TTT", "VVT", "jetFakes"]
if sync and chn=='em':
    #name_bkg=["embed", "W","QCD","ZLL","TT","VV","EWKZ"]
    name_bkg=["embed", "W","QCD","ZLL","TT","VV"]

min_signal=0.06 # min signal/bkg below which we set signal to 0! 0.01->1%

sigma1_HZZ=290.58626
sigma3_HZZ=44.670158
sigma1_VBF=968.674
sigma3_VBF=10909.54
sigmaa1a3int_VBF=1937.15

if par=="fa2":
	print "\t using fa2_VBF xsections"
	sigma3_HZZ=105.85594
	sigma3_VBF=13102.71
	sigmaa1a3int_VBF=2207.73
if par=="fL1":
        print "\t using fL1_VBF xsections"
        sigma3_HZZ=1.9846071e-06
        sigma3_VBF=2.08309E-4
        sigmaa1a3int_VBF=2861.21349769
if par=="fL1Zg":
        print "\t using fL1Zg_VBF xsections"
        sigma3_HZZ=5.013e-06
        sigma3_VBF=4.9845301e-05
        sigmaa1a3int_VBF=1410.5494


sigma_Powheg_ggH=48.58
sigma1_ggH=15980
sigma3_ggH=15981


vbf_dir_names_stat=[]

# now define the directories that will be used:
## default: "*vbf_ggHMELA_bin*"
for k1 in dirList:
    #print "\n signal DCP_minus: ", k1.GetName()
    h1 = k1.ReadObj()
    nom=k1.GetName()
    if chn=='tt' and "tt_vbf_ggHMELA_bin" in nom:
        vbf_dir_names_stat.append(nom)
    if chn!='tt' and "_1_" not in nom and "_2_" not in nom:
        vbf_dir_names_stat.append(nom)

if useSingleVBFdir:
	vbf_dir_names_stat=["em_vbf"]


print " dirs: ",vbf_dir_names_stat
# fa3 points to evaluate signal model for:
fa3_VBF=[-1., -0.5, -0.01, -0.005, -0.004,-0.0015, -0.001, -0.0002, -0.0001, 0.,0.0001, 0.0002, 0.001,0.0015,0.004, 0.005, 0.01, 0.5, 1.]
fa3_ggH=[ 0.,0.0001, 0.01, 0.5, 1.]
fa3_with_neg_yields_ggH=[]
fa3_with_neg_yields_VBF=[]

negative_binsN_SM_ggH=0
negative_binsN_PS_ggH=0
negative_binsN_int_ggH=0
negative_binsN_SM_VBF=0
negative_binsN_PS_VBF=0
negative_binsN_int_VBF=0

for k1 in vbf_dir_names_stat:

    if int(options.do_print)==1:
       print "\n dir: ", k1    

    # get all used histograms:
    h_SM_ggH_JHU_c2=file.Get(k1).Get(name_SM_ggH_JHU)
    h_SM_ggH_JHU2=h_SM_ggH_JHU_c2.Clone()

    if par=="fa3":
    	h_PS_ggH_JHU_c2=file.Get(k1).Get(name_PS_ggH_JHU)
    	h_PS_ggH_JHU2=h_PS_ggH_JHU_c2.Clone()
    	if int(options.do_ggh_int)==1:
		#print " getting %s from %s %s"%(name_int_ggH_JHU,k1,filename_in)
    		h_int_ggH_JHU_c2=file.Get(k1).Get(name_int_ggH_JHU)
    		h_int_ggH_JHU2=h_int_ggH_JHU_c2.Clone()

    h_SM_qqH_JHU_c2=file.Get(k1).Get(name_SM_qqH_JHU)
    h_SM_qqH_JHU2=h_SM_qqH_JHU_c2.Clone()
    h_PS_qqH_JHU_c2=file.Get(k1).Get(name_PS_qqH_JHU)
    h_PS_qqH_JHU2=h_PS_qqH_JHU_c2.Clone()
    h_int_qqH_JHU_c2=file.Get(k1).Get(name_int_qqH_JHU)
    h_int_qqH_JHU2=h_int_qqH_JHU_c2.Clone()

    # get total bkg:
    total_bkg=h_SM_ggH_JHU2.Clone()
    total_bkg.Sumw2()
    total_bkg.Scale(0)
    for bkg_i in name_bkg:
	print " getting %s bkg %s"%(k1,bkg_i)
        if file.Get(k1).Get(bkg_i):
		print "   ... exists"
        	total_bkg.Add(file.Get(k1).Get(bkg_i))
    #print "total bkg yield= %s"%(total_bkg.Integral())
    

    # get min yield of all histograms:
    min_SM=file.Get(k1).Get(name_SM_ggH_JHU).GetMinimum()
    if par=="fa3":
    	min_PS=file.Get(k1).Get(name_PS_ggH_JHU).GetMinimum()
    	if int(options.do_ggh_int)==1:
    		min_int=file.Get(k1).Get(name_int_ggH_JHU).GetMinimum()
    min_SM_VBF=file.Get(k1).Get(name_SM_qqH_JHU).GetMinimum()
    min_PS_VBF=file.Get(k1).Get(name_PS_qqH_JHU).GetMinimum()
    min_int_VBF=file.Get(k1).Get(name_int_qqH_JHU).GetMinimum()

    # get min bin of all histograms:
    min_SM_bin=file.Get(k1).Get(name_SM_ggH_JHU).GetMinimumBin()
    if par=="fa3":
    	min_PS_bin=file.Get(k1).Get(name_PS_ggH_JHU).GetMinimumBin()
    	if int(options.do_ggh_int)==1:
    		min_int_bin=file.Get(k1).Get(name_int_ggH_JHU).GetMinimumBin()
    min_SM_VBF_bin=file.Get(k1).Get(name_SM_qqH_JHU).GetMinimumBin()
    min_PS_VBF_bin=file.Get(k1).Get(name_PS_qqH_JHU).GetMinimumBin()
    min_int_VBF_bin=file.Get(k1).Get(name_int_qqH_JHU).GetMinimumBin()

    # loop over bins and calculate ggH and VBF signal model for several fa3 points:
    for i in range(1,h_SM_ggH_JHU2.GetNbinsX()+1):
        if int(options.do_print)==1:
            print " bin %s"%(i)
        yield_i_SM_ggH=h_SM_ggH_JHU2.GetBinContent(i)
	yield_i_PS_ggH=0
	yield_i_int_ggH=0
	if par=="fa3":
        	yield_i_PS_ggH=h_PS_ggH_JHU2.GetBinContent(i)
        	if int(options.do_ggh_int)==1:
            		yield_i_int_ggH=h_int_ggH_JHU2.GetBinContent(i)

        yield_i_SM_VBF=h_SM_qqH_JHU2.GetBinContent(i)
        yield_i_PS_VBF=h_PS_qqH_JHU2.GetBinContent(i)
        yield_i_int_VBF=h_int_qqH_JHU2.GetBinContent(i)

        yield_bkg_i=total_bkg.GetBinContent(i)
        error_bkg_i=total_bkg.GetBinError(i)

        #if yield_bkg_i<=1.0:
	#	print "\t\t PROBLEM: %s BKG yield: bin %s   BKG is  %.2f +- %.2f ! "%(k1,i,yield_bkg_i,error_bkg_i)
        #print "\t\t PROBLEM: %s BKG yield: bin %s   BKG is  %.2f +- %.2f ! "%(k1,i,yield_bkg_i,error_bkg_i)
       
 
        if int(options.do_print)==1:
            if int(options.do_ggh_int)==0 and par=="fa3":
                print " ggH SM %.4f, PS %.4f"%(yield_i_SM_ggH,yield_i_PS_ggH)
            if int(options.do_ggh_int)==1 and par=="fa3":
                print " ggH SM %.4f, PS %.4f, int %.4f"%(yield_i_SM_ggH,yield_i_PS_ggH,yield_i_int_ggH)
            print " VBFH SM %.4f, PS %.4f, int %.4f"%(yield_i_SM_VBF,yield_i_PS_VBF,yield_i_int_VBF)
            print " VBFH SM %.4f, PS*Xsec %.4f, int*Xsec %.4f"%(yield_i_SM_VBF,yield_i_PS_VBF*sigma3_VBF/sigma1_VBF,yield_i_int_VBF*sigmaa1a3int_VBF/sigma1_VBF)

        for fa3_VBF_i in fa3_VBF:
            a1_VBF=math.sqrt(1-abs(fa3_VBF_i))
            muVc=1./(1.+300.*abs(fa3_VBF_i))
            a3_VBF=np.sign(fa3_VBF_i)*math.sqrt(abs(fa3_VBF_i)*sigma1_HZZ/sigma3_HZZ)
            y=sigma3_VBF/sigma1_VBF
            factor_SM_VBF=muVc*(a1_VBF**2-a1_VBF*a3_VBF*math.sqrt(y))
            factor_BSM_VBF=muVc*(a3_VBF**2*y-a1_VBF*a3_VBF*math.sqrt(y))
            factor_int_VBF=muVc*(a1_VBF*a3_VBF*math.sqrt(y)*sigmaa1a3int_VBF/sigma1_VBF)
            yield_bin_VBF=factor_SM_VBF*yield_i_SM_VBF+factor_BSM_VBF*yield_i_PS_VBF+factor_int_VBF*yield_i_int_VBF
            if (yield_bin_VBF<0):
                if fa3_VBF_i not in fa3_with_neg_yields_VBF:
                    fa3_with_neg_yields_VBF.append(fa3_VBF_i)
                print "\t\t WARNING: %s negative VBF SIGNAL MODEL yield: bin %s for fa3_VBF=%.4f: => yield_SM=%.4f  factor= %.4f| yield_PS=%.4f factor= %.4f| yield_int=%.4f factor= %.4f  => bin yield= %.4f"%(k1,i,fa3_VBF_i,yield_i_SM_VBF,factor_SM_VBF,yield_i_PS_VBF,factor_BSM_VBF,yield_i_int_VBF,factor_int_VBF,yield_bin_VBF)
		if yield_bkg_i!=0:
                	if yield_i_SM_VBF/yield_bkg_i<min_signal and yield_i_PS_VBF/yield_bkg_i<min_signal:
                    		print "\t\t\t \033[1;42m bkg yield %s => SM/B=%s PS/B=%s  ==> less than %s ok: set signal to 0!\033[0;m"%(yield_bkg_i,yield_i_SM_VBF/yield_bkg_i,yield_i_PS_VBF/yield_bkg_i,min_signal)
                    		h_SM_qqH_JHU2.SetBinContent(i,0.)
                    		h_PS_qqH_JHU2.SetBinContent(i,0.)
                    		h_int_qqH_JHU2.SetBinContent(i,0.)
                	else:
                    		print "\t\t\t \x1b[1;31m bkg yield %s => SM/B=%s PS/B=%s  ==> more than %s do not set signal to 0 !\x1b[0;m"%(yield_bkg_i,yield_i_SM_VBF/yield_bkg_i,yield_i_PS_VBF/yield_bkg_i,min_signal)
                else:
	                print "\t\t PROBLEM: %s BKG yield: bin %s   BKG is %.2f +- %.2f ! "%(k1,i,yield_bkg_i,error_bkg_i)

                
        for fa3_ggH_i in fa3_ggH:
            a1_ggH=math.sqrt(1-abs(fa3_ggH_i))
            muf=1.
            a3_ggH=math.sqrt(abs(fa3_ggH_i))
            y=sigma3_ggH/sigma1_ggH
	    yield_bin_ggH=0
            if int(options.do_print)==1:
                print "\t fa3ggH=%.4f, a1=%.4f, a3=%.4f"%(fa3_ggH_i, a1_ggH, a3_ggH)
            if int(options.do_ggh_int)==0 and par=="fa3":
                # do ggH signal model without intereference !
                factor_SM_ggH=muf*(a1_ggH**2)
                factor_BSM_ggH=muf*(a3_ggH**2)
                yield_bin_ggH=factor_SM_ggH*yield_i_SM_ggH+factor_BSM_ggH*yield_i_PS_ggH
            if int(options.do_ggh_int)==1  and par=="fa3":
                # do ggH signal model with intereference !
                factor_SM_ggH=muf*(a1_ggH**2-a1_ggH*a3_ggH*math.sqrt(y))
                factor_BSM_ggH=muf*(a3_ggH**2*y-a1_ggH*a3_ggH*math.sqrt(y))
                factor_int_ggH=muf*(a1_ggH*a3_ggH*math.sqrt(y)*2.)
                yield_bin_ggH=factor_SM_ggH*yield_i_SM_ggH+factor_BSM_ggH*yield_i_PS_ggH+factor_int_ggH*yield_i_int_ggH
                yield_i_SM_ggH+factor_BSM_ggH*yield_i_PS_ggH+factor_int_ggH*yield_i_int_ggH
            if int(options.do_print)==1:
                if int(options.do_ggh_int)==0 and par=="fa3":
                    print "\t\t factor_SM_ggH= %.4f, factor_PS_ggH= %.4f  => bin yield= %.4f"%(factor_SM_ggH,factor_BSM_ggH,yield_bin_ggH)
                    print "\t\t\t fa3_ggH=%.4f: => yield_SM_ggH=%.4f  factor= %.4f, yield_PS_ggH=%.4f factor= %.4f  => bin yield= %.4f"%(fa3_ggH_i, yield_i_SM_ggH,factor_SM_ggH,yield_i_PS_ggH,factor_BSM_ggH,yield_bin_ggH)
                if int(options.do_ggh_int)==1 and par=="fa3":
                    print "\t\t factor_SM_ggH= %.4f, factor_PS_ggH= %.4f, factor_int_ggH= %.4f  => bin yield= %.4f"%(factor_SM_ggH,factor_BSM_ggH,factor_int_ggH,yield_bin_ggH)
                    print "\t\t\t fa3_ggH=%.4f: => yield_SM_ggH=%.4f  factor= %.4f, yield_PS_ggH=%.4f factor= %.4f, yield_int_ggH=%.4f factor= %.4f  => bin yield= %.4f"%(fa3_ggH_i, yield_i_SM_ggH,factor_SM_ggH,yield_i_PS_ggH,factor_BSM_ggH,yield_i_int_ggH,factor_int_ggH,yield_bin_ggH)

            if (yield_bin_ggH<0) and par=="fa3":
                if fa3_ggH_i not in fa3_with_neg_yields_ggH:
                    fa3_with_neg_yields_ggH.append(fa3_ggH_i)
                if int(options.do_ggh_int)==0:
                    print "\t WARNING: negative GGH SIGNAL MODEL yield: bin %s for fa3_ggH=%.4f: => yield_SM=%.4f  factor= %.4f| yield_PS=%.4f factor= %.4f  => bin yield= %.4f"%(i,fa3_ggH_i, yield_i_SM_ggH,factor_SM_ggH,yield_i_PS_ggH,factor_BSM_ggH,yield_bin_ggH)
                    #print "\t\t\t bkg yield %s => SM/B=%s PS/B=%s "%(yield_bkg_i,yield_i_SM_ggH/yield_bkg_i,yield_i_PS_ggH/yield_bkg_i)
		    if yield_bkg_i!=0:
                    	if yield_i_SM_ggH/yield_bkg_i<min_signal and yield_i_PS_ggH/yield_bkg_i<min_signal:
                        	print "\t\t\t \033[1;42m bkg yield %s => SM/B=%s PS/B=%s  ==> less than %s ok: set signal to 0! \033[0;m"%(yield_bkg_i,yield_i_SM_ggH/yield_bkg_i,yield_i_PS_ggH/yield_bkg_i,min_signal)
                        	h_SM_ggH_JHU2.SetBinContent(i,0.)
                        	h_PS_ggH_JHU2.SetBinContent(i,0.)
				if int(options.do_ggh_int)==1:
                        		h_int_ggH_JHU2.SetBinContent(i,0.)
                        	#print FSAfolder + "\t\033[1;42m A.O.K \033[0;m"
                    	else:
                        	print "\t\t\t \x1b[1;31m bkg yield %s => SM/B=%s PS/B=%s  ==> more than %s do not set signal to 0 ! \x1b[0;m"%(yield_bkg_i,yield_i_SM_ggH/yield_bkg_i,yield_i_PS_ggH/yield_bkg_i,min_signal)
	        else:
                        print "\t\t PROBLEM: %s BKG yield: bin %s   BKG is %.2f +- %.2f ! "%(k1,i,yield_bkg_i,error_bkg_i)


                if int(options.do_ggh_int and yield_bkg_i>0)==1 and par=="fa3":
                    print "\t WARNING: negative GGH SIGNAL MODEL yield: bin %s for fa3_ggH=%.4f: => yield_SM=%.4f  factor= %.4f| yield_PS=%.4f factor= %.4f| yield_int=%.4f factor= %.4f  => bin yield= %.4f"%(i,fa3_ggH_i, yield_i_SM_ggH,factor_SM_ggH,yield_i_PS_ggH,factor_BSM_ggH,yield_i_int_ggH,factor_int_ggH,yield_bin_ggH)
                    #print "\t\t\t bkg yield %s => SM/B=%s PS/B=%s "%(yield_bkg_i,yield_i_SM_ggH/yield_bkg_i,yield_i_PS_ggH/yield_bkg_i)
                    if yield_i_SM_ggH/yield_bkg_i<min_signal and yield_i_PS_ggH/yield_bkg_i<min_signal:
                        print "\t\t\t \033[1;42m bkg yield %s => SM/B=%s PS/B=%s  ==> less than %s ok: set signal to 0! \033[0;m"%(yield_bkg_i,yield_i_SM_ggH/yield_bkg_i,yield_i_PS_ggH/yield_bkg_i,min_signal)
                        h_SM_ggH_JHU2.SetBinContent(i,0.)
                        h_PS_ggH_JHU2.SetBinContent(i,0.)
                        if int(options.do_ggh_int)==1:
                       	 	h_int_ggH_JHU2.SetBinContent(i,0.)
                    else:
                        print "\t\t\t \x1b[1;31m bkg yield %s => SM/B=%s PS/B=%s  ==> more than %s do not set signal to 0 ! \x1b[0;m"%(yield_bkg_i,yield_i_SM_ggH/yield_bkg_i,yield_i_PS_ggH/yield_bkg_i,min_signal)
               
        
        if yield_i_SM_ggH<0:
            negative_binsN_SM_ggH=negative_binsN_SM_ggH+1
        if yield_i_PS_ggH<0:
            negative_binsN_PS_ggH=negative_binsN_PS_ggH+1
        if int(options.do_ggh_int)==1:
            if yield_i_int_ggH<0:
                negative_binsN_int_ggH=negative_binsN_int_ggH+1

        if yield_i_SM_VBF<0:
            negative_binsN_SM_VBF=negative_binsN_SM_VBF+1
        if yield_i_PS_VBF<0:
            negative_binsN_PS_VBF=negative_binsN_PS_VBF+1
        if yield_i_int_VBF<0:
            negative_binsN_int_VBF=negative_binsN_int_VBF+1
    
    if int(options.do_ggh_int)==0 and par=="fa3":
        if (min_SM<0. or min_PS<0.):
            print "     WARNING: input GGH signal histogram has negative yields !!!!    SM min ggH: %s (bin %s), PS min ggH: %s (bin %s)"%(min_SM,min_SM_bin, min_PS, min_PS_bin)
    if int(options.do_ggh_int)==1 and par=="fa3":
        if (min_SM<0. or min_PS<0. or min_int<0.):
            print "     WARNING: input GGH signal histogram has negative yields !!!!    SM min ggH: %s (bin %s), PS min ggH: %s (bin %s), int min ggH: %s (bin %s)"%(min_SM,min_SM_bin, min_PS, min_PS_bin,min_int,min_int_bin)
    if (min_SM_VBF<0. or min_PS_VBF<0. or min_int_VBF<0.):
        print "     WARNING: input VBF signal histogram has negative yields !!!!    SM min VBF: %s (bin %s), PS min VBF: %s (bin %s), int min VBF: %s (bin %s)"%(min_SM_VBF,min_SM_VBF_bin, min_PS_VBF,min_PS_VBF_bin, min_int_VBF, min_int_VBF_bin)

    file1.mkdir(k1)
    file1.cd(k1)  

    h_SM_ggH_JHU2.SetName(name_SM_ggH_JHU)          
    if par=="fa3":
    	h_PS_ggH_JHU2.SetName(name_PS_ggH_JHU)      
    h_SM_qqH_JHU2.SetName(name_SM_qqH_JHU)
    h_PS_qqH_JHU2.SetName(name_PS_qqH_JHU)
    h_int_qqH_JHU2.SetName(name_int_qqH_JHU)
    h_SM_ggH_JHU2.Write()
    if par=="fa3":
    	h_PS_ggH_JHU2.Write()
    h_SM_qqH_JHU2.Write()
    h_PS_qqH_JHU2.Write()
    h_int_qqH_JHU2.Write()

    if int(options.do_ggh_int)==1 and par=="fa3":   
        h_int_ggH_JHU2.SetName(name_int_ggH_JHU) 
	#print " ===> writing ggH int %s to output %s!"%(h_int_ggH_JHU2.GetName(),k1)
        h_int_ggH_JHU2.Write()
        
file.cd()
dirList = gDirectory.GetListOfKeys()
for k1 in dirList:
    h1 = k1.ReadObj()
    nom=k1.GetName()
    nom_out=nom
    file1.mkdir(nom_out)
    
    h1.cd()
    histoList = gDirectory.GetListOfKeys()
    for k2 in histoList:
        #if ((k2.GetName()!=name_SM_ggH_JHU and k2.GetName()!=name_PS_ggH_JHU and k2.GetName()!=name_PS_qqH_JHU and k2.GetName()!=name_SM_qqH_JHU and k2.GetName()!=name_int_qqH_JHU) or ("vbf" not in nom)):
        if ((k2.GetName()!=name_SM_ggH_JHU and k2.GetName()!=name_PS_ggH_JHU and k2.GetName()!=name_PS_qqH_JHU and k2.GetName()!=name_SM_qqH_JHU and k2.GetName()!=name_int_qqH_JHU) or ("_1_" in nom or "_2_" in nom)):

            #if int(options.do_ggh_int)==1 and k2.GetName()==name_int_ggH_JHU and "vbf" in nom:
            if int(options.do_ggh_int)==1 and k2.GetName()==name_int_ggH_JHU and ("_1_" not in nom and "_2_" not in nom):

                continue
                
            h2 = k2.ReadObj()
            h3=h2.Clone()
            h3.SetName(k2.GetName())
            file1.cd(nom_out)
            h3.Write()


        
print "\n\n\t ================================================================================================================"
print "\t ==================================  SUMMARY  ==================================================================="
if int(options.do_ggh_int)==0:
    print "\n\t\t using ggH signal model WITHOUT intreference !\n"
if int(options.do_ggh_int)==1:
    print "\n\t\t using ggH signal model WITH intreference !\n"

    print "\n\t total negative yield input bins SM VBF: %s, negative bins PS VBF: %s, negative bins int VBF: %s"%(negative_binsN_SM_VBF,negative_binsN_PS_VBF,negative_binsN_int_VBF)
if int(options.do_ggh_int)==0:
    print "\t total negative yield input bins SM ggH: %s, negative bins PS ggH: %s"%(negative_binsN_SM_ggH,negative_binsN_PS_ggH)
if int(options.do_ggh_int)==1:
    print "\t total negative yield input bins SM ggH: %s, negative bins PS ggH: %s, negative bins PS ggH: %s"%(negative_binsN_SM_ggH,negative_binsN_PS_ggH,negative_binsN_int_ggH)

fa3_with_neg_yields_VBF.sort()
fa3_with_neg_yields_ggH.sort()
print "\n\n\t tested fa3_VBF points:\t\t\t\t VBF = %s "%(fa3_VBF)
print "\t fa3_VBF points with NEGATIVE YIELD bins\t VBF = %s"%(fa3_with_neg_yields_VBF)
print "\n\t tested fa3_ggH points:\t\t\t\t ggH = %s "%(fa3_ggH)
print "\t fa3_ggH points with NEGATIVE YIELD bins\t ggH = %s"%(fa3_with_neg_yields_ggH)
print "\n\t ================================================================================================================\n"
        
