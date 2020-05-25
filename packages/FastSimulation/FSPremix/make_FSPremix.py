import os,sys,random,socket,pwd

def print_sampleinfo(sample_name, inputpath):
        print "[INFO] "+sample_name
        print "[INFO] || "+inputpath

def exit_argumenterr():
	print "[EXIT] Input arguments are not correctly given"
	print "[EXIT] single : python make_"+nametag+".py SAMPLENAME TUNEFILE INPUTPATH NEVENTS NCORES"
	print "[EXIT] multiple : python make_"+nametag+".py LIST.dat"
	sys.exit()

def exit_runhosterr(hostname):
	print "[EXIT] FastSimulation samples can only be submitted through CRABJOB"
	print "[EXIT] CRABJOB : KNU & KISTI"
	sys.exit()

username = pwd.getpwuid(os.getuid()).pw_name

cwd = os.getcwd()
datasettag = cwd.split("/")[-2]
nametag =datasettag.split("__")[0]
year = cwd.split("/")[-3]

if (len(sys.argv) == 2):
  if (".dat" in sys.argv[1]):
    multi_flag = True
    inputpath = sys.argv[1]
  else:
    exit_argumenterr()
elif (len(sys.argv) >= 4):
  multi_flag = False
else:
  exit_argumenterr()

hostname = os.getenv("HOSTNAME")
if not hostname in ["cms.knu.ac.kr", "cms01.knu.ac.kr", "cms02.knu.ac.kr", "cms03.knu.ac.kr", "ui10.sdfarm.kr", "ui20.sdfarm.kr"]:
  exit_runhosterr(hostname)
if hostname in ["ui10.sdfarm.kr", "ui20.sdfarm.kr"]:
  use_KISTI = True
else:
  use_KISTI = False

try:
  hostname = hostname+" "+str(socket.gethostbyname(socket.gethostname()))
except:
  print "[WARNING] socket.gethostbyname(socket.gethostname()) is not working"

if (multi_flag == True):
  if (os.path.exists("submit_many.sh") or os.path.exists("submit_many_dir")):
    print "[EXIT] Make sure you cleared up all the shell script files before generating new submit scripts"
    print "[EXIT] Please execute : rm -rf sumbit_many_dir; rm submit_many.sh"
    sys.exit()

  os.system("mkdir submit_many_dir")
  tmp_multi_flag = open ("tmp/multi_flag", "w")
  tmp_multi_flag.close()
  submitmanyshellfile = open("submit_many.sh", "w")
  submitmanyshellfile.write("rm tmp/multi_flag\n")
  submitmanyshellfile.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
  submitmanyshellfile.write("eval `scramv1 runtime -sh`\n")
  submitmanyshellfile.write("scram b -j 2\n")

  listf = open(inputpath)
  lists = listf.readlines()
  listf.close()
  for listl in lists:
    listl = listl.strip()
    sample_name = listl.split("\t")[0]
    tunefile = listl.split("\t")[1].replace(".py","").replace("skeleton/","")
    inputpath = listl.split("\t")[2]
    submitmanyshellfile.write("source "+cwd+"/submit_many_dir/submit_"+sample_name+".sh\n")
    try:
      crab_nevents = listl.split("\t")[3]
      crab_ncores = listl.split("\t")[4]
      os.system("python make_"+nametag+".py "+sample_name+" "+tunefile+" "+inputpath+" "+crab_nevents+" "+crab_ncores)
    except:
      os.system("python make_"+nametag+".py "+sample_name+" "+tunefile+" "+inputpath)
    inputlinef = open("tmp/"+sample_name+".dat")
    inputlines = inputlinef.readlines()
    inputlinef.close()
  submitmanyshellfile.close()
else:
  sample_name = sys.argv[1]
  tunefile = sys.argv[2].replace(".py","").replace("skeleton/","")
  inputpath = sys.argv[3]

  if (".lhe" in inputpath):
    os.system("ls -1 "+inputpath+" &> tmp/"+sample_name+".dat")
  else:
    os.system("ls -1 "+inputpath+"/*lhe &> tmp/"+sample_name+".dat")

  inputlinef = open("tmp/"+sample_name+".dat")
  inputlines = inputlinef.readlines()
  inputlinef.close()
  if (len(inputlines) > 1):
    print "[EXIT] Multiple LHE files detected, INPUTPATH not correctly given"
    print "[EXIT] /PATH/TO/INPUTFILE/LHEFILE.lhe"
    sys.exit()
  inputlinef_tmp = open("tmp/"+sample_name+"_tmp.dat","w")
  for inputlinel in inputlines:
    inputlinel = inputlinel.strip()
    if (use_KISTI == True):
      inputlinef_tmp.write("root://cms-xrdr.private.lo:2094//xrd/store/user/"+username+"/"+inputlinel.split("/xrootd/")[1]+"\n")
    else:
      inputlinef_tmp.write("root://cluster142.knu.ac.kr//store/user/"+username+"/"+inputlinel.split(username)[1]+"\n")

    try:
      crab_nevents = sys.argv[4]
      crab_ncores = sys.argv[5]
    except:
      readlhef = open(inputlinel)
      readlhes = readlhef.readlines()
      readlhef.close()
      for readlhel in readlhes:
        readlhel = readlhel.strip()
        if "#  Number of Events        :" in readlhel:
          crab_nevents = readlhel.replace("#  Number of Events        :","")
          crab_ncores = str(int(crab_nevents)/1000)
          break
  inputlinef_tmp.close()
  os.system("mv tmp/"+sample_name+"_tmp.dat tmp/"+sample_name+".dat")
  inputlinef = open("tmp/"+sample_name+".dat")
  inputlines = inputlinef.readlines()
  inputlinef.close()

if (multi_flag == True):
  sys.exit()
else:
  if os.path.exists("tmp/multi_flag"):
    submitshellfile = open("submit_many_dir/submit_"+sample_name+".sh", "w")
  else:
    submitshellfile = open("submit.sh", "w")
    submitshellfile.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
    submitshellfile.write("eval `scramv1 runtime -sh`\n")
    submitshellfile.write("scram b -j 2\n")

if os.path.exists("CRABJOB/"+sample_name+"/"):
  print "[EXIT] Either CRABJOB/"+sample_name+"/ already exists"
  sys.exit()
else:
  os.system("mkdir -p CRABJOB/"+sample_name+"/")

print_sampleinfo(sample_name, inputpath)

cmsdriverf = open("skeleton/"+nametag+".dat")
cmsdrivers = cmsdriverf.readlines()
cmsdriverf.close()
for cmsdriverl in cmsdrivers:
  if (year == cmsdriverl.strip().split("\t")[0]):
    cmsdriverdat = cmsdriverl.strip().split("\t")[1]

os.system("mkdir -p Configuration/GenProduction/python")
os.system("cp skeleton/"+tunefile+".py Configuration/GenProduction/python/"+sample_name+".py")

submitshellfile.write("###Submitting "+sample_name+"\n")

os.system("cp skeleton/crab.py CRABJOB/"+sample_name+"/")
os.system("sed -i 's|###REQUESTNAME|config.General.requestName = \""+sample_name+"__"+datasettag+"\"|g' CRABJOB/"+sample_name+"/crab.py")
os.system("sed -i 's|###PSETNAME|config.JobType.psetName = \""+sample_name+".py\"|g' CRABJOB/"+sample_name+"/crab.py")
os.system("sed -i 's|###OUTPUTDATASET|config.Data.outputPrimaryDataset = \""+sample_name+"\"|g' CRABJOB/"+sample_name+"/crab.py")
os.system("sed -i 's|###OUTPUTTAG|config.Data.outputDatasetTag = \""+datasettag+"\"|g' CRABJOB/"+sample_name+"/crab.py")
os.system("sed -i 's|###UNITSPERJOB|config.Data.unitsPerJob = "+str(int(crab_nevents)/int(crab_ncores))+"|g' CRABJOB/"+sample_name+"/crab.py")
os.system("sed -i 's|###NJOBS|NJOBS = "+crab_ncores+"|g' CRABJOB/"+sample_name+"/crab.py")
os.system("cp skeleton/sedcommand.py CRABJOB/"+sample_name+"/")
os.system("cp skeleton/FastMinBias_"+year+".dat CRABJOB/"+sample_name+"/selected_ThisMinBias.dat")
#  if (year == "2016"): minbias_files = "\"dbs:/Neutrino_E-10_gun/RunIISummer16FSPremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v4-v1/GEN-SIM-DIGI-RAW\""
#  elif (year == "2017"): minbias_files = "\"dbs:/Neutrino_E-10_gun/RunIIFall17FSPrePremix-PUMoriond17_94X_mc2017_realistic_v15-v1/GEN-SIM-DIGI-RAW\""
#  elif (year == "2018"): minbias_files = "\"dbs:/Neutrino_E-10_gun/RunIIFall17FSPrePremix-PUMoriond18_102X_upgrade2018_realistic_v15-v2/GEN-SIM-DIGI-RAW\""

runshellfile = open("CRABJOB/"+sample_name+"/run.sh","w")
this_cmsdrivercmd = "cmsDriver.py Configuration/GenProduction/"+sample_name+".py "+cmsdriverdat+" -n 91117 --python_filename "+sample_name+".py --fileout \""+nametag+".root\" --nThreads 4 --filein \""+inputlines[0].strip()+"\" --pileup_input \"###PILEUP_INPUT\""
runshellfile.write(this_cmsdrivercmd+"\n")
runshellfile.write("python sedcommand.py "+sample_name+".py\n")
runshellfile.write("crab submit -c crab.py\n")
runshellfile.close()

submitshellfile.write("cd "+cwd+"/CRABJOB/"+sample_name+"\n")
submitshellfile.write("source run.sh\n")
submitshellfile.write("cd "+cwd+"\n")
submitshellfile.close()
