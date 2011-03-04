from  matplotlib.pyplot import *
from math import *
from numpy import *


def stats(x):
    N=len(vals)
    sum=0.0
    for v in vals:
        sum+=v
    aver=sum/float(N)
    
    sum=0.0
    for v in vals:
        sum += (aver-v)**2
        
    std = sqrt(sum/float(N))
    
    return N,aver,std
        
    

file="/home/pjl/A/Marking/2011/CI.raw"

fin=open(file,"r")

data=fin.read()
toks=data.split()

N=len(toks)
print " N=",N

outOf=60
sum=0.0
cohorts={}
for tok in toks:
    #print ">",tok,"<"
    #for c in tok:
    #    print c
        
    if tok[0] == '*':
        raw=[]
        cohorts[tok[1:]]=raw
        continue
    
    val=float(tok)
    #print val
    val = val*100.0/outOf
    #print val
    raw.append(val)
 
for name,vals in cohorts.items():
    
    print name, stats(vals)


"""
while True:
    line=fin.readLine

subplot(311)
plot(fs,h2)
ylabel("H(f)")
grid()

subplot(312)
vlines(freqs,ymin,h1)
ylabel("X(f)")
grid()

subplot(313)
vlines(freqs,ymin,ymax)
xlabel("f [Hz]")
ylabel("Y(f)")
grid()

show()
"""