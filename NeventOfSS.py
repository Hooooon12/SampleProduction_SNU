#This counts SS Nevents in an lhe file

with open('pLHE_1.lhe') as f:
  lines = f.readlines()

events = []
OSevents = []
SSevents = []

for i in range(len(lines)):
  if '<event>' in lines[i]:
    this_ev = []
    for j in range(20):
      if not 'aMCatNLO' in lines[i+2+j]:
        this_ev.append(lines[i+2+j].strip())
      else:
        break
    events.append(this_ev)

for i in range(len(events)):
  SS = 1
  for ptcl in events[i]:
    if int(ptcl.split(' ')[0])==13 or int(ptcl.split(' ')[0])==11:
      SS*=1
    elif int(ptcl.split(' ')[0])==-13 or int(ptcl.split(' ')[0])==-11:
      SS*=-1
  if SS == 1:
    SSevents.append(events[i])
  elif SS == -1:
    OSevents.append(events[i])

print "total Nevents:",len(events)
print "SS Nevents:",len(SSevents)
print "OS Nevents:",len(OSevents)
