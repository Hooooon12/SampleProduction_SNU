import os,sys,random,socket,pwd

def print_sampleinfo(sample_name, nevents, ncores, gridpack):
	print "[INFO] "+sample_name
        print "[INFO] || "+nevents+" events using "+ncores+" cores : evts/core = "+str(int(nevents)/int(ncores))
        print "[INFO] || "+gridpack

def exit_argumenterr():
	print "[EXIT] Input arguments are not correctly given"
	print "[EXIT] single : python make_"+nametag+".py RUNMODE SAMPLENAME TUNEFILE NEVENTS NCORES GRIDPACKPATH"
	print "[EXIT] multiple : python make_"+nametag+".py RUNMODE LIST.dat"
	sys.exit()

def exit_runhosterr(runmode,hostname):
	print "[EXIT] "+runmode+" could not be submitted to "+hostname
	print "[EXIT] MULTICORE : SNU"
	print "[EXIT] CLUSTER : SNU tamsa & KISTI"
	print "[EXIT] CRABJOB : KNU & KISTI"
	sys.exit()

cwd = os.getcwd()
datasettag = cwd.split("/")[-2]
nametag =datasettag.split("__")[0]
year = cwd.split("/")[-3]

try:
  runmode = sys.argv[1]
except:
  exit_argumenterr()
if (len(sys.argv) == 3):
  if (".dat" in sys.argv[2]):
    multi_flag = True
    inputpath = sys.argv[2]
  else:
    exit_argumenterr()
elif (len(sys.argv) == 7):
  multi_flag = False
else:
  exit_argumenterr()

hostname = os.getenv("HOSTNAME")
if (runmode == "MULTICORE"):
  if not hostname in ["cms1", "cms2"]:
    exit_runhosterr(runmode,hostname)
elif (runmode == "CLUSTER"):
  if not hostname in ["tamsa1", "tamsa2", "ui10.sdfarm.kr", "ui20.sdfarm.kr"]:
    exit_runhosterr(runmode,hostname)
elif (runmode == "CRABJOB"):
  if not hostname in ["cms.knu.ac.kr", "cms01.knu.ac.kr", "cms02.knu.ac.kr", "cms03.knu.ac.kr", "lxplus", "ui10.sdfarm.kr", "ui20.sdfarm.kr"]:
    exit_runhosterr(runmode,hostname)
else:
  exit_runhosterr(runmode,hostname)

if hostname in ["tamsa1", "tamsa2", "cms1", "cms2"]:
  use_SNU = True
else:
  use_SNU = False

try:
  hostname = hostname+" "+str(socket.gethostbyname(socket.gethostname()))
except:
  print "[WARNING] socket.gethostbyname(socket.gethostname()) is not working"

ncores = 0
ncores_many = 0
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
    nevents = listl.split("\t")[2]
    ncores = listl.split("\t")[3]
    gridpack = listl.split("\t")[4]
    submitmanyshellfile.write("source "+cwd+"/submit_many_dir/submit_"+sample_name+".sh\n")
    os.system("python make_"+nametag+".py "+runmode+" "+sample_name+" "+tunefile+" "+nevents+" "+ncores+" "+gridpack)
    ncores_many = ncores_many+int(ncores)
  submitmanyshellfile.close()
else:
  sample_name = sys.argv[2]
  tunefile = sys.argv[3].replace(".py","").replace("skeleton/","")
  nevents = sys.argv[4]
  ncores = sys.argv[5]
  gridpack = sys.argv[6]

if (runmode == "MULTICORE"):
  if (int(ncores_many) > 70 or int(ncores) > 70):
    print "[EXIT] Number of cores too many : should not be more than 70 [cms*.snu.ac.kr]"
    sys.exit()

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

if (int(nevents)/int(ncores) > 5000):
  print "[EXIT] Number of events per core too many : should not be more than 5000"
  sys.exit()

if ((int(nevents)/int(ncores)) != (float(nevents)/int(ncores))):
  print "[EXIT] Number of events per core not an integer"
  sys.exit()

if (runmode == "CRABJOB"):
  if (year == "2016"):
    print "[EXIT] 2016 Campaign samples is highly recommended to be submitted with pLHE and GS configurations separately since nThreads option is not available"
    sys.exit()

if (os.path.exists(runmode+"/"+sample_name+"/") or os.path.exists("output/"+sample_name+"/")):
  print "[EXIT] Either "+runmode+"/"+sample_name+"/ or output/"+sample_name+"/ already exists"
  sys.exit()
else:
  os.system("mkdir -p "+runmode+"/"+sample_name+"/")
  if (runmode == "MULTICORE") or (runmode == "CLUSTER"):
    os.system("mkdir -p output/"+sample_name+"/")

print_sampleinfo(sample_name, nevents, ncores, gridpack)

cmsdriverf = open("skeleton/"+nametag+".dat")
cmsdrivers = cmsdriverf.readlines()
cmsdriverf.close()
for cmsdriverl in cmsdrivers:
  if (year == cmsdriverl.strip().split("\t")[0]):
    cmsdriverdat = cmsdriverl.strip().split("\t")[1]

os.system("mkdir -p Configuration/GenProduction/python")
os.system("cp skeleton/"+tunefile+".py Configuration/GenProduction/python/"+sample_name+".py")
os.system("sed -i 's|###GRIDPACK|    args = cms.vstring(\""+gridpack+"\"),|g' Configuration/GenProduction/python/"+sample_name+".py")

cmsdrivercmd = "cmsDriver.py Configuration/GenProduction/"+sample_name+".py -n "+str(int(nevents)/int(ncores))+" "+cmsdriverdat
submitshellfile.write("###Submitting "+sample_name+"\n")

if (runmode == "MULTICORE") or (runmode == "CLUSTER"):
  for ijob in range(1,int(ncores)+1):
    os.system("mkdir -p "+runmode+"/"+sample_name+"/run"+str(ijob))
    runshellfile = open(runmode+"/"+sample_name+"/run"+str(ijob)+"/run"+str(ijob)+".sh","w")
    runshellfile.write("cd "+cwd+"/"+runmode+"/"+sample_name+"/run"+str(ijob)+"/\n")
    runshellfile.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
    runshellfile.write("eval `scramv1 runtime -sh`\n")
    this_cmsdrivercmd = cmsdrivercmd+" --python_filename run"+str(ijob)+".py --fileout \"file:"+cwd+"/output/"+sample_name+"/"+nametag+"_"+str(ijob)+".root\" --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="+str(random.randint(1, 10000000))
    runshellfile.write(this_cmsdrivercmd+"\n")
    runshellfile.write("cmsRun run"+str(ijob)+".py &> run"+str(ijob)+".log\n")
    runshellfile.close()

    submitshellfile.write("cd "+cwd+"/"+runmode+"/"+sample_name+"/run"+str(ijob)+"\n")
    if (runmode == "MULTICORE"):
      submitshellfile.write("chmod 755 "+cwd+"/"+runmode+"/"+sample_name+"/run"+str(ijob)+"/run"+str(ijob)+".sh\n")
      submitshellfile.write("nohup "+cwd+"/"+runmode+"/"+sample_name+"/run"+str(ijob)+"/run"+str(ijob)+".sh &\n")
    elif (runmode == "CLUSTER"):
      os.system("cp skeleton/condor.jds "+runmode+"/"+sample_name+"/run"+str(ijob))
      os.system("sed -i 's|###CONDORRUN|executable = run"+str(ijob)+".sh|g' "+runmode+"/"+sample_name+"/run"+str(ijob)+"/condor.jds")
      os.system("sed -i 's|###JOBBATCHNAME|+JobBatchName=\""+sample_name+"\"|g' "+runmode+"/"+sample_name+"/run"+str(ijob)+"/condor.jds")
      submitshellfile.write("condor_submit condor.jds\n")

elif (runmode == "CRABJOB"):
  os.system("cp skeleton/crab.py "+runmode+"/"+sample_name+"/")
  os.system("sed -i 's|###REQUESTNAME|config.General.requestName = \""+sample_name+"__"+datasettag+"\"|g' "+runmode+"/"+sample_name+"/crab.py")
  os.system("sed -i 's|###PSETNAME|config.JobType.psetName = \""+sample_name+".py\"|g' "+runmode+"/"+sample_name+"/crab.py")
  os.system("sed -i 's|###OUTPUTDATASET|config.Data.outputPrimaryDataset = \""+sample_name+"\"|g' "+runmode+"/"+sample_name+"/crab.py")
  os.system("sed -i 's|###OUTPUTTAG|config.Data.outputDatasetTag = \""+datasettag+"\"|g' "+runmode+"/"+sample_name+"/crab.py")
  os.system("sed -i 's|###UNITSPERJOB|config.Data.unitsPerJob = "+str(int(nevents)/int(ncores))+"|g' "+runmode+"/"+sample_name+"/crab.py")
  os.system("sed -i 's|###NJOBS|NJOBS = "+str(int(ncores))+"|g' "+runmode+"/"+sample_name+"/crab.py")

  runshellfile = open(runmode+"/"+sample_name+"/run.sh","w")
  this_cmsdrivercmd = cmsdrivercmd+" --python_filename "+sample_name+".py --fileout \""+nametag+".root\" --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="+str(random.randint(1, 10000000))+" --nThreads 4"
  runshellfile.write(this_cmsdrivercmd+"\n")
  runshellfile.write("crab submit -c crab.py\n")
  runshellfile.close()

  submitshellfile.write("cd "+cwd+"/"+runmode+"/"+sample_name+"\n")
  submitshellfile.write("source run.sh\n")
submitshellfile.write("cd "+cwd+"\n")
submitshellfile.close()
