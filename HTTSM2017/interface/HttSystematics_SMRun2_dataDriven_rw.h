#ifndef SM2016_HttSystematics_SMRun2_dataDriven_rw_h
#define SM2016_HttSystematics_SMRun2_dataDriven_rw_h
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"

namespace ch {
// Run2 SM analysis systematics
// Implemented in src/HttSystematics_SMRun2.cc
void AddSMRun2Systematics_dataDriven_rw(CombineHarvester& cb, int control_region = 0, bool zmm_fit = false, bool ttbar_fit = false);
}

#endif
