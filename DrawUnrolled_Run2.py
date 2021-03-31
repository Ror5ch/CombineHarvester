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

ROOT.gStyle.SetFrameLineWidth(2)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

c=ROOT.TCanvas("canvas","",0,0,1200,600)
c.cd()
if (args.doLog=="1"):
    c.SetLogy()

myfile=ROOT.TFile("output_shapes_fL1Zg.root","read")
file2=ROOT.TFile("htt_input_fL1Zg.root","read")
if args.variable=="L1":
   myfile=ROOT.TFile("output_shapes_fL1.root","read")
   file2=ROOT.TFile("htt_input_fL1.root","read")
if args.variable=="a2":
   myfile=ROOT.TFile("output_shapes_fa2.root","read")
   file2=ROOT.TFile("htt_input_fa2.root","read")
#if args.variable=="a3" or args.variable=="0jet" or args.variable=="boosted_mtt" or args.variable=="boosted_pth":
#   myfile=ROOT.TFile("output_shapes_fa3.root","read")
#   file2=ROOT.TFile("htt_input_fa3.root","read")
if args.variable=="a3" or args.variable=="0jet" or args.variable=="boosted_mtt" or args.variable=="boosted_pth":
   myfile=ROOT.TFile("output_shapes_fa3_tt_"+args.year+".root","read")
   file2=ROOT.TFile("htt_input_"+args.year+"_tt.root","read")

if args.variable=="a3_ggH" and args.channel=="tt":
   myfile=ROOT.TFile("output_shapes_fa3_ggH_tt_"+args.year+".root","read")
   file2=ROOT.TFile("htt_input_"+args.year+"_ggH_tt.root","read")
if args.variable=="a3_ggH" and args.channel=="mt":
   myfile=ROOT.TFile("output_shapes_fa3_ggH_mt_"+args.year+".root","read")
   file2=ROOT.TFile("htt_input_"+args.year+"_ggH_mt.root","read")
if args.variable=="a3_ggH" and args.channel=="et":
   myfile=ROOT.TFile("output_shapes_fa3_ggH_et_"+args.year+".root","read")
   file2=ROOT.TFile("htt_input_"+args.year+"_ggH_et.root","read")
if args.variable=="a3_ggH" and args.channel=="em":
   myfile=ROOT.TFile("output_shapes_fa3_ggH_em_"+args.year+".root","read")
   file2=ROOT.TFile("htt_input_"+args.year+"_ggH_em.root","read")

if args.variable=="a3" and args.channel=="em":
   myfile=ROOT.TFile("output_shapes_fa3_em_"+args.year+".root","read")
   file2=ROOT.TFile("htt_input_"+args.year+"_em.root","read")
if args.variable=="a3" and args.channel=="mt":
   myfile=ROOT.TFile("output_shapes_fa3_mt_"+args.year+".root","read")
   file2=ROOT.TFile("htt_input_"+args.year+"_mt.root","read")
if args.variable=="a3" and args.channel=="et":
   myfile=ROOT.TFile("output_shapes_fa3_et_"+args.year+".root","read")
   file2=ROOT.TFile("htt_input_"+args.year+"_et.root","read")

if args.variable=="CP":
   myfile=ROOT.TFile("output_shapes_fa3.root","read")
   file2=ROOT.TFile("htt_input_fa3.root","read")

adapt=ROOT.gROOT.GetColor(12)
new_idx=ROOT.gROOT.GetListOfColors().GetSize() + 1
trans=ROOT.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(),adapt.GetBlue(), "",0.4)

categ=["htt_em_3_13TeV","htt_em_4_13TeV","htt_em_5_13TeV","htt_em_6_13TeV"]
if args.channel=="et":
   categ=["htt_et_3_13TeV","htt_et_4_13TeV","htt_et_5_13TeV","htt_et_6_13TeV"]
if args.channel=="et":
   categ=["htt_et_3_13TeV_"+args.year,"htt_et_4_13TeV_"+args.year,"htt_et_5_13TeV_"+args.year,"htt_et_6_13TeV_"+args.year]

if args.channel=="em":
   categ=["htt_em_3_13TeV_"+args.year,"htt_em_4_13TeV_"+args.year,"htt_em_5_13TeV_"+args.year,"htt_em_6_13TeV_"+args.year]
if args.channel=="mt":
   categ=["htt_mt_3_13TeV_"+args.year,"htt_mt_4_13TeV_"+args.year,"htt_mt_5_13TeV_"+args.year,"htt_mt_6_13TeV_"+args.year]
if args.channel=="tt":
   categ=["htt_tt_3_13TeV_"+args.year,"htt_tt_4_13TeV_"+args.year,"htt_tt_5_13TeV_"+args.year,"htt_tt_6_13TeV_"+args.year]
if args.channel=="emetmt":
   categ=["htt_et_3_13TeV","htt_et_4_13TeV","htt_et_5_13TeV","htt_et_6_13TeV","htt_em_3_13TeV","htt_em_4_13TeV","htt_em_5_13TeV","htt_em_6_13TeV","htt_mt_3_13TeV","htt_mt_4_13TeV","htt_mt_5_13TeV","htt_mt_6_13TeV"]

   '''
if args.variable=="a3" or args.variable=="CP":
   if args.channel=="em":
      categ=["htt_em_3_13TeV","htt_em_4_13TeV","htt_em_5_13TeV","htt_em_6_13TeV","htt_em_7_13TeV","htt_em_8_13TeV","htt_em_9_13TeV","htt_em_10_13TeV"]
   if args.channel=="et":
      categ=["htt_et_3_13TeV","htt_et_4_13TeV","htt_et_5_13TeV","htt_et_6_13TeV","htt_et_7_13TeV","htt_et_8_13TeV","htt_et_9_13TeV","htt_et_10_13TeV"]
   if args.channel=="mt":
      categ=["htt_mt_3_13TeV","htt_mt_4_13TeV","htt_mt_5_13TeV","htt_mt_6_13TeV","htt_mt_7_13TeV","htt_mt_8_13TeV","htt_mt_9_13TeV","htt_mt_10_13TeV"]
   if args.channel=="tt":
      categ=["htt_tt_3_13TeV","htt_tt_4_13TeV","htt_tt_5_13TeV","htt_tt_6_13TeV","htt_tt_7_13TeV","htt_tt_8_13TeV","htt_tt_9_13TeV","htt_tt_10_13TeV"]
   if args.channel=="emetmt":
      categ=["htt_em_3_13TeV","htt_em_4_13TeV","htt_em_5_13TeV","htt_em_6_13TeV","htt_em_7_13TeV","htt_em_8_13TeV","htt_em_9_13TeV","htt_em_10_13TeV","htt_et_3_13TeV","htt_et_4_13TeV","htt_et_5_13TeV","htt_et_6_13TeV","htt_et_7_13TeV","htt_et_8_13TeV","htt_et_9_13TeV","htt_et_10_13TeV","htt_mt_3_13TeV","htt_mt_4_13TeV","htt_mt_5_13TeV","htt_mt_6_13TeV","htt_mt_7_13TeV","htt_mt_8_13TeV","htt_mt_9_13TeV","htt_mt_10_13TeV"]
'''

# HERE
binnum=int(48)
if args.channel=="mt" or (args.year=="2016" and args.channel=="et"):
   binnum=int(32)
if (args.channel=="et" and args.year!="2016") or args.channel=="tt":
   binnum=int(24)
if args.channel=="em":
   binnum=int(64)

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
    SM=file2.Get(mycat).Get("reweighted_qqH_htt_0PM125")
    SM_other=file2.Get(mycat).Get("GGH2Jets_sm_M125")
    if args.variable=="a3_ggH":
	    SM=file2.Get(mycat).Get("GGH2Jets_sm_M125")
	    SM_other=file2.Get(mycat).Get("reweighted_qqH_htt_0PM125")


    BSM=file2.Get(mycat).Get("reweighted_qqH_htt_0M125")

    if args.variable=="a3_ggH":
       BSM=file2.Get(mycat).Get("GGH2Jets_pseudoscalar_M125")

    if args.variable=="CP":
       BSM=file2.Get(mycat).Get("reweighted_qqH_htt_0Mf05ph0125")


    B=myfile.Get(mycat+"_postfit").Get("TotalBkg")
    ZTT=myfile.Get(mycat+"_postfit").Get("ZTT")
    if args.isEmbed=="1":
        ZTT=myfile.Get(mycat+"_postfit").Get("embedded")
    ZL=myfile.Get(mycat+"_postfit").Get("ZL")
    if myfile.Get(mycat+"_postfit").Get("ZJ") and ZL:
       ZL.Add(myfile.Get(mycat+"_postfit").Get("ZJ"))
    if not ZL:
        if args.channel=="em":
            ZL=myfile.Get(mycat+"_postfit").Get("ZLL")
        else:
            ZL=myfile.Get(mycat+"_postfit").Get("ZJ")
    TT=myfile.Get(mycat+"_postfit").Get("TT")
    if not TT and args.isEmbed=="0":
      TT=myfile.Get(mycat+"_postfit").Get("TTT")
      if myfile.Get(mycat+"_postfit").Get("TTL"):
        TT.Add(myfile.Get(mycat+"_postfit").Get("TTL"))
      if myfile.Get(mycat+"_postfit").Get("TTJ"):
        TT.Add(myfile.Get(mycat+"_postfit").Get("TTJ"))
      
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
    elif "_7_" in mycat:
      factor=1
    elif "_8_" in mycat:
       factor=2
    elif "_9_" in mycat:
       factor=3
    elif "_10_" in mycat:
       factor=4

    for j in range(1,B.GetSize()-1):

       #HERE
       bin = int(j) + 12*(factor-1)
       if args.channel=="et" or args.channel=="tt":
           #bin = int(j) + 28*(factor-1)
           bin = int(j) + 6*(factor-1)
       if args.channel=="em":
           #bin = int(j) + 28*(factor-1)
           bin = int(j) + 16*(factor-1)
       if args.channel=="mt"  or (args.channel=="et" and args.year=="2016"):
           #bin = int(j) + 28*(factor-1)
           bin = int(j) + 8*(factor-1)

       myweight=1.0


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
       hist_SM_other_em.SetBinContent(bin,hist_SM_other_em.GetBinContent(bin)+SM_other.GetBinContent(j)*myweight)
       hist_BSM_em.SetBinContent(bin,hist_BSM_em.GetBinContent(bin)+BSM.GetBinContent(j)*myweight)

       # do data blinding:
       data_yield=hist_D_em.Integral()
       if hist_B_em.GetBinContent(bin) > 0 and (hist_SM_em.GetBinContent(bin)+hist_BSM_em.GetBinContent(bin))/ TMath.Sqrt(hist_B_em.GetBinContent(bin) + 0.09*0.09*hist_B_em.GetBinContent(bin)*hist_B_em.GetBinContent(bin)) >= 0.3:
           hist_D_em.SetBinContent(bin, -10)


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
hist_D_em.SetMinimum(0.9)
if args.channel=="et":
	hist_D_em.SetMinimum(0.5)
if args.channel=="em":
	hist_D_em.SetMinimum(0.05)

if (args.doLog=="1"):
    hist_D_em.SetMaximum(800*hist_B_em.GetMaximum())
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

legend2=make_legend_2(0.0)
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
if args.variable=="L1Zg":
   myvariable="D_{#Lambda1}^{Z#gamma}"

line2=[]
label2=[]
if args.channel=="mt":
   nx=4
   ny=8
   for z in range(1, nx+1):
       line2.append(ROOT.TLine(z*ny,0,z*ny,hist_D_em.GetMaximum()))
       line2[z-1].SetLineStyle(3)
       line2[z-1].Draw("same")
       posx=0.15+0.74*(z-1)/nx
       label2.append(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
       if args.variable!="a3_ggH":
       		label2[z-1].AddText(myvariable+" #in [0,0.2]")
       else:
                label2[z-1].AddText(myvariable+" #in [0,0.35]")
       if z==2:
   	   label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
       	   if args.variable!="a3_ggH":
           	label2[z-1].AddText(myvariable+" #in [0.2,0.4]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.35,0.5]")

       elif z==3:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           #label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.5,0.65]")

       elif z==4:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           #label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.65,1.0]")

       label2[z-1].SetBorderSize(   0 )
       label2[z-1].SetFillStyle(    0 )
       label2[z-1].SetTextAlign(   12 )
       label2[z-1].SetTextSize ( 0.05 )
       label2[z-1].SetTextColor(    1 )
       label2[z-1].SetTextFont (   42 )
       label2[z-1].Draw("same")
elif args.channel=="et" and args.year!="2016":
   nx=4
   ny=6
   for z in range(1, nx+1):
       line2.append(ROOT.TLine(z*ny,0,z*ny,hist_D_em.GetMaximum()))
       line2[z-1].SetLineStyle(3)
       line2[z-1].Draw("same")
       posx=0.15+0.74*(z-1)/nx
       label2.append(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
       '''
       label2[z-1].AddText(myvariable+" #in [0,0.2]")
       if z==2:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           label2[z-1].AddText(myvariable+" #in [0.2,0.4]")
       elif z==3:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
       elif z==4:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
       '''
       if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0,0.2]")
       else:
                label2[z-1].AddText(myvariable+" #in [0,0.35]")
       if z==2:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.2,0.4]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.35,0.5]")

       elif z==3:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           #label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.5,0.65]")

       elif z==4:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           #label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.65,1.0]")

       label2[z-1].SetBorderSize(   0 )
       label2[z-1].SetFillStyle(    0 )
       label2[z-1].SetTextAlign(   12 )
       label2[z-1].SetTextSize ( 0.05 )
       label2[z-1].SetTextColor(    1 )
       label2[z-1].SetTextFont (   42 )
       label2[z-1].Draw("same")
elif args.channel=="et" and args.year=="2016":
   nx=4
   ny=8
   for z in range(1, nx+1):
       line2.append(ROOT.TLine(z*ny,0,z*ny,hist_D_em.GetMaximum()))
       line2[z-1].SetLineStyle(3)
       line2[z-1].Draw("same")
       posx=0.15+0.74*(z-1)/nx
       label2.append(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
       '''
       label2[z-1].AddText(myvariable+" #in [0,0.2]")
       if z==2:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           label2[z-1].AddText(myvariable+" #in [0.2,0.4]")
       elif z==3:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
       elif z==4:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
       '''
       if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0,0.2]")
       else:
                label2[z-1].AddText(myvariable+" #in [0,0.35]")
       if z==2:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.2,0.4]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.35,0.5]")

       elif z==3:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           #label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.5,0.65]")

       elif z==4:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           #label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.65,1.0]")

       label2[z-1].SetBorderSize(   0 )
       label2[z-1].SetFillStyle(    0 )
       label2[z-1].SetTextAlign(   12 )
       label2[z-1].SetTextSize ( 0.05 )
       label2[z-1].SetTextColor(    1 )
       label2[z-1].SetTextFont (   42 )
       label2[z-1].Draw("same")
elif args.channel=="em":
   nx=4
   ny=16
   for z in range(1, nx+1):
       line2.append(ROOT.TLine(z*ny,0,z*ny,hist_D_em.GetMaximum()))
       line2[z-1].SetLineStyle(3)
       line2[z-1].Draw("same")
       posx=0.15+0.74*(z-1)/nx
       label2.append(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
       '''
       label2[z-1].AddText(myvariable+" #in [0,0.2]")
       if z==2:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           label2[z-1].AddText(myvariable+" #in [0.2,0.4]")
       elif z==3:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
       elif z==4:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
       '''
       if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0,0.2]")
       else:
                label2[z-1].AddText(myvariable+" #in [0,0.35]")
       if z==2:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.2,0.4]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.35,0.5]")

       elif z==3:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           #label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.5,0.65]")

       elif z==4:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           #label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.65,1.0]")

       label2[z-1].SetBorderSize(   0 )
       label2[z-1].SetFillStyle(    0 )
       label2[z-1].SetTextAlign(   12 )
       label2[z-1].SetTextSize ( 0.05 )
       label2[z-1].SetTextColor(    1 )
       label2[z-1].SetTextFont (   42 )
       label2[z-1].Draw("same")

else: #tt
   nx=4
   ny=6 # 6->8
   for z in range(1, nx+1):
       line2.append(ROOT.TLine(z*ny,0,z*ny,hist_D_em.GetMaximum()))
       line2[z-1].SetLineStyle(3)
       line2[z-1].Draw("same")
       posx=0.15+0.74*(z-1)/nx
       label2.append(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
       #label2[z-1].AddText(myvariable+" #in [0,0.2]")
       '''
       if z==2:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           label2[z-1].AddText(myvariable+" #in [0.2,0.4]")
       elif z==3:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
       elif z==4:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
       '''
       if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0,0.2]")
       else:
                label2[z-1].AddText(myvariable+" #in [0,0.35]")
       if z==2:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.2,0.4]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.35,0.5]")

       elif z==3:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           #label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.4,0.8]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.5,0.65]")

       elif z==4:
           label2[z-1]=(ROOT.TPaveText(posx, 0.75, posx+0.15, 0.75+0.155, "NDC"))
           #label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
           if args.variable!="a3_ggH":
                label2[z-1].AddText(myvariable+" #in [0.8,1.0]")
           else:
                label2[z-1].AddText(myvariable+" #in [0.65,1.0]")

       label2[z-1].SetBorderSize(   0 )
       label2[z-1].SetFillStyle(    0 )
       label2[z-1].SetTextAlign(   12 )
       label2[z-1].SetTextSize ( 0.05 )
       label2[z-1].SetTextColor(    1 )
       label2[z-1].SetTextFont (   42 )
       label2[z-1].Draw("same")


line=[]
label=[]
text=[]
if args.channel=="mt":
   nx=16
   ny=2
   for z in range(1, nx+1):
       line.append(ROOT.TLine(z*ny,0,z*ny,0.085*hist_D_em.GetMaximum()))
       line[z-1].SetLineStyle(5)
       line[z-1].SetLineColor(4)
       line[z-1].Draw("same")
       posx=0.113+0.75*(z-1)/nx
       label.append(ROOT.TPaveText(posx, 0.33, posx+0.15, 0.5, "NDC"))

       text.append(label[z-1].AddText("NN_{disc} #in [0,0.05]"))
       if (int(z-1)%4==1):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC")
          text[z-1]=label[z-1].AddText("NN_{disc} #in [0.05,0.3]")
       if (int(z-1)%4==2):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC")
          text[z-1]=label[z-1].AddText("NN_{disc} #in [0.3,0.7]")
       elif (int(z-1)%4==3):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.58, "NDC")
          #text[z-1]=label[z-1].AddText("NN_{disc} > 1100 GeV")
          text[z-1]=label[z-1].AddText("NN_{disc} #in [0.7,1.0]")

   
       label[z-1].SetBorderSize(   0 )
       label[z-1].SetFillStyle(    0 )
       label[z-1].SetTextAlign(   12 )
       label[z-1].SetTextSize ( 0.05 )
       label[z-1].SetTextColor(    4 )
       label[z-1].SetTextFont (   42 )
       text[z-1].SetTextAngle(90)
       label[z-1].Draw("same")
elif args.channel=="et" and args.year!="2016":
   nx=12
   ny=2
   for z in range(1, nx+1):
       line.append(ROOT.TLine(z*ny,0,z*ny,0.085*hist_D_em.GetMaximum()))
       line[z-1].SetLineStyle(5)
       line[z-1].SetLineColor(4)
       line[z-1].Draw("same")
       posx=0.113+0.75*(z-1)/nx
       label.append(ROOT.TPaveText(posx, 0.33, posx+0.15, 0.5, "NDC"))

       text.append(label[z-1].AddText("NN_{disc} #in [0,0.05]"))
       if (int(z-1)%4==1):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC")
          text[z-1]=label[z-1].AddText("NN_{disc} #in [0.05,0.9]")
       if (int(z-1)%4==2):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC")
          text[z-1]=label[z-1].AddText("NN_{disc} #in [0.9,1.0]")
       #elif (int(z-1)%4==3):
       #   label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.58, "NDC")
       #   #text[z-1]=label[z-1].AddText("NN_{disc} > 1100 GeV")
       #   text[z-1]=label[z-1].AddText("NN_{disc} #in [0.7,1.0]")


       label[z-1].SetBorderSize(   0 )
       label[z-1].SetFillStyle(    0 )
       label[z-1].SetTextAlign(   12 )
       label[z-1].SetTextSize ( 0.05 )
       label[z-1].SetTextColor(    4 )
       label[z-1].SetTextFont (   42 )
       text[z-1].SetTextAngle(90)
       label[z-1].Draw("same")
elif args.channel=="et" and args.year=="2016":
   nx=16
   ny=2
   for z in range(1, nx+1):
       line.append(ROOT.TLine(z*ny,0,z*ny,0.085*hist_D_em.GetMaximum()))
       line[z-1].SetLineStyle(5)
       line[z-1].SetLineColor(4)
       line[z-1].Draw("same")
       posx=0.113+0.75*(z-1)/nx
       label.append(ROOT.TPaveText(posx, 0.33, posx+0.15, 0.5, "NDC"))

       text.append(label[z-1].AddText("NN_{disc} #in [0,0.2]"))
       if (int(z-1)%4==1):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC")
          text[z-1]=label[z-1].AddText("NN_{disc} #in [0.2,0.4]")
       if (int(z-1)%4==2):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC")
          text[z-1]=label[z-1].AddText("NN_{disc} #in [0.4,0.7]")
       elif (int(z-1)%4==3):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC")
          #text[z-1]=label[z-1].AddText("NN_{disc} > 1100 GeV")
          text[z-1]=label[z-1].AddText("NN_{disc} #in [0.7,1.0]")


       label[z-1].SetBorderSize(   0 )
       label[z-1].SetFillStyle(    0 )
       label[z-1].SetTextAlign(   12 )
       label[z-1].SetTextSize ( 0.05 )
       label[z-1].SetTextColor(    4 )
       label[z-1].SetTextFont (   42 )
       text[z-1].SetTextAngle(90)
       label[z-1].Draw("same")
elif args.channel=="em":
   nx=16
   ny=4
   for z in range(1, nx+1):
       line.append(ROOT.TLine(z*ny,0,z*ny,0.085*hist_D_em.GetMaximum()))
       line[z-1].SetLineStyle(5)
       line[z-1].SetLineColor(4)
       line[z-1].Draw("same")
       posx=0.113+0.75*(z-1)/nx
       label.append(ROOT.TPaveText(posx, 0.33, posx+0.15, 0.5, "NDC"))

       text.append(label[z-1].AddText("NN_{disc} #in [0,0.1]"))
       if (int(z-1)%4==1):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC")
          text[z-1]=label[z-1].AddText("NN_{disc} #in [0.1,0.7]")
       elif (int(z-1)%4==2):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC")
          text[z-1]=label[z-1].AddText("NN_{disc} #in [0.7,0.9]")
       elif (int(z-1)%4==3):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC")
          #text[z-1]=label[z-1].AddText("NN_{disc} > 1100 GeV")
          text[z-1]=label[z-1].AddText("NN_{disc} #in [0.9,1.0]")


       label[z-1].SetBorderSize(   0 )
       label[z-1].SetFillStyle(    0 )
       label[z-1].SetTextAlign(   12 )
       label[z-1].SetTextSize ( 0.05 )
       label[z-1].SetTextColor(    4 )
       label[z-1].SetTextFont (   42 )
       text[z-1].SetTextAngle(90)
       label[z-1].Draw("same")
else: # tt
   nx=12 # 16->12
   ny=2
   for z in range(1, nx+1):
       line.append(ROOT.TLine(z*ny,0,z*ny,0.085*hist_D_em.GetMaximum()))
       line[z-1].SetLineStyle(5)
       line[z-1].SetLineColor(4)
       line[z-1].Draw("same")
       posx=0.109+0.75*(z-1)/nx
       label.append(ROOT.TPaveText(posx, 0.33, posx+0.15, 0.5, "NDC"))

       text.append(label[z-1].AddText("NN_{disc} #in [0,0.4]"))
       if (int(z-1)%3==1):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC")
	  if args.year=="2016" and args.variable=="a3_ggH":
          	text[z-1]=label[z-1].AddText("NN_{disc} #in [0.4,0.6]")
          else:
                text[z-1]=label[z-1].AddText("NN_{disc} #in [0.4,0.7]")
       if (int(z-1)%3==2):
          label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.42, "NDC")
          text[z-1]=label[z-1].AddText("NN_{disc} #in [0.7,1.0]")
       #elif (int(z-1)%4==3):
       #   label[z-1]=ROOT.TPaveText(posx, 0.33, posx+0.15, 0.58, "NDC")
       #   #text[z-1]=label[z-1].AddText("NN_{disc} > 1100 GeV")
       #   text[z-1]=label[z-1].AddText("NN_{disc} #in [0.7,1.0]")

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
if (((args.channel == "et" or args.year!="2016") or args.channel == "tt") and (args.channel != "em") and (args.channel == "et" and args.year!="2016") or args.channel == "tt"):
   print " \t ========>  this is et/tt!!! "

   h1.GetXaxis().SetBinLabel(1,"0-0.5")
   h1.GetXaxis().SetBinLabel(2,"0.5-1")
   h1.GetXaxis().SetBinLabel(3,"0-0.5")
   h1.GetXaxis().SetBinLabel(4,"0.5-1")
   h1.GetXaxis().SetBinLabel(5,"0-0.5")
   h1.GetXaxis().SetBinLabel(6,"0.5-1")
   h1.GetXaxis().SetBinLabel(7,"0-0.5")
   h1.GetXaxis().SetBinLabel(8,"0.5-1")
   h1.GetXaxis().SetBinLabel(9,"0-0.5")
   h1.GetXaxis().SetBinLabel(10,"0.5-1")
   h1.GetXaxis().SetBinLabel(11,"0-0.5")
   h1.GetXaxis().SetBinLabel(12,"0.5-1")
   h1.GetXaxis().SetBinLabel(13,"0-0.5")
   h1.GetXaxis().SetBinLabel(14,"0.5-1")
   h1.GetXaxis().SetBinLabel(15,"0-0.5")
   h1.GetXaxis().SetBinLabel(16,"0.5-1")
   h1.GetXaxis().SetBinLabel(17,"0-0.5")
   h1.GetXaxis().SetBinLabel(18,"0.5-1")
   h1.GetXaxis().SetBinLabel(19,"0-0.5")
   h1.GetXaxis().SetBinLabel(20,"0.5-1")
   h1.GetXaxis().SetBinLabel(21,"0-0.5")
   h1.GetXaxis().SetBinLabel(22,"0.5-1")
   h1.GetXaxis().SetBinLabel(23,"0-0.5")
   h1.GetXaxis().SetBinLabel(24,"0.5-1")
elif args.channel == "em":
   print " \t ========>  this is em!!! "
   h1.GetXaxis().SetBinLabel(1,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(2,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(3,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(4,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(5,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(6,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(7,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(8,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(9,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(10,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(11,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(12,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(13,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(14,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(15,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(16,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(17,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(18,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(19,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(20,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(21,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(22,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(23,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(24,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(25,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(26,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(27,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(28,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(29,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(30,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(31,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(32,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(33,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(34,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(35,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(36,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(37,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(38,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(39,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(40,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(41,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(42,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(43,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(44,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(45,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(46,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(47,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(48,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(49,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(50,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(51,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(52,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(53,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(54,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(55,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(56,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(57,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(58,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(59,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(60,"0.75-1.0")
   h1.GetXaxis().SetBinLabel(61,"0.0-0.25")
   h1.GetXaxis().SetBinLabel(62,"0.25-0.5")
   h1.GetXaxis().SetBinLabel(63,"0.5-0.75")
   h1.GetXaxis().SetBinLabel(64,"0.75-1.0")

elif (args.channel == "et" or args.year=="2016") or args.channel == "mt":
   print " \t ========>  this is et/tti 2016 w!!! "
   h1.GetXaxis().SetBinLabel(1,"0-0.5")
   h1.GetXaxis().SetBinLabel(2,"0.5-1")
   h1.GetXaxis().SetBinLabel(3,"0-0.5")
   h1.GetXaxis().SetBinLabel(4,"0.5-1")
   h1.GetXaxis().SetBinLabel(5,"0-0.5")
   h1.GetXaxis().SetBinLabel(6,"0.5-1")
   h1.GetXaxis().SetBinLabel(7,"0-0.5")
   h1.GetXaxis().SetBinLabel(8,"0.5-1")
   h1.GetXaxis().SetBinLabel(9,"0-0.5")
   h1.GetXaxis().SetBinLabel(10,"0.5-1")
   h1.GetXaxis().SetBinLabel(11,"0-0.5")
   h1.GetXaxis().SetBinLabel(12,"0.5-1")
   h1.GetXaxis().SetBinLabel(13,"0-0.5")
   h1.GetXaxis().SetBinLabel(14,"0.5-1")
   h1.GetXaxis().SetBinLabel(15,"0-0.5")
   h1.GetXaxis().SetBinLabel(16,"0.5-1")
   h1.GetXaxis().SetBinLabel(17,"0-0.5")
   h1.GetXaxis().SetBinLabel(18,"0.5-1")
   h1.GetXaxis().SetBinLabel(19,"0-0.5")
   h1.GetXaxis().SetBinLabel(20,"0.5-1")
   h1.GetXaxis().SetBinLabel(21,"0-0.5")
   h1.GetXaxis().SetBinLabel(22,"0.5-1")
   h1.GetXaxis().SetBinLabel(23,"0-0.5")
   h1.GetXaxis().SetBinLabel(24,"0.5-1")
   h1.GetXaxis().SetBinLabel(25,"0-0.5")
   h1.GetXaxis().SetBinLabel(26,"0.5-1")
   h1.GetXaxis().SetBinLabel(27,"0-0.5")
   h1.GetXaxis().SetBinLabel(28,"0.5-1")
   h1.GetXaxis().SetBinLabel(29,"0-0.5")
   h1.GetXaxis().SetBinLabel(30,"0.5-1")
   h1.GetXaxis().SetBinLabel(31,"0-0.5")
   h1.GetXaxis().SetBinLabel(32,"0.5-1")


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
categ2.AddText("D_{2jets}^{VBF}")
categ2.Draw("same")

c.cd()
pad1.Draw()

ROOT.gPad.RedrawAxis()

c.Modified()
c.SaveAs("plots/unrolled_"+args.variable+"_"+args.channel+"_"+args.year+".pdf")
c.SaveAs("plots/unrolled_"+args.variable+"_"+args.channel+"_"+args.year+".png")



