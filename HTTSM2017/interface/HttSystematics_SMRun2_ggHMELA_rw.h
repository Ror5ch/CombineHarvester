#ifndef SM2016_HttSystematics_SMRun2_ggHMELA_rw_h
#define SM2016_HttSystematics_SMRun2_ggHMELA_rw_h
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"

namespace ch {
// Run2 SM analysis systematics
// Implemented in src/HttSystematics_SMRun2.cc
  void AddSMRun2Systematics_ggHMELA_rw(CombineHarvester& cb, int tt_cate_count=3, int mt_cate_count=3, int control_region = 0, bool do_shapeSyst=false, int year=-999, bool zmm_fit = false, bool ttbar_fit = false);
}

#endif
