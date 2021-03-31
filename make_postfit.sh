combine -M FitDiagnostics output/data_MANUAL_$3_MELAVBF/$1/125/fa03_Workspace_MengsMuV_$1_$2.root  -m 125 --setParameterRanges muV=0.0,4.0:muf=0.0,10.0:fa3_ggH=0.,1.:CMS_zz4l_fai1=-0.01,0.01 --robustFit=1 --setRobustFitAlgo=Minuit2,Migrad --X-rtd FITTER_NEW_CROSSING_ALGO --setRobustFitTolerance=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --setParameters muV=1.,CMS_zz4l_fai1=0.,muf=1.,fa3_ggH=0.  -t -1 --expectSignal=1 -v 9
PostFitShapesFromWorkspace -o output_shapes_f$4_$1_$2.root -m 125 -f fitDiagnostics.root:fit_s --postfit --sampling --print -d output/data_MANUAL_$3_MELAVBF/$1/125/combined_$1_$2.txt.cmb -w output/data_MANUAL_$3_MELAVBF/$1/125/fa03_Workspace_MengsMuV_$1_$2.root
cp output/data_MANUAL_$3_MELAVBF/$1/common/htt_input_$2.root htt_input_f$4_$1_$2.root

