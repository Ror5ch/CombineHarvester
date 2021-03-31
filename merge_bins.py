#!/usr/bin/env python
import ROOT
from ROOT import *

import re
# from array import array
from optparse import OptionParser
import sys
import numpy


#parser = OptionParser()
import argparse
parser = argparse.ArgumentParser("Compare total template to stage 1.1 templates")

#parser.add_option('--nbins', '-n', action='store_true',
#                  default=64, dest='nbins',
#                  help='Nbins'
#                  )
parser.add_argument(
        "--nbins",
        action="store",
        dest="nbins",
        default=64,
        help="Which file1name to run over?")
parser.add_argument(
        "--year",
        action="store",
        dest="year",
        default="2016",
        help="Which file1name to run over?")
parser.add_argument(
        "--ttoptimal",
        action="store",
        dest="ttoptimal",
        default=0,
        help="Which file1name to run over?")
parser.add_argument(
        "--useDCP",
        action="store",
        dest="useDCP",
        default=0,
        help="Use DCP bins or not (0/1) ?")
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
parser.add_argument(
        "--channel",
        action="store",
        dest="channel",
        default="tt",
        help="Which file1name to run over?")
parser.add_argument(
        "--scaleGGH",
        action="store",
        dest="scaleGGH",
        default="1",
        help="Which file1name to run over?")
parser.add_argument(
        "--scaleHWWAC",
        action="store",
        dest="scaleHWWAC",
        default="1",
        help="Which file1name to run over?")
parser.add_argument(
        "--scaleAllGGH",
        action="store",
        dest="scaleAllGGH",
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

args = parser.parse_args()

nbins=int(args.nbins)
year="_"+args.year
ttoptimal=int(args.ttoptimal)
inputfile =args.inputfile
channel =args.channel
outputfile=args.outputfile
scaleGGH =float(args.scaleGGH)
scaleHWWAC =float(args.scaleHWWAC)
scaleAllGGH =float(args.scaleAllGGH)
usePhiJJ=bool(int(args.usePhiJJ))
useDCP=int(args.useDCP)
mergeMSV=int(args.mergeMSV)


# for tt 2016, HVV:
# moreBins
binsNN=[]
binsD2jet=[]
binsD2jet_origi=[]

if nbins==64:
        binsNN=[0.,0.05,0.6,0.9,1.]
        binsD2jet=[0.,0.25,0.5,0.75,1.0]
if nbins==64 and channel == 'tt':
        binsNN=[0.,0.4,0.7,1.]
        #binsNN=[0.,0.4,0.7,1.]
        binsD2jet=[0.,0.5,1.0]
if nbins==64 and channel == 'tt' and ("2016" in year and "_fa3ggH_" in inputfile):
        binsNN=[0.,0.4,0.6,1.]
        binsD2jet=[0.,0.5,1.0]


if (channel =='mt' ) and nbins==64:
        # no merging:
        binsNN=[0,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.85,0.9,0.95,1.0]
        #binsNN=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
        #binsD2jet=[0.,0.25,0.5, 0.75,1.0]
        binsD2jet=[0.,0.125,0.25,0.375,0.5,0.625, 0.75,0.875,1.0] # before D2jet and MELA swaping
        binsD2jet=[0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]


'''
        #binsNN=[0, 0.15, 0.4, 0.6, 1.0]
        #binsNN=[0, 0.15, 0.4, 0.8, 1.0] # ggH

        #binsNN=[0, 0.1, 0.3,0.8, 1.0] 
        #binsD2jet=[0.,0.75,1.0]
        binsNN=[0, 0.1, 0.2,0.8, 1.0]
        binsD2jet=[0.,0.75,1.0]
    
    if ("2016" in year or "2017" in year):
        binsNN=[0, 0.1, 0.2,0.8, 1.0]
            binsD2jet=[0.,0.75,1.0]

        #if ("2018" in year and "_a2" in inputfile):
        #        binsNN=[0, 0.1, 0.3,0.7, 1.0]

        if ('_l1' in inputfile):
                binsNN=[0, 0.1, 0.3,0.6, 1.0]
                #binsD2jet=[0.,0.625,1.0]
                binsD2jet=[0.,0.75,1.0]
                if ("2016" in year):
            binsNN=[0, 0.1, 0.2,0.7, 1.0]
            binsD2jet=[0.,0.75,1.0]
                if ("2018" in year):
            binsNN=[0, 0.2, 0.4,0.6, 1.0]
            binsD2jet=[0.,0.75,1.0]
        if ('_l1zg' in inputfile):
                #binsNN=[0, 0.1, 0.3, 0.5, 1.0] #Aug binning
                #binsD2jet=[0.,0.75,1.0] #Aug binning
                binsNN=[0, 0.1, 0.3, 0.7, 1.0] 
                binsD2jet=[0.,0.5,1.0]

        if ("2016" in year):
            binsNN=[0, 0.1, 0.3, 0.4, 1.0]
            binsD2jet=[0.,0.75,1.0]
        #binsD2jet=[0.,0.25,0.5,0.75,1.0]
    if "_ggh." in inputfile:
            binsNN=[0, 0.15, 0.4,0.8, 1.0]
            #binsD2jet=[0.,0.25,0.5,0.75,1.0]
                binsD2jet=[0.,0.5,0.75,1.0]

        # fastMTT test
                #binsNN=[0,0.05, 0.15, 0.4,0.95, 1.0]
                #binsD2jet=[0.,0.25,0.5,0.75,1.0]

        if "2016" in year:
            binsNN=[0, 0.1, 0.4,0.8, 1.0]
'''

if ( channel =='et') and nbins==64:

        # no merging:
        binsNN=[0,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.85,0.9,0.95,1.0]
        binsD2jet=[0.,0.125,0.25,0.375,0.5,0.625, 0.75,0.875,1.0]

        binsD2jet=[0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

'''
        #binsNN=[0, 0.15, 0.4, 0.6, 1.0]
        #binsNN=[0, 0.15, 0.4, 0.8, 1.0] # ggH
        #binsNN=[0, 0.1, 0.2,0.6, 1.0]     
        binsNN=[0, 0.1, 0.2,0.7, 1.0]

        binsD2jet=[0.,0.75,1.0]
        #binsD2jet=[0.,0.25,0.5,0.75,1.0]
    
    if ("2016" in year or "2017" in year):
                binsD2jet=[0.,0.75,1.0]
        if ("2016" in year and '_l1zg' in inputfile):
        binsNN=[0, 0.1, 0.2,0.6, 1.0]
        binsD2jet=[0.,0.5,1.0]
        if ('_l1' in inputfile):
                binsNN=[0, 0.1, 0.3,0.6, 1.0]
                binsD2jet=[0.,0.75,1.0]
        #if ("2016" in year):
            #binsNN=[0, 0.1, 0.3, 1.0]
                    #binsD2jet=[0.,0.5,1.0]
        if ('_l1zg' in inputfile):
                binsNN=[0, 0.1, 0.2,0.6, 1.0]
                binsD2jet=[0.,0.75,1.0]
        if ("2016" in year):
            binsNN=[0, 0.1,0.6, 1.0]
            binsD2jet=[0.,0.625,1.0]
                if ("2018" in year):
                        binsD2jet=[0.,0.625,1.0]
        if "_ggh." in inputfile:
                binsNN=[0, 0.15, 0.4,0.8, 1.0]
                #binsD2jet=[0.,0.5,0.75,1.0]
            binsD2jet=[0.,0.25,0.5,0.75,1.0]

'''

'''

if (channel =='mt' ) and nbins==64 and ("2016" in year):
        binsNN=[0, 0.05, 0.15,0.5,1.0]
        binsD2jet=[0.,0.5,1.0]
if (channel =='mt' ) and nbins==64 and ("2017" in year):
        binsNN=[0, 0.05, 0.3,0.7,1.0]
        binsD2jet=[0.,0.5,1.0]
if (channel =='mt' ) and nbins==64 and ("2018" in year):
        binsNN=[0, 0.05, 0.3,0.7,1.0]
        binsD2jet=[0.,0.5,1.0]
'''

'''
if ( channel =='et') and nbins==64 and ("2016" in year):
        #binsNN=[0, 0.2, 0.3,0.7,1.0]
        #binsNN=[0, 0.1, 0.4,0.7,1.0]
        binsNN=[0,0.2, 0.4, 0.6,1.0]
        binsNN=[0, 0.05, 0.3, 0.8, 1.0]
        #binsNN=[0,0.7,1.0]
        binsD2jet=[0.,0.75,1.0]
if ( channel =='et') and nbins==64 and ("2017" in year):
        #binsNN=[0, 0.2, 0.3,0.7,1.0]
        #binsNN=[0, 0.1, 0.4,0.7,1.0]
        binsNN=[0, 0.7,0.9,1.0]
        binsD2jet=[0.,0.5,1.0]
if ( channel =='et') and nbins==64 and ("2018" in year):
        #binsNN=[0, 0.2, 0.3,0.7,1.0]
        #binsNN=[0, 0.1, 0.4,0.7,1.0]
        binsNN=[0, 0.05,0.9,1.0]
        binsD2jet=[0.,0.5,1.0]
'''



if (channel =='em') and nbins==64:
    # no merging:
 #        binsNN=[0,0.1001,0.2001,0.3001,0.4001,0.5001,0.6001,0.7001,0.8001,0.9001,1.0]
    # binsNN=[0.0, 0.10000000149011612, 0.20000000298023224, 0.30000001192092896, 0.4000000059604645, 0.5, 0.6000000238418579, 0.699999988079071, 0.800000011920929, 0.8999999761581421, 1.0]
 #        binsD2jet=[0.,0.125,0.25,0.375,0.5,0.625, 0.75,0.875,1.0]

        # binsD2jet=[0.0, 0.10000000149011612, 0.20000000298023224, 0.30000001192092896, 0.4000000059604645, 0.5, 0.6000000238418579, 0.699999988079071, 0.800000011920929, 0.8999999761581421, 1.0]
        # binsNN=[0.,0.125,0.25,0.375,0.5,0.625, 0.75,0.875,1.0]

        binsD2jet=[0.000,0.125,0.250,0.375,0.500,0.625,0.750,0.875,1.000]
        binsNN=[0.0, 0.10000000149011612, 0.20000000298023224, 0.30000001192092896, 0.4000000059604645, 0.5, 0.6000000238418579, 0.699999988079071, 0.800000011920929, 0.8999999761581421, 1.0]
     
        # binsNN=[0.0, 0.20000000298023224, 0.4000000059604645, 0.6000000238418579, 0.800000011920929, 1.0]



'''
        binsNN=[0,0.1001,0.7001,0.9001,1.0]
        #binsNN=[0,0.1001,0.5001,0.9001,1.0] # optimistic scenario
        binsNN=[0,0.2001,0.4001,1.0] # works for all parameters in 2016 # conservative scenario
        #binsNN=[0,0.1001,0.5001,0.8001,1.0]
        #binsNN=[0,0.1001,0.8001,1.0] # ok
        #binsNN=[0,0.1001,0.7001,1.0] #
        #binsNN=[0,0.1001,0.2001,0.8001,1.0]

        #binsD2jet=[0.,0.25,0.5,0.75,1.0]
        #binsD2jet=[0.,0.5,0.75,1.0]
        binsD2jet=[0.,0.5,1.0]


    #print "is em year:",year
    if (year=="_2017"):
            binsNN=[0,0.1001,0.3001,0.8001,1.0]
            binsD2jet=[0.,0.75,1.0]
        #binsD2jet=[0.,0.625,1.0] # for FL1
        elif (year=="_2018"):
                binsNN=[0,0.2001,0.5001,0.8001,1.0]
                binsD2jet=[0.,0.5,1.0]
                binsD2jet=[0.,0.75,1.0] # for fa3
                binsD2jet=[0.,0.25,0.5,0.75,1.0] # for fa3
    # new binning (June 2020):
    binsNN=[0,0.2001,0.5001,0.8001,1.0]
        binsNN=[0,0.3001,0.5001,0.8001,1.0]
    #binsNN=[0,0.3001,0.5001,0.7001,1.0]
    binsNN=[0,0.3001,0.5001,0.6001,0.8001,0.9001,1.0] #Abdollah's binning

    #binsNN=[0, 0.5001, 0.60001, 0.7001,0.8001, 1.0]
        #binsD2jet=[0.,0.5,0.75,1.0] # for fa3
        binsD2jet=[0.,0.5,0.625,1.0] # for fa3
        #binsD2jet=[0.,0.25,0.5,0.75,1.0] # for fa3 #Abdollah's binning
        binsD2jet=[0.,0.25,0.5,0.75,1.0] # for fa3_ggH Jun22

    #if ('_ggh' in inputfile and year=="_2018"):
        if ('_ggh' in inputfile):
            binsNN=[0,0.3001,0.5001,0.8001,1.0]
        binsNN=[0,0.3001,0.4001,0.5001,0.6001,0.7001,0.8001,0.9001,1.0]
                binsD2jet=[0.,0.25,0.5,0.75,1.0]
        # for AutoRebin testing:
                #binsNN=[0,0.1001,0.2001,0.3001, 0.4001,0.5001,0.6001,0.7001,0.8001,0.9001,1.0]
                #binsD2jet=[0.,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0]
                # for testing Abdollah's binning: bins_vbf_var1{0, 0.25, 0.5, 0.75, 1.} bins_vbf_var2{0,0.3,0.4,0.5,0.6,0.7, 0.8,0.9,1.0}, //New NN binning
                #binsNN=[0,0.3001, 0.4001,0.5001,0.6001,0.7001,0.8001,0.9001,1.0]
                #binsD2jet=[0.,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0]
                #binsNN=[0,0.5001,0.6001,0.7001,0.8001,1.0]
                #binsD2jet=[0.,0.25,0.5,0.75,1.0]
        if year!="_2018":
            binsD2jet=[0.,0.5,0.75,1.0]
        else:
            binsD2jet=[0.,0.25,0.5,1.0]

    # for Abdollah's NN:D0- only scenario:
        #binsNN=[0,0.3001, 0.4001, 0.5001, 0.60001, 0.7001,0.8001,0.9001, 1.0]
        #binsD2jet=[0.,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0] # for fa3_ggH Jun22


        if ('_l1zg' in inputfile):
                binsD2jet=[0.,0.5,1.0]
        elif ('_l1' in inputfile):
                binsD2jet=[0.,0.5,1.0]
                binsNN=[0,0.3001,0.5001,0.8001,1.0]

                #binsD2jet=[0.,0.375,1.0]
        #binsNN=[0,0.2001,0.4001,0.6001,1.0]
        if (year!="_2018"):
            binsD2jet=[0.,0.375,1.0]
                if (year=="_2017"):
            #binsNN=[0,0.3001,0.5001,0.7001,1.0]
            binsD2jet=[0.,0.25,1.0]
        elif ('_hvv_201' in inputfile):
                #binsD2jet=[0.,0.375,0.625,1.0]
                #binsNN=[0,0.3001,0.4001,0.5001,0.6001,0.8001,1.0]

                binsD2jet=[0.,0.625,1.0]
                binsNN=[0,0.3001,0.5001,0.8001,1.0]
        if (year=="_2018" and '_a2' in inputfile): # do no merging for AutoRebin test
                binsNN=[0,0.1001,0.2001,0.3001,0.4001,0.5001,0.6001,0.7001,0.8001,0.9001,1.0]
                binsD2jet=[0.,0.125,0.25,0.375,0.5,0.625, 0.75,0.875,1.0]
'''
       #print "  is em 2017!!! "

#if (channel =='em') and nbins==64:
#        binsNN=[0,0.1001,0.7001,0.9001,1.0]
#        binsD2jet=[0.,0.5,1.0]


if nbins==24:
        binsNN=[0.,0.05,0.7,1.]
        binsD2jet=[0.,0.5,1.0]

if nbins==24 and ttoptimal==1:
        binsNN=[0.,2.,13.,18.]
        binsD2jet=[0.,2.,4.]


if (channel =='mt' or channel =='et') and nbins==24:
        binsNN=[0,0.05, 0.7,1.0]
        binsD2jet=[0,0.5,1.0]
if (channel =='em') and nbins==24:
        binsNN=[0,0.1001,0.7001,1.0]
        binsD2jet=[0.,0.5,1.0]

if usePhiJJ:
        binsNN=[50,80,100,115,130,150,200]
        binsD2jet=[-3.20000,-2.66666, -2.13332,-1.60000,-1.06666,-0.533333,0.00000,0.533334,1.06667,1.60000,2.13334,2.66667,3.20000]


file=ROOT.TFile(inputfile,"r")
file.cd()
dirList = gDirectory.GetListOfKeys()

ofile=ROOT.TFile(outputfile,"recreate")
categories_list= file.GetListOfKeys()
categories=[]
for k2 in categories_list:
    categories.append(k2.GetName())

print "\t\t ========>>>  using NN: ", binsNN, " D2jet: ",binsD2jet

def rename_histo(name_histo):
    if channel=='em':
        name_histo=name_histo.replace("prefiring_down", "CMS_prefiringDown")
        name_histo=name_histo.replace("prefiring_up", "CMS_prefiringUp")
        #name_histo=name_histo.replace("QCDUp","QCD_QCDUp")
        #name_histo=name_histo.replace("QCDDown","QCD_QCDDown")
        name_histo=name_histo.replace("QCDsystyear_Up","QCD_QCDUp")
        name_histo=name_histo.replace("QCDsystyear_Down","QCD_QCDDown")
        name_histo=name_histo.replace("_Jet","_CMS_Jet")
        name_histo=name_histo.replace("_JER","_CMS_JER")

    name_histo=name_histo.replace("Rivet0","THU_ggH_Mu")
    name_histo=name_histo.replace("Rivet1","THU_ggH_Res")
    name_histo=name_histo.replace("Rivet2","THU_ggH_Mig01")
    name_histo=name_histo.replace("Rivet3","THU_ggH_Mig12")
    name_histo=name_histo.replace("Rivet4","THU_ggH_VBF2j")
    name_histo=name_histo.replace("Rivet5","THU_ggH_VBF3j")
    name_histo=name_histo.replace("Rivet6","THU_ggH_PT60")
    name_histo=name_histo.replace("Rivet7","THU_ggH_PT120")
    name_histo=name_histo.replace("Rivet8","THU_ggH_qmtop")


    name_histo=name_histo.replace("_ClusteredMet_","_CMS_scale_met_clustered_13TeV"+year)
    name_histo=name_histo.replace("_UncMet_","_CMS_scale_met_unclustered_13TeV"+year)
    name_histo=name_histo.replace("JetUES_","_CMS_scale_met_unclustered_13TeV"+year)
    name_histo=name_histo.replace("_dyShape_","_CMS_htt_dyShape_13TeV"+year)
    name_histo=name_histo.replace("_ttbarShape_","_CMS_htt_ttbarShape_13TeV"+year)
    name_histo=name_histo.replace("_zmumuShape_","_CMS_htt_zmumuShape_VBF_13TeV"+year)
    name_histo=name_histo.replace("_vbfMass_","_")
    name_histo=name_histo.replace("CMS_htt_prefiring","CMS_prefiring")
    
    if (channel=='mt' or channel=='et'):
        name_histo=name_histo.replace("_scale_e"+year,"_scale_e")

    if (channel=='mt' or channel=='et') and ("tauideff" in name_histo or "scale_e" in name_histo or "_scale_t_" in name_histo or "scale_j" in name_histo or "eff_t_embedded" in name_histo or "BBEC1" in name_histo or "JetAbsolute" in name_histo or "JetEC2" in name_histo or "JetHF" in name_histo or "JER" in name_histo or "trg" in name_histo):
        #print "adding year to tauideff"
        name_histo=name_histo.replace("_2016","_13TeV"+year)
        name_histo=name_histo.replace("_2017","_13TeV"+year)
        name_histo=name_histo.replace("_2018","_13TeV"+year)
        #print "adding year to tauideff: %s"%(name_histo)
    if channel=='mt' or channel=='et':
        name_histo=name_histo.replace("embed","embedded")
        name_histo=name_histo.replace("eddedd","edd")
        name_histo=name_histo.replace("ZTT","embedded")
        name_histo=name_histo.replace("FlavorQCD_","FlavorQCD")
        name_histo=name_histo.replace("CHAN",channel)
        name_histo=name_histo.replace("_YEAR",year)
        name_histo=name_histo.replace("_tt_0jet_unc","_tt_unc")

        name_histo=name_histo.replace("WH_signed_","WH_")


    #if channel=='em' and 'emb' in inputfile:
    if channel=='em':
        name_histo=name_histo.replace("ZTT","embedded")
        name_histo=name_histo.replace("HWW","hww125")

    name_histo=name_histo.replace("_Up","Up")
    name_histo=name_histo.replace("_Down","Down")

    name_histo=name_histo.replace("2016","13TeV")
    name_histo=name_histo.replace("2017","13TeV")
    name_histo=name_histo.replace("2018","13TeV")
    name_histo=name_histo.replace("CMS_htt_CMS_htt","CMS_htt")
    name_histo=name_histo.replace("13TeV13TeV","13TeV")
    name_histo=name_histo.replace("_CMS_scale_jet_","_Jet")
    name_histo=name_histo.replace("_madgraph_ggH125","")
    name_histo=name_histo.replace("_v1_ggH125","")
    name_histo=name_histo.replace("_ggH125","")
    #if "_Jet" in name_histo:
    #    name_histo=name_histo.replace("Up","_13TeV"+year+"Up")
    #    name_histo=name_histo.replace("Down","_13TeV"+year+"Down")

    if channel=='em' or channel=='et' or channel=='mt':
        name_histo=name_histo.replace("_13TeV_13TeV","_13TeV"+year)

    if channel=='mt' or channel=='et' or channel=='tt':
        name_histo=name_histo.replace("_1prong1pizero_13TeV","_1prong1pizero_13TeV"+year)
        name_histo=name_histo.replace("_1prong_13TeV","_1prong_13TeV"+year)
        name_histo=name_histo.replace("_3prong_13TeV","_3prong_13TeV"+year) 
        name_histo=name_histo.replace("_1pizero_13TeV","_1pizero_13TeV"+year)
        name_histo=name_histo.replace("_13TeV_13TeV","_13TeV"+year)
        name_histo=name_histo.replace("_up","_13TeV"+year+"Up")
        name_histo=name_histo.replace("_down","_13TeV"+year+"Down")
        name_histo=name_histo.replace("_stat","_"+channel+"_stat")
        name_histo=name_histo.replace("_dm0","_1prong")
        name_histo=name_histo.replace("_dm1","_3prong")
        name_histo=name_histo.replace("_CMS_htt_ff","_ff")

    if 'clustered' in name_histo or "rawFF" in name_histo or "embed" in name_histo:
        name_histo=name_histo.replace("_13TeV","_13TeV"+year)

    if "_boson" in name_histo or "scale_t_id_" in name_histo:
        name_histo=name_histo.replace("_13TeV","_13TeV"+year)

    if channel=='tt':
        name_histo=name_histo.replace("_1prong1pizero","_1prong1pizero_13TeV"+year)
        name_histo=name_histo.replace("_1prongUp","_1prong_13TeV"+year+"Up")
        name_histo=name_histo.replace("_3prongUp","_3prong_13TeV"+year+"Up")
        name_histo=name_histo.replace("_3prongDown","_3prong_13TeV"+year+"Down")

        name_histo=name_histo.replace("_1prongDown","_1prong_13TeV"+year+"Down")
        name_histo=name_histo.replace("_1pizero","_1pizero_13TeV"+year)
        name_histo=name_histo.replace("clustered","clustered_13TeV"+year)
        name_histo=name_histo.replace("_dyShape","_dyShape_13TeV"+year)

    name_histo=name_histo.replace("_2016_2016","_2016")
    name_histo=name_histo.replace("_2017_2017","_2017")
    name_histo=name_histo.replace("_2018_2018","_2018")
    name_histo=name_histo.replace("_2016_2016","_2016")
    name_histo=name_histo.replace("_2017_2017","_2017")
    name_histo=name_histo.replace("_2018_2018","_2018")

    if channel=='em' or channel=='et' or channel=='mt':
        name_histo=name_histo.replace("__","_")
        name_histo=name_histo.replace("JHU_rew","JHU__rew")


    if channel=='em' and "EE" in name_histo:
        name_histo=name_histo.replace("EESigma","CMS_scale_e_Sigma_13TeV")
        #name_histo=name_histo.replace("EEScale","CMS_scale_e_Scale_13TeV")
        name_histo=name_histo.replace("EEScale","CMS_scale_e")

    name_histo=name_histo.replace("_JetRelSam","_JetRelativeSample"+year)
    name_histo=name_histo.replace("JetRelBal","JetRelativeBal")

    if channel!='et' and channel!='mt':     
        name_histo=name_histo.replace("JER","JER"+year)
        name_histo=name_histo.replace("JetJER","JER")
        name_histo=name_histo.replace("JetAbsoluteyear","JetAbsolute"+year)
        name_histo=name_histo.replace("JetEC2year","JetEC2"+year)
        name_histo=name_histo.replace("JetHFyear","JetHF"+year)
        name_histo=name_histo.replace("_201","_13TeV_201")
        name_histo=name_histo.replace("_13TeV_13TeV","_13TeV")
        name_histo=name_histo.replace("year","_13TeV"+year)
    if channel=='em':
        name_histo=name_histo.replace("_13TeV_201","_201")
    if channel=='mt' or channel=='et':
        name_histo=name_histo.replace("_13TeV_201","_201")
        name_histo=name_histo.replace("eta2p1to2p4p","eta2p1to2p4Up")
    if "FF_closure" in name_histo:
        name_histo=name_histo.replace("_13TeV","")
        name_histo=name_histo.replace("_OSSS_mvis_mt_qcd","_OSSS_mvis_mt_qcd"+year)
        name_histo=name_histo.replace("_OSSS_mvis_et_qcd","_OSSS_mvis_et_qcd"+year)
        name_histo=name_histo.replace("_mt_et_w_unc1","_mt_et_w_unc1"+year)
        name_histo=name_histo.replace("_mt_et_w_unc2","_mt_et_w_unc2"+year)
        name_histo=name_histo.replace("_mt_mt_w_unc1","_mt_mt_w_unc1"+year)
        name_histo=name_histo.replace("_mt_mt_w_unc2","_mt_mt_w_unc2"+year)
    if channel=='mt':
        name_histo=name_histo.replace("_singlemutrg_emb_","_singlemutrg_")
        name_histo=name_histo.replace("_mutautrg_emb_","_mutautrg_")
    if usePhiJJ and channel=='em':
        name_histo=name_histo.replace("qqH_htt_0M125","reweighted_qqH_htt_0M125")
        name_histo=name_histo.replace("qqH_htt_0PM125","reweighted_qqH_htt_0PM125")


    if channel == 'em': 
        name_histo=name_histo.replace("CMS_htt_emb_ttbar_YEAR", "CMS_htt_emb_ttbar"+year)
        name_histo=name_histo.replace("RecoilReso_njets0_YEAR", "CMS_htt_boson_reso_met_0jet"+year)
        name_histo=name_histo.replace("RecoilReso_njets1_YEAR", "CMS_htt_boson_reso_met_1jet"+year)
        name_histo=name_histo.replace("RecoilReso_njets2_YEAR", "CMS_htt_boson_reso_met_2jet"+year)
        name_histo=name_histo.replace("RecoilResp_njets0_YEAR", "CMS_htt_boson_scale_met_0jet"+year)
        name_histo=name_histo.replace("RecoilResp_njets1_YEAR", "CMS_htt_boson_scale_met_1jet"+year)
        name_histo=name_histo.replace("RecoilResp_njets2_YEAR", "CMS_htt_boson_scale_met_2jet"+year)
        name_histo=name_histo.replace("CMS_CMS_scale_met_unclustered","CMS_scale_met_unclustered")
        name_histo=name_histo.replace("CMS_htt_dyShape_2016","CMS_htt_dyShape")
        name_histo=name_histo.replace("CMS_htt_dyShape_2017","CMS_htt_dyShape")
        name_histo=name_histo.replace("CMS_htt_dyShape_2018","CMS_htt_dyShape")
        name_histo=name_histo.replace("CMS_htt_ttbarShape_2016","CMS_htt_ttbarShape")
        name_histo=name_histo.replace("CMS_htt_ttbarShape_2017","CMS_htt_ttbarShape")
        name_histo=name_histo.replace("CMS_htt_ttbarShape_2018","CMS_htt_ttbarShape")

    if channel == "et" or channel == "mt":
        name_histo=name_histo.replace("CMS_htt_boson_reso_met_0Jet", "CMS_htt_boson_reso_met_0jet")
        name_histo=name_histo.replace("CMS_htt_boson_reso_met_1Jet", "CMS_htt_boson_reso_met_1jet")
        name_histo=name_histo.replace("CMS_htt_boson_reso_met_2Jet", "CMS_htt_boson_reso_met_2jet")
        name_histo=name_histo.replace("CMS_htt_boson_scale_met_0Jet", "CMS_htt_boson_scale_met_0jet")
        name_histo=name_histo.replace("CMS_htt_boson_scale_met_1Jet", "CMS_htt_boson_scale_met_1jet")
        name_histo=name_histo.replace("CMS_htt_boson_scale_met_2Jet", "CMS_htt_boson_scale_met_2jet")
        name_histo=name_histo.replace("CMS_htt_ttbarShape_2016","CMS_htt_ttbarShape")
        name_histo=name_histo.replace("CMS_htt_ttbarShape_2017","CMS_htt_ttbarShape")
        name_histo=name_histo.replace("CMS_htt_ttbarShape_2018","CMS_htt_ttbarShape")


    name_histo=name_histo.replace("CMS_Jet","CMS_scale_j_")
    name_histo=name_histo.replace("CMS_JER","CMS_res_j")

    if channel == "em":
        if "0jet" in nom:
            name_histo=name_histo.replace("QCDsystBkgNorm", "QCD_QCDsystBkgNorm_0jet")
        elif "boosted" in nom:
            name_histo=name_histo.replace("QCDsystBkgNorm", "QCD_QCDsystBkgNorm_boosted")
        elif "vbf" in nom:
            name_histo=name_histo.replace("QCDsystBkgNorm", "QCD_QCDsystBkgNorm_vbf")

    if channel == "et" or channel == "mt":
        name_histo=name_histo.replace("lpt_xtrg_{channel}_qcd{year}".format(channel=channel, year=year), "lpt_xtrg_{channel}_qcd".format(channel=channel))
        name_histo=name_histo.replace("lpt_xtrg_{channel}_w{year}".format(channel=channel, year=year), "lpt_xtrg_{channel}_w".format(channel=channel))
        name_histo=name_histo.replace("lpt_xtrg_{channel}_tt{year}".format(channel=channel, year=year), "lpt_xtrg_{channel}_tt".format(channel=channel))

    name_histo = name_histo.replace("_vsmu_vloose", "_vsmu_vloose{year}".format(year=year))
    name_histo = name_histo.replace("_vse_vvvloose", "_vse_vvvloose{year}".format(year=year))

    if channel == "em" and name_histo.find("embedded_CMS_scale_e") != -1:
        name_histo = name_histo.replace("CMS_scale_e", "CMS_scale_emb_e")

    if channel == "et" and name_histo.find("embedded_CMS_scale_emb_e13TeV") != -1:
        name_histo = name_histo.replace("CMS_scale_emb_e13TeV", "CMS_scale_emb_e")

    if channel == "mt" and name_histo.find("CMS_m_FakeTau") != -1:
        name_histo = name_histo.replace("_13TeV", year)

    if channel == "et" and name_histo.find("CMS_e_FakeTau") != -1:
        name_histo = name_histo.replace("_13TeV", year)

    if channel == "et" and name_histo.find("CMS_efaket_norm") != -1:
        name_histo = name_histo.replace("_13TeV", year)
        name_histo = name_histo.replace("CMS_efaket_norm", "_CMS_efaket_norm")

    if channel == "mt" and name_histo.find("CMS_mfaket_norm") != -1:
        name_histo = name_histo.replace("_13TeV", year)
        name_histo = name_histo.replace("CMS_mfaket_norm", "_CMS_mfaket_norm")

    return name_histo

        
        
ncat=len(categories)
for k1 in dirList: # loop over categories
    h1 = k1.ReadObj()
    nom=k1.GetName()
    h1.cd()
    histoList = gDirectory.GetListOfKeys()

    print "dir: %s DCP %s"%(nom,useDCP)
    
    if "bin5" in nom or "bin6" in nom or "bin7" in nom or "bin8" in nom or "bin9" in nom or "bin10" in nom or "bin11" in nom or "bin12" in nom:
        continue

    if channel=='em' and useDCP==0 and 'DCP' in nom:
        continue
    if channel=='em' and useDCP==1 and ('DCP' not in nom and '0jet' not in nom and 'boosted' not in nom):
        continue
    print " passing... "

    nom_new=nom
    nom_new=nom_new.replace('dijet','vbf')
    nom_new=nom_new.replace('_2016','')
    nom_new=nom_new.replace('_2017','')
    nom_new=nom_new.replace('_2018','')
    nom_new=nom_new.replace('_loosemjj_lowboost','_ggHMELA_bin1')
    nom_new=nom_new.replace('_loosemjj_boosted','_ggHMELA_bin2')
    nom_new=nom_new.replace('_loosemjj_boost','_ggHMELA_bin2')
    nom_new=nom_new.replace('_tightmjj_lowboost','_ggHMELA_bin3')
    nom_new=nom_new.replace('_tightmjj_boosted','_ggHMELA_bin4')
    nom_new=nom_new.replace('_tightmjj_boost','_ggHMELA_bin4')
    mydir=ofile.mkdir(nom_new)


    #mydir=ofile.mkdir(nom)
    #print "dir: ",nom

    N_histo=0
    print " dir: %s ..."%(nom)
    
    for histo in histoList:
        h2 = histo.ReadObj()
        h3=h2.Clone()
        h3.SetName(h2.GetName())
        #print "histo name: %s"%()

        if channel == 'em':
            if h3.GetName().find("Contamination_P") == 0 or h3.GetName().find("Contamination_M") == 0:
                continue
            # if h3.GetName().find("RecoilReso_njets") != -1:
            #     continue
            # if h3.GetName().find("RecoilResp") != -1:
            #     continue

        if ('vbf' in nom and channel=='em') or ('vbf_' in nom):

            bin_i=0

            if usePhiJJ:
                 binsNN=[50,80,100,115,130,150,200]
            if "bin1" in nom and mergeMSV==1:
                 binsNN=[50,80,100,115,150,200]

            if "data_obs" in h3.GetName():
                print " ===> final NN binning in %s is %s"%(nom,binsNN)
                print " ===> final D2jet binning in %s is %s"%(nom,binsD2jet)

                # now check that the output bin edges are present in input datacards
                binsXinput=[]
                binsYinput=[]
                for binX in range(1,h3.GetXaxis().GetNbins()+2):
                    binsXinput.append(h3.GetXaxis().GetBinLowEdge(binX))
                for binY in range(1,h3.GetYaxis().GetNbins()+2):
                    binsYinput.append(h3.GetYaxis().GetBinLowEdge(binY))
                print "\t INPUT datacard:  binsX: ", binsXinput, " binsY: ", binsYinput

                for binY in binsNN:
                    closestY=min(binsYinput, key=lambda x:abs(x-binY))
            #print "closest=%s"%(closestY)
                        #if binY not in binsYinput:
                    if abs(closestY-binY)>0.01:
                        print " ERROR Y bin %s not in input datacard ====>>> BREAK !!!!!!!!!!!!!!!! "%(binY)
                        exit(0)
                for binX in binsD2jet:
                    closestX=min(binsXinput, key=lambda x:abs(x-binX))
                    #print "closest=%s"%(closestX)
                    #if binX not in binsXinput:
                    if abs(closestX-binX)>0.01:
                        print " ERROR X bin %s not in input datacard ====>>> BREAK !!!!!!!!!!!!!!!! "%(binX)
                        exit(0)
                    

                #if "GGH2Jets_pseudoscalar_0Mf05" in h3.GetName():
                #       print " input histo: %s"%(h3.GetName())

            histo=ROOT.TH1F("histo",h3.GetName(),(len(binsNN)-1)*(len(binsD2jet)-1),0,(len(binsNN)-1)*(len(binsD2jet)-1))
            for binX in range(len(binsNN)-1):
                for binY in range(len(binsD2jet)-1):
                    bin_i=bin_i+1
                    #print "binX %s binY %s ==> %s"%(binX,binY,bin_i)
                    binNN_low=binsNN[binX]
                    binNN_high=binsNN[binX+1]
                    binD2jet_low=binsD2jet[binY]
                    binD2jet_high=binsD2jet[binY+1]
                    #if "data_obs" in h3.GetName():
                    #   print " bin %s: NN [%s,%s], D2jet [%s,%s]"%(bin,binNN_low,binNN_high,binD2jet_low,binD2jet_high)
                    # find these bins in input 2D plot:
                    binNN_low_i=h3.GetYaxis().FindBin(binNN_low)
                    binNN_high_i=h3.GetYaxis().FindBin(binNN_high)-1
                    binD2jet_low_i=h3.GetXaxis().FindBin(binD2jet_low)
                    binD2jet_high_i=h3.GetXaxis().FindBin(binD2jet_high)-1
                    error_merged = ROOT.Double()
                    yield_merged=h3.IntegralAndError(binD2jet_low_i,binD2jet_high_i,binNN_low_i,binNN_high_i,error_merged)

                    if ("ggH_htt_0Mf05ph0125" in h3.GetName()):
                        error_merged=error_merged*scaleGGH
                        yield_merged=yield_merged*scaleGGH
                    #print " %s %s scale by %s"%(nom,h3.GetName(),scaleGGH)
                    if ("HWW_a3" in h3.GetName() and "VBF" in h3.GetName()):
                        error_merged=error_merged*scaleHWWAC
                        yield_merged=yield_merged*scaleHWWAC
                        #print " %s %s scale by %s"%(nom,h3.GetName(),scaleGGH)

                    if ("ggH125" in h3.GetName()):
                        error_merged=error_merged*scaleAllGGH
                        yield_merged=yield_merged*scaleAllGGH

                    histo.SetBinContent(bin_i,yield_merged)
                    histo.SetBinError(bin_i,error_merged)
                    if "ZTT" in h3.GetName() and yield_merged==0:
                        histo.SetBinContent(bin_i,0.01)
                        histo.SetBinError(bin_i,0.03)

                        #if "ZTT" in h3.GetName() and "Up" not in h3.GetName() and "Down" not in h3.GetName():
                        #       print "   ===> [x],[y]: [%s,%s], [%s,%s] : [%s,%s], [%s,%s] = %s +- %s"%(binD2jet_low,binD2jet_high,binNN_low,binNN_high,binD2jet_low_i,binD2jet_high_i,binNN_low_i,binNN_high_i,yield_merged,error_merged)
                #name_histo=h3.GetName()
                '''    
            if ("ggH_htt_0Mf05ph0125" in h3.GetName()):
            print " this is %s and scale by %s"%(h3.GetName(),scaleGGH) 
                    histo.Scale(scaleGGH)      
                '''            
                #mydir=ofile.mkdir(nom)
            mydir.cd()
            name_histo=h3.GetName()
            if (channel=='em' and ("Up" in name_histo or "Down" in name_histo)):
                name_histo=name_histo.replace("M125","M125_")   
                name_histo=name_histo.replace("PH125","PH125_")
                name_histo=name_histo.replace("0125","0125_")
            name_histo=name_histo.replace("MES","muES")
            if (channel=='em' and "GG" in name_histo):
                name_histo=name_histo.replace("0Mf05","Mf05")


            name_histo=name_histo.replace("JHU__reweighted","reweighted")
            name_histo=name_histo.replace("JHU__unweighted","reweighted")

            if (channel=='em' and year!="_2016"):
                name_histo=name_histo.replace("MG__","")

            name_histo=name_histo.replace("_powheg","")
            name_histo=name_histo.replace("wh125","WH125")
            name_histo=name_histo.replace("zh125","ZH125")
            name_histo=name_histo.replace("vbf125","VBF125")
            name_histo=name_histo.replace("ggh125","ggH125")
            #name_histo=name_histo.replace("GGH2Jets_sm_M125","ggh_madgraph_twojet")
            #name_histo=name_histo.replace("GGH2Jets_pseudoscalar_M125","ggh_madgraph_PS_twojet")
            name_histo=name_histo.replace("GGH2Jets_sm_M125","reweighted_GGH2Jets_0PM125")
            name_histo=name_histo.replace("GGH2Jets_pseudoscalar_M125","reweighted_GGH2Jets_0M125")
            name_histo=name_histo.replace("GGH2Jets_pseudoscalar_Mf05ph0125","reweighted_GGH2Jets_Mf05ph0125")
            name_histo=name_histo.replace("_nominal","")

            #if (channel=='em' and year=="_2016" or channel=='et' or channel=='mt'):
            if (channel=='em' or channel=='et' or channel=='mt'):

                 name_histo=name_histo.replace("reweighted_ggH_htt_0PM125","reweighted_GGH2Jets_0PM125")
                 name_histo=name_histo.replace("reweighted_ggH_htt_0M125","reweighted_GGH2Jets_0M125")
                 name_histo=name_histo.replace("reweighted_ggH_htt_0Mf05ph0125","reweighted_GGH2Jets_Mf05ph0125")

            name_histo=rename_histo(name_histo)
                #print "  write: %s"%(name_histo)            

            if usePhiJJ:
                for bin_under in range(1,h3.GetNbinsX()+1):
                    histo.AddBinContent(0,h3.GetBinContent(bin_under,0))
                    histo.AddBinContent((len(binsNN)-1)*(len(binsD2jet)-1)+1,h3.GetBinContent(bin_under,h3.GetNbinsY()+1))
                
                #if "GGH2Jets_pseudoscalar_0Mf05" in h3.GetName():
                #    print "  =>>>>> write out as: %s"%(name_histo)

            histo.Write(name_histo)
            if usePhiJJ and channel=='em' and name_histo=='WH125':
                histo.Write('reweighted_WH_htt_0PM125')
                histo.Write('reweighted_WH_htt_0M125')
            if usePhiJJ and channel=='em' and name_histo=='ZH125':
                histo.Write('reweighted_ZH_htt_0PM125')
                histo.Write('reweighted_ZH_htt_0M125')
            if usePhiJJ and channel=='em' and name_histo=='reweighted_qqH_htt_0PM125':
                histo.Write('reweighted_qqH_htt_0M125')
                histo.Write('reweighted_qqH_htt_0Mf05ph0125')

            if name_histo.find("CMS_scale_emb_t_1prong") != -1 or name_histo.find("CMS_scale_emb_t_3prong") != -1:
                name_histo = name_histo.replace("_emb_t", "_t")
                histo.Write(name_histo)

            if channel == "em" and name_histo.find("embedded_muES") != -1:
                name_histo = name_histo.replace("muES", "muES_emb")
                histo.Write(name_histo)

            if channel == "mt" and name_histo.find("embedded_CMS_scale_m_eta") != -1:
                name_histo = name_histo.replace("CMS_scale_m_eta", "CMS_scale_emb_m_eta")
                histo.Write(name_histo)

            # if name_histo.find("CMS_singlemutrg_emb_") != -1:
            #     name_histo = name_histo.replace("CMS_singlemutrg_emb_", "CMS_singlemutrg_")
            #     histo.Write(name_histo)
            # elif name_histo.find("CMS_mutautrg_emb_") != -1:
            #     name_histo = name_histo.replace("CMS_mutautrg_emb_", "CMS_mutautrg_")
            #     histo.Write(name_histo)

            if name_histo.find("CMS_eff_t_embedded_") != -1:
                name_histo = name_histo.replace("CMS_eff_t_embedded_", "CMS_tauideff_")
                histo.Write(name_histo)


    #         # now add JHU vs Powheg diffrence as syst shape for VBF:
    #     if ("reweighted_qqH" in name_histo or "reweighted_WH" in name_histo or "reweighted_ZH" in name_histo )  and ("Up" not in name_histo and "Down" not in name_histo):
    #         value=0.
    # # for MELA bins:
    # '''
    #         if '_bin1' in nom:
    #                 value=0.17
    #         elif '_bin2' in nom:
    #                 value=0.06
    #         elif '_bin3' in nom:
    #                 value=-0.03
    #         elif '_bin4' in nom:
    #                 value=-0.08
    # '''
        
    #         # for D2jet bins:
    #         if '_bin1' in nom:
    #                 value=-0.1
    #         elif '_bin2' in nom:
    #                 value=-0.03
    #         elif '_bin3' in nom:
    #                 value=0.08
    #         elif '_bin4' in nom:
    #                 value=0.16

    #         # now make Up/Down:
    #         name_histo_Up=name_histo+"_JHUvsPowUp"
    #         name_histo_Down=name_histo+"_JHUvsPowDown"
    #         histo_Up=histo.Clone("")
    #         histo_Down=histo.Clone("")
    #         histo_Up.Scale(1+value)
    #         histo_Down.Scale(1-value)
    #         # histo_Up.Write(name_histo_Up)
    #         # histo_Down.Write(name_histo_Down)
    #         del histo_Up
    #         del histo_Down

                    
            
        #if "Up" not in name_histo and "Down" not in name_histo and h3.Integral()>0. and not ("ggH_htt_0Mf05ph0125" in h3.GetName() and scaleGGH!=1) and not ("ggH125" in h3.GetName() and scaleAllGGH!=1):
            #if "Up" not in name_histo and "Down" not in name_histo and h3.Integral()>0.  and "ggH_htt_0Mf05ph0125" not in h3.GetName():
            if "Up" not in name_histo and "Down" not in name_histo and h3.Integral()>0.  and "ggH" not in h3.GetName() and "mc_ZTT" not in h3.GetName() and "a3" not in h3.GetName():
        #print "checking merged yields... %s %s -> ratio %.2f"%(h3.Integral(),histo.Integral(),abs(h3.Integral()/histo.Integral()-1.))
                if abs(h3.Integral()/histo.Integral()-1.)>0.02:
                    print " WARNING INPUT and OUTPUT YIELDS DO NOT MATCH: input yield %s: %s output yield: %s"%(h3.GetName(),h3.Integral(),histo.Integral())
                    exit(0)
        else: # not VBF category
            #mydir=ofile.mkdir(nom)
            binXrange = range(1,h3.GetNbinsX()+1)
            binYrange = range(1,h3.GetNbinsY()+1)
            nUnrolledBins = h3.GetNbinsX()*h3.GetNbinsY()
            # # if channel == "mt" and "0jet" in nom:
            # if channel == "mt" and "0jet" in nom and year == "_2016":
            #     # binXrange = [3]
            #     # nUnrolledBins = (h3.GetNbinsY()-2)
            #     binYrange = range(1,h3.GetNbinsY()+1-2)
            #     nUnrolledBins = h3.GetNbinsX()*(h3.GetNbinsY()-2)
            histo=ROOT.TH1F("histo",h3.GetName(), nUnrolledBins,0,nUnrolledBins)

            bin_i=0
            for binX in binXrange:
                for binY in binYrange:
                # for binY in range(1,h3.GetNbinsY()+1):
                    bin_i=bin_i+1
                    # if h3.GetName() == "data_obs":
                    #     for ntimes in range(int(h3.GetBinContent(binX,binY))):
                    #         histo.Fill(bin_i-0.5)
                    #     if not histo.GetBinContent(bin_i) == h3.GetBinContent(binX,binY):
                    #         print("Wrong construction: {ori} vs {re}".format(ori=h3.GetBinContent(binX,binY),re=histo.GetBinContent(bin_i)))
                    #         exit(0) 
                    #     else:
                    #         print("Good matching")
                    # else:
                    
                    real_binY = binY
                    # # if channel == "mt" and "0jet" in nom:
                    # if channel == "mt" and "0jet" in nom and year == "_2016":
                    #     real_binY = binY + 2

                    histo.SetBinContent(bin_i,h3.GetBinContent(binX,real_binY))
                    histo.SetBinError(bin_i,h3.GetBinError(binX,real_binY))
                    # histo.SetBinContent(bin_i,h3.GetBinContent(binX,binY))
                    # histo.SetBinError(bin_i,h3.GetBinError(binX,binY))

            # if "0jet" in nom or "boosted" in nom:
            if "0jet" in nom:
                histo = h3.ProjectionY()
                
            mydir.cd()

            name_histo=h3.GetName()
            if (channel=='em' and ("Up" in name_histo or "Down" in name_histo)):
                name_histo=name_histo.replace("M125","M125_")                  
                name_histo=name_histo.replace("PH125","PH125_")
                name_histo=name_histo.replace("0125","0125_")

            name_histo=name_histo.replace("MES","muES")
            if (channel=='em' and "GG" in name_histo):
                name_histo=name_histo.replace("0Mf05","Mf05")

            name_histo=name_histo.replace("JHU__reweighted","reweighted")
            name_histo=name_histo.replace("JHU__unweighted","reweighted")

            if (channel=='em' and year!="_2016"):
                name_histo=name_histo.replace("MG__","")
            
            name_histo=name_histo.replace("_powheg","")
            name_histo=name_histo.replace("wh125","WH125")
            name_histo=name_histo.replace("zh125","ZH125")
            name_histo=name_histo.replace("vbf125","VBF125")
            name_histo=name_histo.replace("ggh125","ggH125")
            #name_histo=name_histo.replace("GGH2Jets_sm_M125","ggh_madgraph_twojet")
            #name_histo=name_histo.replace("GGH2Jets_pseudoscalar_M125","ggh_madgraph_PS_twojet")
            name_histo=name_histo.replace("GGH2Jets_sm_M125","reweighted_GGH2Jets_0PM125")
            name_histo=name_histo.replace("GGH2Jets_pseudoscalar_M125","reweighted_GGH2Jets_0M125")
            name_histo=name_histo.replace("GGH2Jets_pseudoscalar_Mf05ph0125","reweighted_GGH2Jets_Mf05ph0125")

            #if ((channel=='em' or channel=='et' or channel=='mt') and year=="_2016"):
            #if (channel=='em' and year=="_2016" or channel=='et' or channel=='mt'):
            if (channel=='em' or channel=='et' or channel=='mt'):

                 name_histo=name_histo.replace("reweighted_ggH_htt_0PM125","reweighted_GGH2Jets_0PM125")
                 name_histo=name_histo.replace("reweighted_ggH_htt_0M125","reweighted_GGH2Jets_0M125")
                 name_histo=name_histo.replace("reweighted_ggH_htt_0Mf05ph0125","reweighted_GGH2Jets_Mf05ph0125")

            name_histo=rename_histo(name_histo)
 

            histo.Write(name_histo)
            if usePhiJJ and channel=='em' and name_histo=='WH125':
                histo.Write('reweighted_WH_htt_0PM125')
                histo.Write('reweighted_WH_htt_0M125')
                histo.Write('reweighted_WH_htt_0Mf05ph0125')
            if usePhiJJ and channel=='em' and name_histo=='ZH125':
                histo.Write('reweighted_ZH_htt_0PM125')
                histo.Write('reweighted_ZH_htt_0M125')
                histo.Write('reweighted_ZH_htt_0Mf05ph0125')
            if usePhiJJ and channel=='em' and name_histo=='reweighted_qqH_htt_0PM125':
                histo.Write('reweighted_qqH_htt_0M125')
                histo.Write('reweighted_qqH_htt_0Mf05ph0125')

            if name_histo.find("CMS_scale_emb_t_1prong") != -1 or name_histo.find("CMS_scale_emb_t_3prong") != -1:
                name_histo = name_histo.replace("_emb_t", "_t")
                histo.Write(name_histo)

            if channel == "em" and name_histo.find("embedded_muES") != -1:
                name_histo = name_histo.replace("muES", "muES_emb")
                histo.Write(name_histo)
                
            if channel == "mt" and name_histo.find("embedded_CMS_scale_m_eta") != -1:
                name_histo = name_histo.replace("CMS_scale_m_eta", "CMS_scale_emb_m_eta")
                histo.Write(name_histo)
                
            # if name_histo.find("CMS_singlemutrg_emb_") != -1:
            #     name_histo = name_histo.replace("CMS_singlemutrg_emb_", "CMS_singlemutrg_")
            #     histo.Write(name_histo)
            # elif name_histo.find("CMS_mutautrg_emb_") != -1:
            #     name_histo = name_histo.replace("CMS_mutautrg_emb_", "CMS_mutautrg_")
            #     histo.Write(name_histo)

            if name_histo.find("CMS_eff_t_embedded_") != -1:
                name_histo = name_histo.replace("CMS_eff_t_embedded_", "CMS_tauideff_")
                histo.Write(name_histo)

            # if ("reweighted_qqH" in name_histo or "reweighted_WH" in name_histo or "reweighted_ZH" in name_histo ) and ("Up" not in name_histo and "Down" not in name_histo):
            #         value=0.
            #         # now make Up/Down:
            #         name_histo_Up=name_histo+"_JHUvsPowUp"
            #         name_histo_Down=name_histo+"_JHUvsPowDown"
            #         histo_Up=histo.Clone("")
            #         histo_Down=histo.Clone("")
            #         histo_Up.Scale(1+value)
            #         histo_Down.Scale(1-value)
            #         # histo_Up.Write(name_histo_Up)
            #         # histo_Down.Write(name_histo_Down)
            #         del histo_Up
            #         del histo_Down

            # #h3.Write(h3.GetName())

