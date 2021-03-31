#!/usr/bin/env python
import sys
import ROOT
import copy
from optparse import OptionParser

inputfile = sys.argv[1]
channel = sys.argv[2]

parser = OptionParser()
parser.add_option('--svn', '-s', action='store_true',
                  default=False, dest='is_SVN',
                  help='input is SVN datacard'
                  )
parser.add_option('--ztt', '-z', action='store_true',
                  default=False, dest='is_zttMC',
                  help='run on embedded or MC ZTT'
                  )
(options, args) = parser.parse_args()

file = ROOT.TFile(inputfile,'r')
file1D = ROOT.TFile('htt_'+channel+'.inputs-sm-13TeV-2D.root', 'recreate')

categories = [
    channel+'_0jet', channel+'_boosted', channel+'_vbf', 
    channel+'_vbf_ggHMELA_bin1_NN_bin1'  , channel+'_vbf_ggHMELA_bin2_NN_bin1'  , channel+'_vbf_ggHMELA_bin3_NN_bin1'  ,
    channel+'_vbf_ggHMELA_bin4_NN_bin1'  , channel+'_vbf_ggHMELA_bin5_NN_bin1'  , channel+'_vbf_ggHMELA_bin6_NN_bin1'  ,
    # channel+'_vbf_ggHMELA_bin7_NN_bin1'  , channel+'_vbf_ggHMELA_bin8_NN_bin1'  , channel+'_vbf_ggHMELA_bin9_NN_bin1'  ,
    # channel+'_vbf_ggHMELA_bin10_NN_bin1' , channel+'_vbf_ggHMELA_bin11_NN_bin1' , channel+'_vbf_ggHMELA_bin12_NN_bin1' ,
    channel+'_vbf_ggHMELA_bin1_NN_bin2' , channel+'_vbf_ggHMELA_bin2_NN_bin2' , channel+'_vbf_ggHMELA_bin3_NN_bin2' ,
    channel+'_vbf_ggHMELA_bin4_NN_bin2' , channel+'_vbf_ggHMELA_bin5_NN_bin2' , channel+'_vbf_ggHMELA_bin6_NN_bin2' ,
    # channel+'_vbf_ggHMELA_bin7_NN_bin2' , channel+'_vbf_ggHMELA_bin8_NN_bin2' , channel+'_vbf_ggHMELA_bin9_NN_bin2' ,
    # channel+'_vbf_ggHMELA_bin10_NN_bin2', channel+'_vbf_ggHMELA_bin11_NN_bin2',  channel+'_vbf_ggHMELA_bin12_NN_bin2',
    # channel+'_vbf_ggHMELA_bin1_NN_bin3', channel+'_vbf_ggHMELA_bin2_NN_bin3', channel+'_vbf_ggHMELA_bin3_NN_bin3',
    # channel+'_vbf_ggHMELA_bin4_NN_bin3', channel+'_vbf_ggHMELA_bin5_NN_bin3', channel+'_vbf_ggHMELA_bin6_NN_bin3',
    # channel+'_vbf_ggHMELA_bin7_NN_bin3', channel+'_vbf_ggHMELA_bin8_NN_bin3', channel+'_vbf_ggHMELA_bin9_NN_bin3',
    # channel+'_vbf_ggHMELA_bin10_NN_bin3', channel+'_vbf_ggHMELA_bin11_NN_bin3',  channel+'_vbf_ggHMELA_bin12_NN_bin3',
] # input dir names
dir_names = copy.deepcopy(categories)

processes = [
    'data_obs', 'embedded', 'mc_ZTT', 'VVT', 'W', 'ZL', 'ZJ', 'TTT', 'TTJ', 'VVJ', 'ggH125', 'VBF125',
    'WH125', 'ZH125', 'jetFakes', 'EWKZ', 'reweighted_qqH_htt_0L1125', 'reweighted_qqH_htt_0L1Zg125',
    'reweighted_qqH_htt_0M125', 'reweighted_qqH_htt_0PM125', 'reweighted_qqH_htt_0PH125', 'reweighted_qqH_htt_0L1f05ph0125',
    'reweighted_qqH_htt_0L1Zgf05ph0125', 'reweighted_qqH_htt_0Mf05ph0125', 'reweighted_qqH_htt_0PHf05ph0125',
    'reweighted_WH_htt_0L1125', 'reweighted_WH_htt_0L1Zg125', 'reweighted_WH_htt_0M125', 'reweighted_WH_htt_0PM125',
    'reweighted_WH_htt_0PH125', 'reweighted_WH_htt_0L1f05ph0125', 'reweighted_WH_htt_0L1Zgf05ph0125', 'reweighted_WH_htt_0Mf05ph0125',
    'reweighted_WH_htt_0PHf05ph0125', 'reweighted_ZH_htt_0L1125', 'reweighted_ZH_htt_0L1Zg125', 'reweighted_ZH_htt_0M125',
    'reweighted_ZH_htt_0PM125', 'reweighted_ZH_htt_0PH125', 'reweighted_ZH_htt_0L1f05ph0125', 'reweighted_ZH_htt_0L1Zgf05ph0125',
    'reweighted_ZH_htt_0Mf05ph0125', 'reweighted_ZH_htt_0PHf05ph0125', 'GGH2Jets_sm_M125', 'GGH2Jets_pseudoscalar_M125', 
    'GGH2Jets_pseudoscalar_Mf05ph0125'
] # input histos

if options.is_SVN:
    categories = ['htt_'+channel+'_1_13TeV', 'htt_'+channel+'_2_13TeV', 'htt_'+channel+'_3_13TeV']
    processes = [
        'data_obs', 'ZTT', 'W', 'QCD', 'ZL', 'ZJ', 'TTT', 'TTJ', 'VV', 
        'EWKZ', 'ggH_htt125', 'qqH_htt125', 'WH_htt125', 'ZH_htt125'
    ] # input histos    

if options.is_zttMC:
    del processes[:]
    processes = [
        'data_obs', 'ZTT', 'jetFakes', 'ZL', 'TTT', 
        'VVT', 'EWKZ', 'ggH125', 'VBF125', 'WH125', 'ZH125'
    ] # input histos    

systematics = [ # systematics
    '_CMS_htt_dyShape_13TeV',
    '_CMS_htt_jetToTauFake_13TeV',
    '_CMS_htt_ttbarShape_13TeV',
    '_CMS_scale_t_13TeV',
    '_CMS_scale_t_1prong_13TeV',
    '_CMS_scale_t_1prong1pizero_13TeV',
    '_CMS_scale_t_3prong_13TeV',
    '_CMS_scale_met_unclustered_13TeV',
    '_CMS_scale_met_clustered_13TeV',
    '_CMS_scale_j_13TeV',
    '_CMS_htt_zmumuShape_VBF_13TeV'
    ]
systematics = [] # overwrite with empty for now

ncat = len(categories)
print 'ncat={}'.format(ncat)

for i in range (0,ncat): # loop over categories
    if channel == 'tt':
        categories[i] = categories[i].replace('0p0', '0')
        categories[i] = categories[i].replace('1p0', '1')

    mydir=file1D.mkdir(dir_names[i])

    print '=================>>>  category: ', categories[i]
    N_histo = 0
    binsX_N = 0
    binsY_N = 0
    binsX_low = 0
    binsY_low = 0
    binsX_high = 0
    binsY_high = 0

    binsX_N_first = 0
    binsY_N_first = 0
    binsX_low_first = 0
    binsY_low_first = 0
    binsX_high_first = 0
    binsY_high_first = 0

    for i_histo in processes: # loop over input histos (processes)
        print ' histo: ', i_histo
        N_histo=N_histo+1
            
        histo2D=file.Get(categories[i]).Get(i_histo)

        if N_histo==1:
            binsX_N_first=histo2D.GetNbinsX()
            binsY_N_first=histo2D.GetNbinsY()
            binsX_low_first=histo2D.GetXaxis().GetBinLowEdge(1)
            binsX_high_first=histo2D.GetXaxis().GetBinLowEdge(binsX_N_first+1)
            binsY_low_first=histo2D.GetYaxis().GetBinLowEdge(1)
            binsY_high_first=histo2D.GetYaxis().GetBinLowEdge(binsX_N_first+1)

        binsX_N=histo2D.GetNbinsX()
        binsY_N=histo2D.GetNbinsY()
        binsX_low=histo2D.GetXaxis().GetBinLowEdge(1)
        binsX_high=histo2D.GetXaxis().GetBinLowEdge(binsX_N+1)
        binsY_low=histo2D.GetYaxis().GetBinLowEdge(1)
        binsY_high=histo2D.GetYaxis().GetBinLowEdge(binsX_N+1)

        if binsX_N_first!=binsX_N or binsY_N_first!=binsY_N or binsX_low_first!=binsX_low or binsX_high_first!=binsX_high or binsY_low_first!=binsY_low or binsY_high_first!=binsY_high:
            print ' ###########################   WARNING! different binning: X bins %s %s, Y bins %s %s, X low %s %s, Y low %s %s   '%(binsX_N_first, binsX_N, binsY_N_first, binsY_N, binsX_low_first, binsX_low,binsY_low_first, binsY_low )

        nx=histo2D.GetXaxis().GetNbins()
        ny=histo2D.GetYaxis().GetNbins()
        histo=ROOT.TH1F('histo',histo2D.GetName(),nx*ny,0,nx*ny)
        histo.SetName(histo2D.GetName())    
        if options.is_SVN:
            if histo2D.GetName()=='ggH_htt125':
                histo.SetName('ggH125')
            if histo2D.GetName()=='qqH_htt125':
                histo.SetName('VBF125')
            if histo2D.GetName()=='WH_htt125':
                histo.SetName('WH125')
            if histo2D.GetName()=='ZH_htt125':
                histo.SetName('ZH125')
            if histo2D.GetName()=='ZTT':
                histo.SetName('embedded')

        #print ' in histo: ',histo2D.GetName(), 
        l=0
        for j in range(1,nx+1):
            for k in range(1,ny+1):
	        l=l+1
                n = histo2D.GetBin(j,k);
                cont = histo2D.GetBinContent(n)
                err = histo2D.GetBinError(n)
                #histo.SetBinContent(l, cont)
                if cont < 0:
                  histo.SetBinContent(l, 0.0000000001)
                else:
                  histo.SetBinContent(l, cont)
                histo.SetBinError(l, err)
        mydir.cd()
        histo.Write()

        for systematic in systematics : # loop over available systematics
            if file.Get(categories[i]).Get(i_histo+systematic+'Down') != None:
                print i_histo+systematic+'Down/Up'
                histo2D_d=file.Get(categories[i]).Get(i_histo+systematic+'Down') #
                histo2D_u=file.Get(categories[i]).Get(i_histo+systematic+'Up') #
                histo_d=ROOT.TH1F('histo_d',histo2D_d.GetName(),nx*ny,0,nx*ny) #
                histo_u=ROOT.TH1F('histo_u',histo2D_u.GetName(),nx*ny,0,nx*ny) #
                histo_d.SetName(histo2D_d.GetName()) #
                histo_u.SetName(histo2D_u.GetName()) #
                l=0
                for j in range(1,nx+1):
                    for k in range(1,ny+1):
                        l=l+1
                        n = histo2D.GetBin(j,k);
                        cont_u = histo2D_u.GetBinContent(n)
                        cont_u = histo2D_u.GetBinContent(n)
                        if cont_u < 0:
                          histo_u.SetBinContent(l, 0.0000000001) #
                        if cont_d < 0:
                          histo_d.SetBinContent(l, 0.0000000001) #
                        if cont_u > 0 and cont_d > 0:
                          histo_u.SetBinContent(l,histo2D_u.GetBinContent(n)) #
                          histo_d.SetBinContent(l,histo2D_d.GetBinContent(n)) #
                        histo_u.SetBinError(l,histo2D_u.GetBinError(n)) #
                        histo_d.SetBinError(l,histo2D_d.GetBinError(n)) #
                histo_u.Write() #
                histo_d.Write() #           
            #else :
            #    print i_histo+systematic+'Down/Up fail'

# now make nice unrolled plots:
