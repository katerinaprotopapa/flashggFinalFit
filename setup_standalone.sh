# Setup script for standalone usage of flashggFinalFit
unset PYTHONPATH
export PYTHONNOUSERSITE=1
export CMSSW_BASE=$(dirname $(dirname $(pwd)))
export PYTHONPATH=$PYTHONPATH:${CMSSW_BASE}/src/flashggFinalFit/tools
export SCRAM_ARCH=None
