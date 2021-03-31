#!/usr/bin/env python
import ROOT
import re
import math
from array import array
from collections import OrderedDict
import argparse
import os
from ROOT import TMath

parser = argparse.ArgumentParser(
    "Create pre/post-fit plots for aHTT")
parser.add_argument(
    "--channel",
    action="store",
    dest="channel",
    default="tt",
    help="Which channel to run over? (et, mt, em, tt)")
parser.add_argument(
    "--year",
    action="store",
    dest="year",
    default="2016",
    help="Which year to run over? (2016,2017,2018)")
parser.add_argument(
    "--variable",
    action="store",
    dest="variable",
    default="L1",
    help="Provide the relative path to the target input file")
parser.add_argument(
    "--isEmbed",
    action="store",
    dest="isEmbed",
    default="0",
    help="Provide the relative path to the target input file")
parser.add_argument(
    "--doLog",
    action="store",
    dest="doLog",
    default="1",
    help="Provide the relative path to the target input file")
args = parser.parse_args()


def add_lumi(lumi_x):
    lowX=0.7
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.06)
    lumi.SetTextFont (   42 )
    #lumi.AddText("35.9 fb^{-1} (13 TeV)")
    lumi.AddText(str(lumi_x)+" fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.11
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.08)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi

def add_Preliminary():
    lowX=0.35
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Preliminary")
    return lumi

def make_legend(dx):
        #output = ROOT.TLegend(0.85+dx, 0.25, 0.99, 0.9, "", "brNDC")
        output = ROOT.TLegend(0.85+dx, 0.38, 0.98, 0.98, "", "brNDC")
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        output.SetFillColor(0)
        output.SetBorderSize(0)
        output.SetTextFont(62)
        return output

def make_legend_2(dx):
        #output = ROOT.TLegend(0.85+dx, 0.0, 0.99, 0.24, "", "brNDC")
        output = ROOT.TLegend(0.85+dx, 0.0, 0.99, 0.37, "", "brNDC")
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        output.SetFillColor(0)
        output.SetBorderSize(0)
        output.SetTextFont(62)
        return output

def make_legend_3(dx):
    output = ROOT.TLegend(0.85+dx, 0.0, 0.99, 0.37, "", "brNDC")
    output.SetLineWidth(0)
    output.SetLineStyle(0)
    output.SetFillColor(0)
    output.SetBorderSize(0)
    output.SetTextFont(62)
    output.SetTextSize(0.06)
    return output

ROOT.gStyle.SetFrameLineWidth(2)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

c=ROOT.TCanvas("canvas","",0,0,1200,600)
if args.channel=="em":
    c=ROOT.TCanvas("canvas","",0,0,2500,600)
c.cd()
if (args.doLog=="1"):
    c.SetLogy()

myfile=ROOT.TFile("output_shapes_fa3_%s_%s_%s.root"%(args.channel, args.year, args.variable),"read")
file2=ROOT.TFile("htt_input_%s_%s_%s.root"%(args.year, args.channel, args.variable),"read")
print " file: %s"%(myfile.GetName())
print " file2: %s"%(file2.GetName())



adapt=ROOT.gROOT.GetColor(12)
new_idx=ROOT.gROOT.GetListOfColors().GetSize() + 1
trans=ROOT.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(),adapt.GetBlue(), "",0.4)


categ=["htt_"+args.channel+"_3_"+args.year,
       "htt_"+args.channel+"_4_"+args.year,
       "htt_"+args.channel+"_5_"+args.year,
       "htt_"+args.channel+"_6_"+args.year]

if args.channel=="emetmt":
   categ=["htt_et_3","htt_et_4","htt_et_5","htt_et_6","htt_em_3","htt_em_4","htt_em_5","htt_em_6","htt_mt_3","htt_mt_4","htt_mt_5","htt_mt_6"]


exHisto=file2.Get(categ[0]).Get("reweighted_qqH_htt_0PM125")
#print "exHisto.GetNbinsX() \t",exHisto.GetNbinsX()
binnumPerTDir=exHisto.GetNbinsX()
# Total bin number / nbinsDBSM / nbinsNN
binnum,nbinsDBSM,nbinsNN=int(48), 4, 6
nbinsDBSM = len(categ)
binnum = int(nbinsDBSM*binnumPerTDir)
nbinsNN = 4 # this need to be mannual
if args.channel=="em" : nbinsNN = 6
if args.channel=="et" :
    if args.variable=="L1Zg" and args.year=="2016": nbinsNN = 3
    
nbinsD2j = binnumPerTDir/nbinsNN




hist_ZTT_em=ROOT.TH1F("hist_ZTT_em","hist_ZTT_em",binnum,0,binnum)
hist_ZL_em=ROOT.TH1F("hist_ZL_em","hist_ZL_em",binnum,0,binnum)
hist_TT_em=ROOT.TH1F("hist_TT_em","hist_TT_em",binnum,0,binnum)
hist_W_em=ROOT.TH1F("hist_W_em","hist_W_em",binnum,0,binnum)
hist_QCD_em=ROOT.TH1F("hist_QCD_em","hist_QCD_em",binnum,0,binnum)
hist_others_em=ROOT.TH1F("hist_others_em","hist_others_em",binnum,0,binnum)
hist_D_em=ROOT.TH1F("hist_D_em","hist_D_em",binnum,0,binnum)
hist_B_em=ROOT.TH1F("hist_B_em","hist_B_em",binnum,0,binnum)
hist_S_em=ROOT.TH1F("hist_S_em","hist_S_em",binnum,0,binnum)
hist_SM_em=ROOT.TH1F("hist_SM_em","hist_SM_em",binnum,0,binnum)
hist_SM_other_em=ROOT.TH1F("hist_SM_other_em","hist_SM_other_em",binnum,0,binnum)
hist_BSM_em=ROOT.TH1F("hist_BSM_em","hist_BSM_em",binnum,0,binnum)

data_yield=0.

for mycat in categ:
    print " cat: ",mycat
    #SM=file2.Get(mycat).Get("reweighted_qqH_htt_0PM125")
    print "getting reweighted_qqH_htt_0PM125 from %s %s"%(file2.GetName(),mycat)
    SM=file2.Get(mycat).Get("reweighted_qqH_htt_0PM125")
    SM_other=file2.Get(mycat).Get("GGH2Jets_sm_M125")
    if args.channel=="em":
        SM_other=file2.Get(mycat).Get("reweighted_ggH_htt_0PM125")
        print "taking reweighted_ggH_htt_0M125 %s"%(SM_other.Integral())

    if args.variable=="a3_ggH":
	    SM=file2.Get(mycat).Get("GGH2Jets_sm_M125")
	    #SM_other=file2.Get(mycat).Get("reweighted_qqH_htt_0PM125")
	    SM_other=file2.Get(mycat).Get("reweighted_qqH_htt_0PM125")
            if args.channel=="em":
	        SM=file2.Get(mycat).Get("reweighted_ggH_htt_0PM125")
	        SM_other=file2.Get(mycat).Get("reweighted_qqH_htt_0PM125")


    BSM=file2.Get(mycat).Get("reweighted_qqH_htt_0M125")

    if args.variable=="a3_ggH":
       BSM=file2.Get(mycat).Get("GGH2Jets_pseudoscalar_M125")

    if args.variable=="CP":
       BSM=file2.Get(mycat).Get("reweighted_qqH_htt_0Mf05ph0125")

    if args.channel=="em":
        # htt_em_3_2018 -> htt_em_3_13TeV_2018
        mycat=mycat.replace("_201","_13TeV_201")

    print "getting TotalBkg from %s %s_postfit"%(myfile.GetName(),mycat)
    B=myfile.Get(mycat+"_postfit").Get("TotalBkg")
    ZTT=myfile.Get(mycat+"_postfit").Get("ZTT")
    if args.isEmbed=="1":
        ZTT=myfile.Get(mycat+"_postfit").Get("embedded")
    ZL=myfile.Get(mycat+"_postfit").Get("ZL")
    if myfile.Get(mycat+"_postfit").Get("ZJ") and ZL:
       ZL.Add(myfile.Get(mycat+"_postfit").Get("ZJ"))
    if not ZL:
        if args.channel=="em":
            #ZL=myfile.Get(mycat+"_postfit").Get("ZLL")
            ZL=myfile.Get(mycat+"_postfit").Get("ZL")
        else:
            ZL=myfile.Get(mycat+"_postfit").Get("ZJ")
    TT=myfile.Get(mycat+"_postfit").Get("TT")
    if not TT and args.isEmbed=="0":
      print " => adding TTT and TTL, TTJ"
      TT=myfile.Get(mycat+"_postfit").Get("TTT")
      if myfile.Get(mycat+"_postfit").Get("TTL"):
        TT.Add(myfile.Get(mycat+"_postfit").Get("TTL"))
      if myfile.Get(mycat+"_postfit").Get("TTJ"):
        TT.Add(myfile.Get(mycat+"_postfit").Get("TTJ"))
    elif args.channel=="em":
      print " => adding TTL"
      TT=myfile.Get(mycat+"_postfit").Get("TTL")
    
    VV=myfile.Get(mycat+"_postfit").Get("VV")
    if not VV and args.isEmbed=="0":
      VV=myfile.Get(mycat+"_postfit").Get("VVT")
      if myfile.Get(mycat+"_postfit").Get("VVJ"):
        VV.Add(myfile.Get(mycat+"_postfit").Get("VVJ"))
    EWKZ=myfile.Get(mycat+"_postfit").Get("EWKZ")
    HWW=myfile.Get(mycat+"_postfit").Get("ggH_hww125")
    if args.isEmbed=="1" and args.channel=="tt":
      TT=myfile.Get(mycat+"_postfit").Get("TTL")
      print " getting VVL..."
      VV=myfile.Get(mycat+"_postfit").Get("VVL")
    if args.isEmbed=="1" and (args.channel=="mt" or args.channel=="et"):
      TT=myfile.Get(mycat+"_postfit").Get("TTT")
      print " getting VVL..."
      VV=myfile.Get(mycat+"_postfit").Get("VVT")

    if HWW:
       HWW.Add(myfile.Get(mycat+"_postfit").Get("qqH_hww125"))
    W=myfile.Get(mycat+"_postfit").Get("W")
    QCD=myfile.Get(mycat+"_postfit").Get("jetFakes")
    if args.channel=="em":
        QCD=myfile.Get(mycat+"_postfit").Get("QCD")
    S=myfile.Get(mycat+"_postfit").Get("TotalSig")
    D=myfile.Get(mycat+"_postfit").Get("data_obs")
    factor=0
    if "_3_" in mycat:
      factor=1
    elif "_4_" in mycat:
       factor=2
    elif "_5_" in mycat:
       factor=3
    elif "_6_" in mycat:
       factor=4

    for j in range(1,B.GetSize()-1):
       d2jrotation = (int(j)%nbinsD2j) if (int(j)%nbinsD2j)>0 else nbinsD2j
       #dnnrotation = ((j%nbinsNN)-1) if ((j%nbinsNN)-1)>=0 else nbinsNN-1
       dnnrotation = (int((j-1)/nbinsD2j))
       bin = (d2jrotation-1)*nbinsNN*nbinsDBSM + factor + nbinsDBSM*dnnrotation
       myweight=1.0
       print "j : ", j , "   bin :  ", bin
       print D.GetBinContent(j)
       hist_ZTT_em.SetBinContent(bin,hist_ZTT_em.GetBinContent(bin)+ZTT.GetBinContent(j)*myweight)

       if args.isEmbed=="0":
           hist_ZTT_em.SetBinContent(bin,hist_ZTT_em.GetBinContent(bin)+EWKZ.GetBinContent(j)*myweight)

       if TT:
           hist_TT_em.SetBinContent(bin,hist_TT_em.GetBinContent(bin)+TT.GetBinContent(j)*myweight)
       
       if QCD:
          hist_QCD_em.SetBinContent(bin,hist_QCD_em.GetBinContent(bin)+QCD.GetBinContent(j)*myweight)
       
       if ZL:
          hist_ZL_em.SetBinContent(bin,hist_ZL_em.GetBinContent(bin)+ZL.GetBinContent(j)*myweight)
       if VV:
           hist_others_em.SetBinContent(bin,hist_others_em.GetBinContent(bin)+VV.GetBinContent(j)*myweight)
       if EWKZ:
           hist_others_em.SetBinContent(bin,hist_others_em.GetBinContent(bin)+EWKZ.GetBinContent(j)*myweight)

       if HWW:
          hist_others_em.SetBinContent(bin,hist_others_em.GetBinContent(bin)+HWW.GetBinContent(j)*myweight)
       if W:
          hist_W_em.SetBinContent(bin,hist_W_em.GetBinContent(bin)+W.GetBinContent(j)*myweight)

       hist_D_em.SetBinContent(bin,hist_D_em.GetBinContent(bin)+D.GetBinContent(j)*myweight)
       if hist_D_em.GetBinContent(bin)>0:	
       		hist_D_em.SetBinError(bin,((hist_D_em.GetBinContent(bin)*myweight)**0.5))


       hist_B_em.SetBinError(bin,(hist_B_em.GetBinError(bin)*hist_B_em.GetBinError(bin)+B.GetBinError(j)*B.GetBinError(j)*myweight*myweight)**0.5)
       #hist_B_em.SetBinError(bin,hist_B_em.GetBinError(bin)+B.GetBinError(j)*myweight)
       hist_B_em.SetBinContent(bin,hist_B_em.GetBinContent(bin)+B.GetBinContent(j)*myweight)

       hist_B_em.SetBinError(bin,(hist_B_em.GetBinError(bin)*hist_B_em.GetBinError(bin)+S.GetBinError(j)*S.GetBinError(j)*myweight*myweight)**0.5)
       #hist_B_em.SetBinError(bin,hist_B_em.GetBinError(bin)+S.GetBinError(j)*myweight)
       hist_B_em.SetBinContent(bin,hist_B_em.GetBinContent(bin)+S.GetBinContent(j)*myweight)

       hist_S_em.SetBinContent(bin,hist_S_em.GetBinContent(bin)+S.GetBinContent(j)*myweight)

       hist_SM_em.SetBinContent(bin,hist_SM_em.GetBinContent(bin)+SM.GetBinContent(j)*myweight)
       #print "hist_SM_other_em.GetBinContent(bin)=",hist_SM_other_em.GetBinContent(bin)
       #print "SM_other.GetBinContent(j)=",SM_other.GetBinContent(j)
       hist_SM_other_em.SetBinContent(bin,hist_SM_other_em.GetBinContent(bin)+SM_other.GetBinContent(j)*myweight)
       hist_BSM_em.SetBinContent(bin,hist_BSM_em.GetBinContent(bin)+BSM.GetBinContent(j)*myweight)

       # do data blinding:
       data_yield=hist_D_em.Integral()
       if hist_B_em.GetBinContent(bin) > 0 and (hist_SM_em.GetBinContent(bin)+hist_BSM_em.GetBinContent(bin))/ TMath.Sqrt(hist_B_em.GetBinContent(bin) + 0.09*0.09*hist_B_em.GetBinContent(bin)*hist_B_em.GetBinContent(bin)) >= 0.3:
           hist_D_em.SetBinContent(bin, -100)


err_B=ROOT.Double(0)
err_S=ROOT.Double(0)

c.cd()

pad1 = ROOT.TPad("pad1","pad1",0,0.35,1,1)
pad1.Draw()
pad1.cd()
pad1.SetFillColor(0)
pad1.SetBorderMode(0)
pad1.SetBorderSize(10)
pad1.SetTickx(1)
pad1.SetTicky(1)
#pad1.SetLeftMargin(0.18)
pad1.SetRightMargin(0.15)
pad1.SetTopMargin(0.122)
pad1.SetBottomMargin(0.026)
pad1.SetFrameFillStyle(0)
pad1.SetFrameLineStyle(0)
pad1.SetFrameLineWidth(3)
pad1.SetFrameBorderMode(0)
pad1.SetFrameBorderSize(10)
if (args.doLog=="1"):
    pad1.SetLogy()

hist_D_em.GetXaxis().SetLabelSize(0)
hist_D_em.GetXaxis().SetTitle("")
hist_D_em.GetXaxis().SetTitleSize(0.06)
hist_D_em.GetXaxis().SetNdivisions(505)
hist_D_em.GetYaxis().SetLabelFont(42)
hist_D_em.GetYaxis().SetLabelOffset(0.01)
hist_D_em.GetYaxis().SetLabelSize(0.06)
hist_D_em.GetYaxis().SetTitleSize(0.085)
hist_D_em.GetYaxis().SetTitleOffset(0.6)
hist_D_em.GetYaxis().SetTitle("Events/bin")
hist_D_em.GetYaxis().SetTickLength(0.012)

hist_ZTT_em.SetFillColor(ROOT.TColor.GetColor("#ffcc66"))
hist_ZTT_em.SetLineColor(ROOT.TColor.GetColor("#ffcc66"))
hist_ZL_em.SetFillColor(ROOT.TColor.GetColor("#4496c8"))
hist_ZL_em.SetLineColor(ROOT.TColor.GetColor("#4496c8"))
hist_TT_em.SetFillColor(ROOT.TColor.GetColor("#9999cc"))
hist_TT_em.SetLineColor(ROOT.TColor.GetColor("#9999cc"))
hist_QCD_em.SetFillColor(ROOT.TColor.GetColor("#ffccff"))
hist_QCD_em.SetLineColor(ROOT.TColor.GetColor("#ffccff"))
hist_W_em.SetFillColor(ROOT.TColor.GetColor("#a53db8"))
hist_W_em.SetLineColor(ROOT.TColor.GetColor("#a53db8"))
hist_others_em.SetFillColor(ROOT.TColor.GetColor("#12cadd"))
hist_others_em.SetLineColor(ROOT.TColor.GetColor("#12cadd"))
hist_S_em.SetLineColor(0)
hist_S_em.SetLineWidth(2)
hist_S_em.SetFillColor(2)

hist_SM_em.SetLineColor(ROOT.EColor(ROOT.kRed))
hist_SM_em.SetLineWidth(3)
#hist_SM_other_em.SetLineColor(28)
hist_SM_other_em.SetLineColor(ROOT.EColor(ROOT.kMagenta+1))
hist_SM_other_em.SetLineWidth(2)
hist_SM_other_em.SetLineStyle(2)
hist_BSM_em.SetLineColor(ROOT.EColor(ROOT.kBlack))
hist_BSM_em.SetLineWidth(3)

if args.channel=="em":
  hist_SM_em.SetLineWidth(2)
  hist_SM_other_em.SetLineWidth(1)
  hist_BSM_em.SetLineWidth(2)
  ROOT.gStyle.SetLineWidth(1)
  ROOT.gStyle.SetFrameLineWidth(1)
  pad1.SetBorderSize(5)
  pad1.SetFrameBorderSize(5)



hist_SM_em.Scale(10)
hist_SM_other_em.Scale(10)
hist_BSM_em.Scale(10)

hist_D_em.SetLineColor(1)
errorBand=hist_B_em.Clone()
errorBand.SetMarkerSize(0)
errorBand.SetFillColor(new_idx)
errorBand.SetLineColor(1)
errorBand.SetLineWidth(1)
#histS.SetLineColor(2)
#histS.SetLineWidth(2)
mystack=ROOT.THStack("mystack","mystack")
mystack.Add(hist_others_em)
mystack.Add(hist_W_em)
mystack.Add(hist_QCD_em)
mystack.Add(hist_TT_em)
mystack.Add(hist_ZL_em)
mystack.Add(hist_ZTT_em)
mystack.Add(hist_S_em)
yield_stack=0
for hist in mystack.GetHists():
    yield_stack=yield_stack+hist.Integral()
    print " histo %s yield: %s -> sum %s "%(hist.GetName(),hist.Integral(),yield_stack)

# as if hist_B_em does not include the signal!
#print "\nYIELD CHECK: yield all mystack: %s, total S(%s)+B(%s): %s, ==> ratio %s "%(yield_stack,hist_S_em.Integral(),hist_B_em.Integral(), hist_S_em.Integral()+hist_B_em.Integral(),yield_stack/(hist_S_em.Integral()+hist_B_em.Integral()))
#print  " YIELD CHECK: yield data: %s ==> ratio to mystack %s, to S+B %s "%(data_yield, data_yield/yield_stack,data_yield/(hist_S_em.Integral()+hist_B_em.Integral()))

# as if hist_B_em does include the signal!
print "\nYIELD CHECK: yield all mystack: %s, total S(%s)+B(%s): %s, ==> ratio %s "%(yield_stack,hist_S_em.Integral(),hist_B_em.Integral()-hist_S_em.Integral(), hist_B_em.Integral(),yield_stack/(hist_B_em.Integral()))
print  " YIELD CHECK: yield data: %s ==> ratio to mystack %s, to S+B %s "%(data_yield, data_yield/yield_stack,data_yield/(hist_B_em.Integral()))


hist_D_em.SetMarkerStyle(20)
hist_D_em.Draw("e0pX0")
hist_D_em.SetTitle("")
hist_D_em.SetMinimum(0.1)

for ii in range(1,hist_D_em.GetNbinsX()):
    print ii, "\t", hist_D_em.GetBinContent(ii)

if (args.doLog=="1"):
    hist_D_em.SetMaximum(80000*hist_B_em.GetMaximum())
if (args.doLog=="1" and args.channel=="em"):
    hist_D_em.SetMaximum(100000*hist_B_em.GetMaximum())
#hist_D_em.SetMaximum(max(1.2*hist_B_em.GetMaximum(),2.15*hist_D_em.GetMaximum()))
mystack.Draw("histsame")
errorBand.Draw("e2same")
hist_SM_em.Draw("histsame")
hist_SM_other_em.Draw("histsame")
hist_BSM_em.Draw("histsame")
hist_D_em.Draw("e0pX0same")
legend=make_legend(0.0)
legend.AddEntry(hist_D_em,"Observed","elp")
legend.AddEntry(hist_S_em,"H#rightarrow#tau#tau","f")
legend.AddEntry(hist_ZTT_em,"Z#rightarrow#tau#tau","f")
legend.AddEntry(hist_ZL_em,"Z#rightarrow#mu#mu/ee","f")
legend.AddEntry(hist_TT_em,"t#bar{t}+jets","f")
legend.AddEntry(hist_QCD_em,"QCD multijet","f")
legend.AddEntry(hist_W_em,"W+jets","f")
legend.AddEntry(hist_others_em,"Others","f")
legend.AddEntry(errorBand,"Total unc.","f")
legend.Draw()

legend2=make_legend_2(0.0) if  args.channel!="em" else make_legend_3(0.0)
if args.variable=="a3_ggH":
	legend2.AddEntry(hist_SM_em,"#splitline{SM ggH H#rightarrow#tau#tau}{(#sigma = 10 #sigma_{SM})}","l")
	legend2.AddEntry(hist_BSM_em,"#splitline{BSM ggH H#rightarrow#tau#tau}{(#sigma = 10 #sigma_{SM})}","l")
	legend2.AddEntry(hist_SM_other_em,"#splitline{SM VBF H#rightarrow#tau#tau}{(#sigma = 10 #sigma_{SM})}","l")
else:
        legend2.AddEntry(hist_SM_em,"#splitline{SM VBF H#rightarrow#tau#tau}{(#sigma = 10 #sigma_{SM})}","l")
        legend2.AddEntry(hist_BSM_em,"#splitline{BSM VBF H#rightarrow#tau#tau}{(#sigma = 10 #sigma_{SM})}","l")
	legend2.AddEntry(hist_SM_other_em,"#splitline{SM ggH H#rightarrow#tau#tau}{(#sigma = 10 #sigma_{SM})}","l")
legend2.Draw()

lumi_x=35.9
if args.year=="2017":
    lumi_x=41.5
elif args.year=="2018":
    lumi_x=59.5

l1=add_lumi(lumi_x)
l1.Draw("same")
l2=add_CMS()
l2.Draw("same")
#l3=add_Preliminary()
#l3.Draw("same")

myvariable="D_{#Lambda1}"
if args.variable=="a3":
   myvariable="D_{0-}"
if args.variable=="a3_ggH":
   myvariable="D_{0-}^{ggH}"
if args.variable=="a2":
   myvariable="D_{0h+}"
if args.variable=="L1":
   myvariable="D_{#Lambda1}"
if args.variable=="L1Zg":
   myvariable="D_{#Lambda1}^{Z#gamma}"

line2=[]
label2=[]


## Labels on top - D2j
if 1>0:
    if args.channel=="mt":
        if args.variable=="a3_ggH":
            D2jbins = ["0.00", "0.25", "0.50", "0.75", "1.00"]
        else:
            D2jbins = ["0.00","0.75","1.00"]
    elif args.channel=="et":    
        if args.variable=="L1Zg" and args.year!="2017":            
            D2jbins = ["0.00","0.625","1.00"]
        elif args.variable=="a3_ggH":
            D2jbins =  ["0.00", "0.25", "0.50", "0.75", "1.00"] 
        else:
            D2jbins = ["0.00","0.75","1.00"]            
    elif args.channel=="em":
         D2jbins = ["0.00","0.25","0.50","0.75","1.00"]
    ny = nbinsDBSM*nbinsNN
    nx = binnum/ny
    myvariable2 = "D_{2jets}^{VBF}"
    for z in range(1, nx+1):
        line2.append(ROOT.TLine(z*ny,0,z*ny,hist_D_em.GetMaximum()))
        line2[z-1].SetLineStyle(3)
        line2[z-1].Draw("same")
        posx=0.23+0.74*(z-1)/nx if args.channel!="em" else 0.16+0.74*(z-1)/nx
        if args.variable=="a3_ggH": posx=0.13+0.74*(z-1)/nx
        label2.append(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
        iFirst = (z-1)%(len(D2jbins)-1)
        iSecond = iFirst+1
        label2[z-1].AddText(myvariable2+" #in [%s,%s]"%(D2jbins[iFirst],D2jbins[iSecond]))
        label2[z-1].SetBorderSize(   0 )
        label2[z-1].SetFillStyle(    0 )
        label2[z-1].SetTextAlign(   12 )
        label2[z-1].SetTextSize ( 0.05 )
        label2[z-1].SetTextColor(    1 )
        label2[z-1].SetTextFont (   42 )
        label2[z-1].Draw("same")

## Labels in the middle - NN
line=[]
label=[]
text=[]
if 1>0:
    if args.channel=="mt":
        if args.variable=="a3":
            NNbins = ["0.0","0.1","0.2","0.8","1.0"]
        if args.variable=="a2":
            if args.year=="2018":
                NNbins = ["0.0","0.1","0.2","0.8","1.0"]
            elif args.year=="2017":
                NNbins = ["0.0","0.1","0.2","0.8","1.0"]
            elif args.year=="2016":
                NNbins = ["0.0","0.1","0.2","0.8","1.0"]

        if args.variable=="L1":
            if args.year=="2018":
                NNbins = ["0.0","0.1","0.2","0.8","1.0"]
            elif args.year=="2017":
                NNbins = ["0.0","0.1","0.2","0.8","1.0"]
            elif args.year=="2016":
                NNbins = ["0.0","0.1","0.2","0.7","1.0"]

        if args.variable=="L1Zg":
            if args.year=="2018":
                NNbins = ["0.0","0.1","0.3","0.7","1.0"]
            elif args.year=="2017":
                NNbins = ["0.0","0.1","0.3","0.7","1.0"]
            elif args.year=="2016":
                NNbins = ["0.0","0.1","0.5","0.7","1.0"]

        if args.variable=="a3_ggH":
            NNbins = ["0.00", "0.15", "0.40", "0.80", "1.00"]

    elif args.channel=="et":
        if args.variable=="a3" or args.variable=="a2":
            if args.year=="2018":
                NNbins = ["0.0","0.1","0.2","0.7","1.0"]
            elif args.year=="2017":
                NNbins = ["0.0","0.1","0.2","0.7","1.0"]
            elif args.year=="2016":
                NNbins = ["0.0","0.1","0.2","0.7","1.0"]

        if args.variable=="L1":
            if args.year=="2018":
                NNbins = ["0.0","0.1","0.3","0.6","1.0"] 
            elif args.year=="2017":
                NNbins = ["0.0","0.1","0.3","0.6","1.0"] 
            elif args.year=="2016":
                NNbins = ["0.0","0.1","0.3","0.6","1.0"] 

        if args.variable=="L1Zg":
            if args.year=="2018":
                NNbins = ["0.0","0.1","0.2","0.6","1.0"]
            elif args.year=="2017":
                NNbins = ["0.0","0.1","0.2","0.6","1.0"]
            elif args.year=="2016":
                NNbins = ["0.0","0.1","0.6","1.0"]

        if args.variable=="a3_ggH":
            NNbins = ["0.00", "0.15", "0.40", "0.80", "1.00"]

    elif args.channel=="em":
        NNbins = ["0.00","0.30","0.50","0.65","0.80","0.90","1.0"]


    ny= nbinsDBSM
    nx=binnum/ny
    for z in range(1, nx+1):
        line.append(ROOT.TLine(z*ny,0,z*ny,0.085*hist_D_em.GetMaximum()))
        line[z-1].SetLineStyle(5)
        line[z-1].SetLineColor(4)
        line[z-1].Draw("same")
        posx=0.109+0.75*(z-1)/nx
        label.append(ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC"))
        iFirst = (z-1)%(len(NNbins)-1)
        iSecond = iFirst+1
        text.append(label[z-1].AddText("NN_{disc} #in [%s,%s]"%(NNbins[iFirst],NNbins[iSecond])))


        label[z-1].SetBorderSize(   0 )
        label[z-1].SetFillStyle(    0 )
        label[z-1].SetTextAlign(   12 )
        label[z-1].SetTextSize ( 0.05 )
        label[z-1].SetTextColor(    4 )
        label[z-1].SetTextFont (   42 )
        text[z-1].SetTextAngle(90)
        label[z-1].Draw("same")





pad1.RedrawAxis()

categ  = ROOT.TPaveText(0.33, 0.895, 0.63, 0.99, "NDC")
categ.SetBorderSize(   0 )
categ.SetFillStyle(    0 )
categ.SetTextAlign(   12 )
categ.SetTextSize ( 0.08 )
categ.SetTextColor(    1 )
categ.SetTextFont (   42 )
if args.channel=="em":
    categ.AddText("VBF, e#mu")
if args.channel=="et":
    categ.AddText("VBF, e#tau_{h}")
if args.channel=="mt":
    categ.AddText("VBF, #mu#tau_{h}")
if args.channel=="tt":
    categ.AddText("VBF, #tau_{h}#tau_{h}")
if args.channel=="all":
    categ.AddText("All #tau#tau")
if args.channel=="emetmt":
    categ.AddText("VBF, e#mu + e#tau_{h} + #mu#tau_{h}")
categ.Draw("same")

c.cd()
pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.35);
pad2.SetTopMargin(0.05);
pad2.SetBottomMargin(0.35);
#pad2.SetLeftMargin(0.18);
pad2.SetRightMargin(0.15);
pad2.SetTickx(1)
pad2.SetTicky(1)
pad2.SetFrameLineWidth(3)
#pad2.SetGridx()
pad2.SetGridy()
pad2.Draw()
pad2.cd()
h1=hist_D_em.Clone()
h1.SetMaximum(1.8)
h1.SetMinimum(0.2)
h1.SetMarkerStyle(20)
h3=errorBand.Clone()
hwoE=errorBand.Clone()
for iii in range (1,hwoE.GetSize()-2):
  hwoE.SetBinError(iii,0)
h3.Sumw2()
h1.Sumw2()
h1.SetStats(0)
h1.Divide(hwoE)
h3.Divide(hwoE)
h1.GetXaxis().SetTitle("m_{#tau#tau} (GeV)")
h1.GetXaxis().SetTitle("")
h1.GetYaxis().SetLabelSize(0.08)
h1.GetYaxis().SetTitle("Obs./Exp.")
h1.GetXaxis().SetNdivisions(505)
h1.GetYaxis().SetNdivisions(5)

h1.GetXaxis().SetTitleSize(0.15)
h1.GetYaxis().SetTitleSize(0.15)
h1.GetYaxis().SetTitleOffset(0.3)
h1.GetXaxis().SetTitleOffset(1.04)
h1.GetXaxis().SetLabelSize(0.11)
h1.GetYaxis().SetLabelSize(0.11)
h1.GetXaxis().SetTitleFont(42)
h1.GetYaxis().SetTitleFont(42)

h1.LabelsOption("v","X")
h1.GetXaxis().SetLabelOffset(0.02)
h1.GetXaxis().SetLabelSize(0.06)

if 1>0:
    if args.channel=="mt" or args.channel=="et":
        dBSMbinning = ["0.0","0.3","0.5","0.7","1.0"]
    if args.channel=="em":
        dBSMbinning = ["0.0","0.2","0.5","0.8","1.0"]
    for idx in range(1,binnum+1):
        iFirst = (idx-1)%(len(dBSMbinning)-1)
        iSecond = iFirst+1
        dBSMbinText = "%s-%s"%(dBSMbinning[iFirst], dBSMbinning[iSecond])
        h1.GetXaxis().SetBinLabel(idx,dBSMbinText)
h1.GetXaxis().SetLabelSize(0.07)
h1.GetYaxis().SetLabelSize(0.08)
h1.GetYaxis().SetTickLength(0.012)
h1.GetYaxis().SetNdivisions(5)

h1.GetXaxis().SetLabelSize(0.13)
if args.channel=="tt":
   #h1.GetXaxis().SetLabelSize(0.08)
   h1.GetXaxis().SetLabelSize(0.13)
h1.GetYaxis().SetLabelSize(0.11)
h1.GetXaxis().SetTitleFont(42)
h1.GetYaxis().SetTitleFont(42)
h1.LabelsOption("v","X")

h1.Draw("e0pX0")
h3.Draw("e2same")

categ2  = ROOT.TPaveText(0.86, 0.1, 0.95, 0.4, "NDC")
categ2.SetBorderSize(   0 )
categ2.SetFillStyle(    0 )
categ2.SetTextAlign(   12 )
categ2.SetTextSize ( 0.16 )
categ2.SetTextColor(    1 )
categ2.SetTextFont (   62 )
categ2.AddText(myvariable)
categ2.Draw("same")

c.cd()
pad1.Draw()

ROOT.gPad.RedrawAxis()

c.Modified()
c.SaveAs("plots/unrolled_"+args.variable+"_"+args.channel+"_"+args.year+".pdf")
c.SaveAs("plots/unrolled_"+args.variable+"_"+args.channel+"_"+args.year+".png")



