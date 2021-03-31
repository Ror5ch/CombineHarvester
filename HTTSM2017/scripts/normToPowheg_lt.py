#!/usr/bin/env python
import ROOT
from ROOT import *
import re
from array import array

import operator
import sys
filename_1 = sys.argv[1]
filename_out = sys.argv[2]
chn = sys.argv[3]


islog=1
unrollSV=1

ifile=ROOT.TFile(filename_1,"r")
ofile=ROOT.TFile(filename_out,"recreate")

ifile.cd()
dirList = gDirectory.GetListOfKeys()

name_SM_qqH_powheg="VBF125"
name_SM_qqH_JHU="reweighted_qqH_htt_0PM125"

name_SM_WH_powheg="WH125"
name_SM_WH_JHU="reweighted_WH_htt_0PM125"

name_SM_ZH_powheg="ZH125"
name_SM_ZH_JHU="reweighted_ZH_htt_0PM125"

name_SM_ggH_powheg="ggH125"
name_SM_ggH_JHU="ggh_madgraph_twojet"
name_SM_ggH_boost='ggh_madgraph'

yield_qqH_Powheg = ifile.Get(chn+'_vbf').Get(name_SM_qqH_powheg).Integral()
yield_qqH_JHU = ifile.Get(chn+'_vbf').Get(name_SM_qqH_JHU).Integral()
yield_WH_Powheg = ifile.Get(chn+'_vbf').Get(name_SM_WH_powheg).Integral()
yield_WH_JHU = ifile.Get(chn+'_vbf').Get(name_SM_WH_JHU).Integral()
yield_ZH_Powheg = ifile.Get(chn+'_vbf').Get(name_SM_ZH_powheg).Integral()
yield_ZH_JHU = ifile.Get(chn+'_vbf').Get(name_SM_ZH_JHU).Integral()
yield_ggH_Powheg = ifile.Get(chn+'_vbf').Get(name_SM_ggH_powheg).Integral()
yield_ggH_JHU = ifile.Get(chn+'_vbf').Get(name_SM_ggH_JHU).Integral()
yield_ggH_boost_JHU = ifile.Get(chn+'_boosted').Get(name_SM_ggH_boost).Integral()
yield_ggH_boost_Powheg = ifile.Get(chn+'_boosted').Get(name_SM_ggH_powheg).Integral()

for key in dirList:
    idir = key.ReadObj() 
    name = idir.GetName()

    if 'plots' in name:
      continue

    ofile.mkdir(name)
    
    idir.cd()
    histoList = gDirectory.GetListOfKeys()
    name_last = ""
    
    ifile.cd(name)
    if (yield_qqH_JHU > 0):
        scale_to_Powheg_qqH = yield_qqH_Powheg / yield_qqH_JHU
    if (yield_WH_JHU > 0):
        scale_to_Powheg_WH = yield_WH_Powheg / yield_WH_JHU
    if (yield_ZH_JHU > 0):
        scale_to_Powheg_ZH = yield_ZH_Powheg / yield_ZH_JHU
    if (yield_ggH_JHU > 0):
        scale_to_Powheg_ggH = yield_ggH_Powheg / yield_ggH_JHU
    if (yield_ggH_boost_JHU > 0):
        scale_to_Powheg_ggH_boost = yield_ggH_boost_Powheg / yield_ggH_boost_JHU

    for ihist_name in histoList:
        ihist = ihist_name.ReadObj()
        scaled = ihist.Clone()
        scaled.SetName(ihist.GetName())
        if "WH_htt_0" in scaled.GetName() and scaled.Integral()>0.:
            scaled.Scale(scale_to_Powheg_WH)
        elif "ZH_htt_0" in scaled.GetName() and scaled.Integral()>0.:
            scaled.Scale(scale_to_Powheg_ZH)
        elif "ggh_madgraph_twojet" in scaled.GetName() and scaled.Integral()>0.:
            scaled.Scale(scale_to_Powheg_ggH)
        elif "ggh_madgraph" in scaled.GetName() and scaled.Integral()>0.:
            scaled.Scale(scale_to_Powheg_ggH_boost)                  
        elif "qqH_htt_" in scaled.GetName() and scaled.Integral()>0.:
            scaled.Scale(scale_to_Powheg_qqH)

        ofile.cd(name)

        if 'ggH125' in scaled.GetName() and '0jet' in name:
            name_histo=scaled.GetName().replace("ggH125","GGH2Jets_sm_M125")
            name_histo_PS=scaled.GetName().replace("ggH125","GGH2Jets_pseudoscalar_M125")
            name_histo_maxmix=scaled.GetName().replace("ggH125","GGH2Jets_pseudoscalar_Mf05ph0125")

            # 0jet, boosted, vbf use powheg ggH
            scaled.Write()
            sm = scaled.Clone()
            sm.SetName(name_histo)
            ps = scaled.Clone()
            ps.SetName(name_histo_PS)
            inter = scaled.Clone()
            inter.SetName(name_histo_maxmix)
            sm.Write()
            ps.Write()
            inter.Write()
        elif scaled.GetName() == 'ggh_madgraph' and 'boosted' in name:
            name_histo=scaled.GetName().replace("ggh_madgraph","GGH2Jets_sm_M125")
            name_histo_PS=scaled.GetName().replace("ggh_madgraph","GGH2Jets_pseudoscalar_M125")
            name_histo_maxmix=scaled.GetName().replace("ggh_madgraph","GGH2Jets_pseudoscalar_Mf05ph0125")

            # 0jet, boosted, vbf use powheg ggH
            scaled.Write()
            sm = scaled.Clone()
            sm.SetName(name_histo)
            ps = scaled.Clone()
            ps.SetName(name_histo_PS)
            inter = scaled.Clone()
            inter.SetName(name_histo_maxmix)
            sm.Write()
            ps.Write()
            inter.Write()

        elif 'JHU' in scaled.GetName():
            continue

        elif 'ggh_madgraph' in scaled.GetName() and 'twojet' in scaled.GetName() and 'vbf' in name:
            if 'ggh_madgraph_Maxmix_twojet' in scaled.GetName():
                scaled.SetName(scaled.GetName().replace("ggh_madgraph_Maxmix_twojet","GGH2Jets_pseudoscalar_Mf05ph0125"))
            elif 'ggh_madgraph_PS_twojet' in scaled.GetName():
                scaled.SetName(scaled.GetName().replace("ggh_madgraph_PS_twojet","GGH2Jets_pseudoscalar_M125"))
            elif 'ggh_madgraph_twojet' in scaled.GetName():
                scaled.SetName(scaled.GetName().replace("ggh_madgraph_twojet","GGH2Jets_sm_M125"))

            ihist.Write()
            scaled.Write()
        
        else:
            scaled.Write()

    idir.Close()

