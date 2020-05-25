import os,sys,random

runfile = sys.argv[1]
n_minbias = sys.argv[2]

minbiasf = open("ThisMinBias.dat")
minbiass = minbiasf.readlines()
minbiasf.close()

os.system("mv "+runfile+" run_tmp.py")
minbiasf_sel = open("selected_ThisMinBias.dat","w")
pileup_input = ""
use_SNU = False
for i_minbias in range(0,int(n_minbias)):
  minbiasl_sel = minbiass[random.randint(0, len(minbiass)-1)].strip()
  minbiasf_sel.write(minbiasl_sel+"\n")
  if i_minbias == 0:
    if os.path.exists(minbiasl_sel):
      use_SNU = True
  if use_SNU == True:
    pileup_input = pileup_input+"\"file:"+minbiasl_sel+"\",\n"
  else:
    pileup_input = pileup_input+"\""+minbiasl_sel+"\",\n"
minbiasf_sel.close()

runtmpf = open("run_tmp.py")
runs = runtmpf.readlines()
runtmpf.close()
os.system("rm run_tmp.py")

runf = open(runfile,"w")
for runl in runs:
  if "process.mixData.input.fileNames" in runl:
    runf.write("process.mixData.input.fileNames = cms.untracked.vstring([\n")
    runf.write(pileup_input)
    runf.write("])\n")
  else:
    runf.write(runl)
runf.close()
