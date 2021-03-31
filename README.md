# CombineHarvester

Full documentation: http://cms-analysis.github.io/CombineHarvester

## Quick start

This pacakge requires HiggsAnalysis/CombinedLimit to be in your local CMSSW area. We follow the release recommendations of the combine developers which can be found [here](https://cms-hcomb.gitbooks.io/combine/content/part1/#for-end-users-that-dont-need-to-commit-or-do-any-development). The CombineHarvester framework is  compatible with the CMSSW 7_4_X and 8_1_X series releases.

A new full release area can be set up and compiled in the following steps:

    cmsrel CMSSW_8_1_0
    cd CMSSW_8_1_0/src
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    cd HiggsAnalysis/CombinedLimit
    git fetch origin
    git checkout v8.1.0
    cd ../..
    cp /hdfs/store/user/senka/HTT_2016and2017/signalModels/* HiggsAnalysis/CombinedLimit/python/
    git clone -b lt_chn ssh://git@gitlab.cern.ch:7999/KState-HEP-HTT/CombineHarvester.git CombineHarvester
    scram b

Setup CMSSW_9_4_4 elsewhere (nothing but cmsrel)

    cmsrel CMSSW_9_4_4

run_first_scans_fa3_ggH.sh is a script to make datacards for fa3 ggH. In the script, you need to replace --path_datacard and --path_CMSSW94 with your own datacard path and CMSSW_9_4_4 path in the previous step.

    source run_first_scans_fa3_ggH.sh

Scan fa3 ggH em 2018 (for obs, just add -t -1 for exp)

    combine -M MultiDimFit fa3_ggH_em_2018.root -n _scan_obs_fa3_ggH_em_2018 -m 125 --algo=grid --alignEdges 1 --points=101 -P fa3_ggH --floatOtherPOIs=1 --setParameterRanges muV=0,4:muf=0,10:fa3_ggH=-1,1:CMS_zz4l_fai1=-1,1 --setParameters muV=1,muf=1,fa3_ggH=0,CMS_zz4l_fai1=0 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo "Minuit2,0:1." -v 3
