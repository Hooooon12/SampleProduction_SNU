import os,sys,random,socket,pwd

def print_sampleinfo(sample_name, nevents, ncores, nsubcores, gridpack):
	print "[INFO] "+sample_name
	print "[INFO] || "+nevents+" events using "+ncores+" cores : evts/core = "+str(int(nevents)/int(ncores))
	print "[INFO] || "+nsubcores+" cores are being used for a single job"
	print "[INFO] || "+gridpack

def exit_argumenterr():
	print "[EXIT] Input arguments are not correctly given"
	print "[EXIT] single : python make_"+nametag+".py RUNMODE SAMPLENAME NEVENTS NCORES NSUBCORES GRIDPACKPATH"
	print "[EXIT] multiple : python make_"+nametag+".py RUNMODE LIST.dat"
	sys.exit()

def exit_runhosterr(runmode,hostname):
	print "[EXIT] "+runmode+" could not be submitted to "+hostname
	print "[EXIT] MULTICORE : SNU"
	print "[EXIT] CLUSTER : SNU tamsa & KISTI"
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
else:
  exit_argumenterr()

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
  submitmanyshellfile = open("submit_many.sh", "w")
  submitmanyshellfile.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
  submitmanyshellfile.write("eval `scramv1 runtime -sh`\n")

  listf = open(inputpath)
  lists = listf.readlines()
  listf.close()
  for listl in lists:
    listl = listl.strip()
    sample_name = listl.split("\t")[0]
    nevents = listl.split("\t")[1]
    ncores = listl.split("\t")[2]
    nsubcores = listl.split("\t")[3]
    gridpack = listl.split("\t")[4]
    submitmanyshellfile.write("source "+cwd+"/submit_many_dir/submit_"+sample_name+".sh\n")
    os.system("python make_"+nametag+".py "+runmode+" "+sample_name+" "+nevents+" "+ncores+" "+nsubcores+" "+gridpack)
    ncores_many = ncores_many+(int(ncores)*int(nsubcores))
  submitmanyshellfile.close()
else:
  sample_name = sys.argv[2]
  nevents = sys.argv[3]
  ncores = sys.argv[4]
  nsubcores = sys.argv[5]
  gridpack = sys.argv[6]

if (runmode == "MULTICORE"):
  if (int(ncores_many) > 70) or ((int(ncores)*int(nsubcores)) > 70):
    print "[EXIT] Number of cores too many : should not be more than 70 [cms*.snu.ac.kr]"
    sys.exit()

if (multi_flag == True):
  sys.exit()
else:
  if (os.path.exists("submit_many.sh") and os.path.exists("submit_many_dir")):
    submitshellfile = open("submit_many_dir/submit_"+sample_name+".sh", "w")
  else:
    submitshellfile = open("submit.sh", "w")
    submitshellfile.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
    submitshellfile.write("eval `scramv1 runtime -sh`\n")

if (runmode == "CLUSTER"):
  if (int(nsubcores) > 20):
    print "[EXIT] Number of subcores too many : should not be more than 20"
    sys.exit()

if ((int(nevents)/int(ncores)) != (float(nevents)/int(ncores))):
  print "[EXIT] Number of events per core not an integer"
  sys.exit()

if (os.path.exists(runmode+"/"+sample_name+"/") or os.path.exists("output/"+sample_name+"/")):
  print "[EXIT] Either "+runmode+"/"+sample_name+"/ or output/"+sample_name+"/ already exists"
  sys.exit()
else:
  os.system("mkdir -p "+runmode+"/"+sample_name+"/")
  if (runmode == "MULTICORE") or (runmode == "CLUSTER"):
    os.system("mkdir -p output/"+sample_name+"/")

print_sampleinfo(sample_name, nevents, ncores, nsubcores, gridpack)

submitshellfile.write("###Submitting "+sample_name+"\n")

if (runmode == "MULTICORE") or (runmode == "CLUSTER"):
  for ijob in range(1,int(ncores)+1):
    os.system("mkdir -p "+runmode+"/"+sample_name+"/run"+str(ijob))
    runshellfile = open(runmode+"/"+sample_name+"/run"+str(ijob)+"/run"+str(ijob)+".sh","wt")
    runshellfile.write("cd "+cwd+"/"+runmode+"/"+sample_name+"/run"+str(ijob)+"/\n")
    runshellfile.write("cp "+gridpack+" ./\n")
    runshellfile.write("tar -xavf "+gridpack.split("/")[-1]+"\n")
    runshellfile.write("./runcmsgrid.sh "+str(int(nevents)/int(ncores))+" "+str(random.randint(1, 10000000))+" "+nsubcores+" &> run"+str(ijob)+".log\n")
    runshellfile.write("mv cmsgrid_final.lhe "+cwd+"/output/"+sample_name+"/"+nametag+"_"+str(ijob)+".lhe\n")
    runshellfile.write("rm -rf CMSSW_* InputCards *.tar.xz gridpack_generation.log mgbasedir process runcmsgrid.sh\n")
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
submitshellfile.write("cd "+cwd+"\n")
submitshellfile.close()
