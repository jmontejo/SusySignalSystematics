import ROOT
import sys
import glob
from SWup.coolPlot import coolPlot
ROOT.gROOT.LoadMacro("calc_pt.C++")
ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

do1L = True
quick = False

if do1L: folder = "/eos/user/j/jmontejo/ntuples_wollrath/"
else:    folder = "/eos/atlas/atlascerngroupdisk/phys-susy/tt0L_ANA-SUSY-2018-12/TruthStudies/"

samples = glob.glob(folder+"*")

masses = [225,500,800,1100]
systs = ["qcdw","qcup","scdw","scup","Var3cdw","Var3cup"]
infile  = ROOT.TFile.Open("hpt.root")



for mass in masses:
  hists = {}
  hname = "hpt_stop1L_%s_%s"%(mass,"nominal")
  hnom = infile.Get(hname)
  hists["nominal"] = hnom
  hnom.Write()
  for syst in systs:
    if "dw" in syst: continue
    hname = "hpt_stop1L_%s_%s"%(mass,syst)
    hup = infile.Get(hname)
    hdw = infile.Get(hname.replace("up","dw"))
    hdiff = hup.Clone(hname+"diff")
    hdiff2 = hup.Clone(hname+"diff2")
    hdiff.Add(hdw,-1.)
    hdiff.Scale(0.5)
    hdiff.Add(hnom)
    hdiff2.Add(hdw,-1.)
    hdiff2.Scale(-0.5)
    hdiff2.Add(hnom)
    hists[syst] = hdiff
    hists[syst.replace("up","dw")] = hdiff2
    hdiff.Write(hname)
    hdiff2.Write(hname.replace("up","dw"))
  
  name = "stop_syst1L_%s"%(mass)
  coolPlot(name ,[hists[s] for s in ["nominal"]+systs],formats=("png","pdf","C","root"), titlelist = ["nominal"]+[s for s in systs])
