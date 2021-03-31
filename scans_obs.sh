#!/bin/bash

channel=${1}

ulimit -s unlimited

combineTool.py -n 1D_scan_obs_fa3_${channel}_2016  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-0.1,0.1 ${channel}/125/fa03_Workspace_MengsMuV_${channel}_2016.root --algo=grid --points=101 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo "Minuit2,0:1." --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.
combineTool.py -n 1D_scan_obs_fa3_${channel}_2017  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-0.1,0.1 ${channel}/125/fa03_Workspace_MengsMuV_${channel}_2017.root --algo=grid --points=101 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo "Minuit2,0:1." --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.
combineTool.py -n 1D_scan_obs_fa3_${channel}_2018  -M MultiDimFit -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-0.1,0.1 ${channel}/125/fa03_Workspace_MengsMuV_${channel}_2018.root --algo=grid --points=101 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad -P CMS_zz4l_fai1 --floatOtherPOIs=1 --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --cminFallbackAlgo "Minuit2,0:1." --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.
