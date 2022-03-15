#!/usr/bin/env python 

import argparse
import sys
import glob

production_modes = ["GG","TT","BB","C1N1","C2N1","N1N2","C1N2N1"]

def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--production-mode", choices=production_modes, help="Production mode. Default is to guess from the sample name")
    parser.add_argument("--input",     help="Input folder with all the samples")
    parser.add_argument("--pattern",   help="Process only files that contain this pattern")
    parser.add_argument("--output", default="systematics.root",  help="Output root file to contain the systematics")
    parser.add_argument("--recreate", action="store_true", help="Recreate the output file if it exists. Default is to update")
    parser.add_argument("--mass-position", type=int, help="Position where the mass of the sparticle appears after splitting by '_'. Default is to guess from the sample name")
    parser.add_argument("--all-files-in-folder", action="store_true", help="All root files are in one folder. Default assumes there is one folder per sample")
    parser.add_argument("--binning", default="10,0,1000",  help="Binning for the pT spectrum, defined as a comma separated list. Default '10,0,1000'")
    parser.add_argument("--bsm-container", default="TruthParticles",  help="Truth container to look for SUSY particles")
    opts = parser.parse_args()
    opts.binning = [int(b) for b in opts.binning.split(",")]
    return opts

def guess_systematic(sample):
    import systematics
    for s in systematics.flat_systematics:
        if s and s in sample:
            return s
    return "nominal"

def guess_production(sample):
    for p in production_modes:
        if p in sample:
            return p
    print "Couldn't figure out the production mode"
    print sample
    print production_modes
    sys.exit(1)

def guess_mass(sample):
    tokens = sample.split("_")
    for t in tokens:
        try: 
            mass = int(t)
            return mass
        except ValueError:
            pass
    print "Couldn't figure out the mass of the sample"
    print sample
    sys.exit(2)


def main(opts):
    import ROOT
    ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')
    # Initialize the xAOD infrastructure
    ROOT.xAOD.Init()
    
    outfile = ROOT.TFile.Open(opts.output,"recreate" if opts.recreate else "update")
    samples = glob.glob(opts.input+"/*")
    
    for sample in samples:
        if not opts.pattern in sample: continue
        tokens = sample.split("_")

        if opts.production_mode is None:
            production = guess_production(sample)
        else:
            production = opts.production_mode

        if opts.mass_position is None:
            mass = guess_mass(sample)
        else:
            mass = tokens[opts.mass_position]

        syst = guess_systematic(sample) 

        tchain = ROOT.TChain("CollectionTree")
        if opts.all_files_in_folder: files = [sample]
        else: files = glob.glob(sample+"/*root")
        for f in files:
            tchain.AddFile(f)
        ttree = ROOT.xAOD.MakeTransientTree(tchain)

        hname = "hpt_{}_{}_{}".format(production, mass, syst)
        hpt = ROOT.TH1F(hname, hname,*opts.binning)
        print "Will process",sample, (production, mass, syst)
        ST = ROOT.ST.SUSYObjDef_xAOD('ST_data')
        print "Created ST"
        for ev in range(ttree.GetEntries()):
            ttree.GetEntry(ev)
            spsp_pt = ST.GetSusySystemPt( getattr(ttree,opts.bsm_container) )/1000.
            assert ttree.EventInfo.mcEventWeights()[0] == ttree.TruthEvents[0].weights()[0]
            weight = ttree.EventInfo.mcEventWeights()[0]
            hpt.Fill(spsp_pt, weight)
        outfile.cd()
        hpt.Scale(1./hpt.Integral(0,-1))
        hpt.Write()
        del ttree
    outfile.Close()

if __name__ == "__main__": 
    opts = parse_options()
    main(opts)
