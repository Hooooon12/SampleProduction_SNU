import os,sys

runfile = sys.argv[1]

minbiasf = open("selected_ThisMinBias.dat")
minbiass = minbiasf.readlines()
minbiasf.close()

os.system("mv "+runfile+" run_tmp.py")
pileup_input = ""
for i_minbias in range(0,len(minbiass)-1):
  minbiasl_sel = minbiass[i_minbias].strip()
  pileup_input = pileup_input+"\""+minbiasl_sel+"\",\n"

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
    runf.write(runl+"\n")
runf.close()
