#!/usr/bin/env python
import ROOT
from ROOT import *
import re
from array import array
from optparse import OptionParser

import numpy as np

import operator
import sys
filename_1 = sys.argv[1]
filename_out = sys.argv[2]
chn = sys.argv[3]

parser = OptionParser()
parser.add_option('--dostat', '-s', action='store',
                  default="0", dest='doStat',
                  help='doStat Up/Down for signal ggH SM and PS with setting to 1/2'
                  )
(options, args) = parser.parse_args()

doStat=int(options.doStat)



islog=1
unrollSV=1


file=ROOT.TFile(filename_1,"r")
file1=ROOT.TFile(filename_out,"recreate")

file.cd()
dirList = gDirectory.GetListOfKeys()

# define names of histograms that will be tossed!
histo_toss_SM="reweighted_qqH_htt_0PM125"
histo_toss_BSM="reweighted_qqH_htt_0M125"

if chn=='mt' or chn=='et':
    histo_toss_SM="ggh_madgraph_twojet"
    histo_toss_BSM="ggh_madgraph_PS_twojet"


for k1 in dirList:
    print "\n signal DCP_minus: ", k1.GetName()
    h1 = k1.ReadObj()
    nom=k1.GetName()
    nom_out=nom

    file1.mkdir(nom_out)
    
    h1.cd()
    histoList = gDirectory.GetListOfKeys()
    name_last=""

    h_SM_ggH_JHU_c=h1.Get(histo_toss_SM)
    h_SM_ggH_JHU=h_SM_ggH_JHU_c.Clone()

    h_PS_ggH_JHU_c=h1.Get(histo_toss_BSM)
    h_PS_ggH_JHU=h_PS_ggH_JHU_c.Clone()

    file.cd(nom)

    for k2 in histoList:
        if (k2.GetName()!=name_last):
            h2 = k2.ReadObj()
            h3=h2.Clone()
            h3.SetName(k2.GetName())
            nom=k1.GetName()
            dir_m_name=nom

            file1.cd(nom_out)

            name_histo=h3.GetName()
            #name_histo=name_histo.replace("JetFakes","jetFakes")
            name_last=h3.GetName()
            #print "\n histo name %s "%(name_last)

            # if this is SM or PS then toss toys
            #if name_histo==histo_toss_SM or name_histo==histo_toss_BSM:
            if ((name_histo==histo_toss_SM or name_histo==histo_toss_BSM)):

                for i_x in range(1,h3.GetNbinsX()+1):
                    for i_y in range(1,h3.GetNbinsY()+1):
                        #print " bin %s %s"%(i_x, i_y)
			# get bin content (mu) and uncertainty (sigma) and toss by Gaussian
                        mu, sigma = h3.GetBinContent(i_x,i_y), h3.GetBinError(i_x,i_y)
                        s = np.random.normal(mu, sigma, 1)
                        #print " mu=%s, sigma=%s => s= %s"%(mu,sigma,s)
                        #print "  tossing ..."
                        h3.SetBinContent(i_x,i_y,s)
                        h3.SetBinError(i_x,i_y,sigma)

            h3.SetName(name_histo)
            h3.Write(name_histo)
    h1.Close()
