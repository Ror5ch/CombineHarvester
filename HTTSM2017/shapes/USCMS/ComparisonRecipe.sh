#!/bin/sh 
#########################################################################################
##   usage : source ComparisonRecipe.sh inputfile foldername channel tag -s(or empty)  ##
##           source ComparisonRecipe.sh final_nomianl.root TestOct19 tt mjj            ##
##           source ComparisonRecipe.sh htt_input.root TestOct19 tt mjj --svn          ##
#########################################################################################

# Unrolling
if [ -z ${5} ]; then
    python Unroll_2Drelaxed.py ${1} ${3} 
else
    python Unroll_2Drelaxed.py ${1} ${3} ${5}
fi

# now prepare to run the limits:
cd $CMSSW_BASE/src/CombineHarvester/HTTSM2017/bin
MorphingSM2017 --output_folder=${2} --postfix="-2D" --control_region=0 --manual_rebin=false --real_data=false --mm_fit=false --ttbar_fit=false
# add MC stat uncertainties:                                                                                                                                   
sh _do_mc_Stat.sh  output/${2}
cd output/${2}
combineTool.py -M T2W -i {cmb,${3}}/* -o workspace.root --parallel 18
cp ../../../scripts/texName.json .
cp ../../../scripts/plot1DScan.py .


# Run on mjj and save outputs with name "*_title"
combine -M MultiDimFit -m 125 --algo grid --points 101 --rMin 0 --rMax 2 cmb/125/workspace.root -n nominal_${4} -t -1 --expectSignal=1

