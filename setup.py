import os,argparse

cwd = os.getcwd()

parser = argparse.ArgumentParser(description='Setting up basic environments for SampleProduction_SNU')
parser.add_argument(	"--year", "-y",
			type=str,
			help="Which campaigns from RunIILegacy? [2016,2017,2018] ex) -y 2016,2018 OR -y 2017",
			default="2016,2017,2018",
			)
parser.add_argument(    "--method", "-m",
                        type=str,
                        help="[Fast,Full,LHE] ex) -m Full OR -m Full,Fast -m Full,LHE",
                        default="Fast,Full,LHE",
                        )
parser.add_argument(    "--dev", "-d",
                        type=bool,
                        help="Check to do lists",
                        default=True,
                        )
args = parser.parse_args()

years = args.year.split(",")
methods = args.method.split(",")
steps = {       "Full":{"pLHE-GS":
                        ["CMSSW_7_1_45_patch3","CMSSW_9_3_17","CMSSW_10_2_20"],
			"GS":
			["CMSSW_7_1_45_patch3","CMSSW_9_3_17","CMSSW_10_2_20"],
                        "DRPremix_step1":
                        ["CMSSW_8_0_31","CMSSW_9_4_7","CMSSW_10_2_5"],
                        "DRPremix_step2":
                        ["CMSSW_8_0_31","CMSSW_9_4_7","CMSSW_10_2_5"],
                        "MiniAOD":
                        ["CMSSW_9_4_9","CMSSW_9_4_7","CMSSW_10_2_5"]
                },      
                "Fast":{"FSPremix":
                        ["CMSSW_8_0_31","CMSSW_9_4_12","CMSSW_10_2_11_patch1"],
                        "MiniAOD":
                        ["CMSSW_9_4_9","CMSSW_9_4_12","CMSSW_10_2_11_patch1"]
                }
        }

setupshellfile = open("setup.sh", "w")
setupshellfile.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")

for method in methods:
  if ("LHE" in method):
    setupshellfile.write("mkdir -p LHEProduction\n")
    setupshellfile.write("cd LHEProduction\n")
    setupshellfile.write("scram project -n pLHE__CMSSW_9_3_8 CMSSW CMSSW_9_3_8\n")
    setupshellfile.write("cp -r "+cwd+"/packages/LHEProduction/pLHE/* pLHE__CMSSW_9_3_8/src/\n")
    setupshellfile.write("git clone https://github.com/cms-sw/genproductions.git\n")
    setupshellfile.write("cd -\n")
  else:
    for year in years:
      setupshellfile.write("mkdir -p "+method+"Simulation/"+year+"\n")
      setupshellfile.write("cd "+method+"Simulation/"+year+"\n")
      camp = int(year)-2016
      for i_step in range(0,len(steps[method].keys())):
        step = steps[method].keys()[i_step]
        cmssw = steps[method][step][camp]
        setupshellfile.write("scram project -n "+step+"__"+cmssw+" CMSSW "+cmssw+"\n")
        if "GS" in step:
          setupshellfile.write("pushd "+step+"__"+cmssw+"/src\n")
          setupshellfile.write("cmsenv\n") 
          setupshellfile.write("git cms-addpkg GeneratorInterface/GenFilters\n")
          setupshellfile.write("rm GeneratorInterface/GenFilters/src/*\n")
          setupshellfile.write("cp "+cwd+"/DiLepChargeFilter.cc GeneratorInterface/GenFilters/src\n")
          setupshellfile.write("scram b -j 8\n") 
          setupshellfile.write("popd\n") #JH : to use filter
        setupshellfile.write("cp -r "+cwd+"/packages/"+method+"Simulation/"+step+"/* "+step+"__"+cmssw+"/src/\n")
        setupshellfile.write("mkdir -p "+step+"__"+cmssw+"/src/tmp/\n")
      setupshellfile.write("cd -\n")
setupshellfile.close()

os.system("chmod 755 setup.sh")
os.system("source ./setup.sh")
os.system("rm setup.sh")

#FIXME fastsim : https://cms-pdmv.cern.ch/mcm/requests?dataset_name=SMS-T2tt_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8&page=0&shown=127
#FIXME :: nThreads not working for wmLHEGS 2016, maybe try making LHE for 2016 and then GS 2016
