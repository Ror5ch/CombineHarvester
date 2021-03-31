if [ ! -d "HTTAC2017/shapes/USCMS/" ]
then
    mkdir -p HTTAC2017/shapes/USCMS/
fi

# new SF datacard with and w shape syst em ggH fa3:
python run_optimizedBin_limits.py --chn=em --year=2018 --emb=1 --inputString=MANUAL_optBins_fa3_ggHint_AutoRebin_swaped_newFSA_HWWSMPowheg_Syst --useDCP=1 --par=fa3 --path_datacard=/data6/Users/knam/13TeV/HTTAC/emu_dec02 --name_datacard=em_2D_htt_em_emb_sys_ggh_2018_Dec02.root --path_CMSSW94=/home/knam/HTTAC/CMSSW_9_4_4 --isGGH=1 --use_ggHint=1 --useShapeSyst=1 --symDCP=1 --use_ggHphase=1
source commands_em_2018_isGGH1_MANUAL_optBins_fa3_ggHint_AutoRebin_swaped_newFSA_HWWSMPowheg_Syst_fa3.txt
# python run_optimizedBin_limits.py --chn=em --year=2017 --emb=1 --inputString=MANUAL_optBins_fa3_ggHint_AutoRebin_swaped_newFSA_HWWSMPowheg_Syst --useDCP=1 --par=fa3 --path_datacard=/data6/Users/knam/13TeV/HTTAC/emu_dec02 --name_datacard=em_2D_htt_em_emb_sys_ggh_2017_Dec02.root --path_CMSSW94=/home/knam/HTTAC/CMSSW_9_4_4 --isGGH=1 --use_ggHint=1 --useShapeSyst=1 --symDCP=1 --use_ggHphase=1
# source commands_em_2017_isGGH1_MANUAL_optBins_fa3_ggHint_AutoRebin_swaped_newFSA_HWWSMPowheg_Syst_fa3.txt
# python run_optimizedBin_limits.py --chn=em --year=2016 --emb=1 --inputString=MANUAL_optBins_fa3_ggHint_AutoRebin_swaped_newFSA_HWWSMPowheg_Syst --useDCP=1 --par=fa3 --path_datacard=/data6/Users/knam/13TeV/HTTAC/emu_dec02 --name_datacard=em_2D_htt_em_emb_sys_ggh_2016_Dec02.root --path_CMSSW94=/home/knam/HTTAC/CMSSW_9_4_4 --isGGH=1 --use_ggHint=1 --useShapeSyst=1 --symDCP=1 --use_ggHphase=1
# source commands_em_2016_isGGH1_MANUAL_optBins_fa3_ggHint_AutoRebin_swaped_newFSA_HWWSMPowheg_Syst_fa3.txt

