# SampleProduction

## Samples could be made using following runmodes and servers

RUNMODE : MULTICORE / CLUSTER / CRABJOB
MULTICORE : SNU
CLUSTER : SNU tamsa / KISTI
CRABJOB : KNU / KISTI


## Setting up configuration file generators

Execute the following command line
```bash
python setup.py -m [LHE/Fast/Full] -y [2016/2017/2018]
```
LHE : produce LHE files from gridpacks
Fast : Fast simulation configuration files
Full : Full simulation configuration files

For selected specific campaign setups, for example, execute
```bash
python setup.py -m Full -y 2017 # 2017, full simulation
python setup.py -m Fast,Full -y 2017 # 2017, fast and full simulation
python setup.py -m Full -y 2016,2017 # 2016 and 2017, full simulation
python setup.py -m LHE,Full -y 2016 # LHE production & 2016, full simulation
```
Or for whole specific campaign setups, execute without any option
```bash
python setup.py
```

Above configuration files are from
```bash
Fast : https://cms-pdmv.cern.ch/mcm/requests?dataset_name=SMS-T2tt_dM-10to80_genHT-160_genMET-80_mWMin-0p1_Tune*_13TeV-madgraphMLM-pythia8&page=-1&shown=127
Full : https://cms-pdmv.cern.ch/mcm/requests?dataset_name=HeavyNeutrino_lljj_M-1_V-0p0949736805647_e_massiveAndCKM_LO_Tune*_madgraph-pythia8&page=0&shown=549755816063
```
