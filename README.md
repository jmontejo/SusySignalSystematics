# SusySignalSystematics

Parameterization of SUSY signal systematics independently of the decay. The main impa

# Derive systematics
python script that extracts the variations out of a sample. The variations are stored as histograms of sparticle-sparticle pT, as a function of (process, mass)

# Apply systematics
C++ functions within SUSYTools/Root/Truth.cxx where the user gives (process, mass) + desired systematic and it returns the weight
The function will also ret

# Apply systematics
Second script that returns those variations, interpolated over mass if needed
