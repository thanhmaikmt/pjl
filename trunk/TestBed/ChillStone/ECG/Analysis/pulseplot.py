import matplotlib.pyplot as plt
import numpy as np
from  util import *

name="../data/Feb16_18_38_12.txt"


xx=readECG(name)
nSamps=len(xx)/2
x=np.zeros(nSamps)
t=np.zeros(nSamps)

dt=1.0/200.0
time=0.0
for i in range(nSamps):
     x[i]=xx[2*i]+xx[2*i+1]
     t[i]=time
     time+=dt
     
srate=1.0/dt

# 200ms is min time between pulses
minPulsePeriodSamps=200e-3*srate


# A Real-Time QRS Detection Algorithm

# IEEE TRANSACTIONS ON BIOMEDICAL ENGINEERING, VOL. BME-32, NO. 3, MARCH 1985

y0=x
y1=np.zeros(nSamps)
y2=np.zeros(nSamps)
y3=np.zeros(nSamps)
y4=np.zeros(nSamps)
y5=np.zeros(nSamps)



#  LPF 
#   y(nT) = 2y(nT - T) - y(nT - 2 T) + x(nT) - 2x(nT- 6T)+x(nT- 12T)

for i in range(12,nSamps):
    y1[i] = 2*y1[i-1] - y1[i-2] +  x[i] - 2*x[i-6] + x[i-12]

    
# HPF
# y(nT) = 32x(nT - 16 T) - [y(nT - T) + x(nT) - x(nT - 32 T)]

for i in range(32,nSamps):
    y2[i]=32*y1[i-16] -  (y2[i-1]   + y1[i]  - y1[i-32])
 
 
filteredECG=y2

# Derivative
#  y(nT) = (1/8 T) [-x(nT - 2 T) - 2x(nT - T)+ 2x(nT + T) + x(nT+ 2T)]   


for i in range(2,nSamps-2):
    y3[i]= (1.0/8.0/dt) *( -y2[i-2] - 2*y2[i-1]  + 2* y2[i+1]  + y2[i+2])
    
    
# Square   y[nT]= x[nT]^2

for i in range(nSamps):
    y4[i]= y3[i]*y3[i]
    

#  Moving window integration
# y(nT) = (1/N) [x(nT- (N - 1) T) +x(nT- (N - 2) T)
    


sumWin=0
N=30

for i in range(nSamps):
    sumWin += y4[i]
    y5[i] = sumWin/N
    if i >= N:
        sumWin -= y4[i-N]
        

thresh1=6e7
thresh2=thresh1*0.5

peaking=False
peakVal=0.0

peaksQRStime=[]
peaksQRSval=[]
peakNoise=0.0
fLast=0.0
cnt=0

SPKI=0.0
NPKI=0.0

npkis=[[],[]]
spkis=[[],[]]

SPKI=0.0
NPKI=0.0

waitingForUp=True

state=0
cntMin=20
flast=0

for f,tt in zip(y5,t):
    
    # thresh1 = NPKI + 0.25 * (SPKI - NPKI)   
    # thresh2 = 0.5*thresh1
    # print NPKI,SPKI
    
    if state == 0:          
        if f > flast:
            state=1
            cnt=0         #  start counting
            PEAKI=f
            print '0->1'
        
    if state == 1:        #  we have detected a positive slope
                  
        if f > thresh1:   #   signal > thresh1 then here we go a QRS is detected
            PEAKI = f
            peakTime=tt
            state=2
            print '1->2'
        elif f > PEAKI:
          PEAKI=f  
          pass            #  wait for minCnt samples to ignore local peaks.
      
        elif cnt > cntMin  and  f< flast :  #   noise peak detected   
            PEAKI = max(PEAKI,f)            # Yes record and unarm noise peak detection
            NPKI = 0.125 * PEAKI + 0.875*NPKI
            npkis[0].append(t)
            npkis[1].append(NPKI)
            PEAKI=0.0
            state=0
            print '1->0 NPKI =' ,NPKI
                
    elif state == 2:  #  We are detecting a peak wait for f < peakVal
        if f > PEAKI:
            PEAKI = f      # record max value
            SPKI=max(SPKI,PEAKI*0.25)

        elif f < thresh2:   #  peak detected  
        
            peaksQRStime.append(peakTime)
            peaksQRSval.append(PEAKI)
            SPKI = 0.125* PEAKI + 0.875*SPKI
            spkis[0].append(t)
            spkis[1].append(SPKI)
            PEAKI=0.0
            state=0
            cnt=0
            print '2->0 SPKI=',SPKI
            
    cnt += 1
    flast = f
    
    
     
plt.figure(1)     
plt.vlines(peaksQRStime,0,peaksQRSval)
plt.show()

if False:
    plt.figure(2)
    i1=0
    i2=len(t)
    
    nc='7'
    plt.subplot(nc+"11")
    plt.plot(t[i1:i2],x[i1:i2],"g")   #
    
    plt.subplot(nc+"12")
    plt.plot(t[i1:i2],y1[i1:i2],"r")  #
    
    plt.subplot(nc+"13")
    plt.plot(t[i1:i2],y2[i1:i2],"r")  #
    
    plt.subplot(nc+"14")
    plt.plot(t[i1:i2],y3[i1:i2],"r")  #
    
    plt.subplot(nc+"15")
    plt.plot(t[i1:i2],y4[i1:i2],"r")  #
    
    plt.subplot(nc+"16")
    plt.plot(t[i1:i2],y5[i1:i2],"r")  #
    
    plt.subplot(nc+"17")
    plt.vlines(peaksQRStime,0,peaksQRSval)
    plt.xlim([0,10])
    plt.show()



if False:
    """
    The set of thresholds initially applied to the integration waveform is computed from
    SPKI = 0.125 PEAKI + 0.875 SPKI   (if PEAKI is the signal peak)
    
    NPKI = 0.125 PEAKI + 0.875 NPKI (if PEAKI is the noise peak)
    
    THRESHOLD Il = NPKI + 0.25 (SPKI - NPKI)
    
    THRESHOLD I2 = 0.5 THRESHOLD Il
    
    where all the variables refer to the integration waveform:
    
    PEAKI is the overall peak,
    SPKI is the running estimate of the signal peak,
    NPKI is the running estimate of the noise peak,
    THRESHOLD Il is the first threshold applied, and
    THRESHOLD 12 is the second threshold applied.
    
    
    A peak is a local maximum determined by observing when the signal changes direction within a predefined time interval. 
    The signal peak SPKI is a peak that the algorithm has already established to be a QRS complex. 
    The noise peak NPKI is any peak that is not related to the QRS (e.g., the Twave). 
    The thresholds are based upon running estimates of SPKI and NPKI. 
    That is, new values of these variables are computed in part from their prior values. 
    When a new peak is detected, it must first be classified as a noise peak or a signal peak. 
    To be a signal peak, the peak must exceed THRESHOLD I1 as the signal is first analyzed or THRESHOLD 12 if searchback is required to find the QRS. 
    When the QRS complex is found using the second threshold-,
    
    SPKI = 0.25 PEAKI + 0.75 SPKI. 
    
    The set of thresholds applied to the filtered ECG is determined from
    
    SPKF = 0.125 PEAKF + 0.875 SPKF (if PEAKF is the signal peak)
    
    NPKF = 0.125 PEAKF + 0.875 NPKF (if PEAKF is the noise peak)
    
    THRESHOLD F1 = NPKF + 0.25 (SPKF - NPKF)
    THRESHOLD F2 = 0.5 THRESHOLD Fl
    
    where all the variables refer to the filtered ECG:
    
    PEAKF is the overall peak,
    SPKF is the running estimate of the signal peak,
    NPKF is the running estimate of the noise peak,
    THRESHOLD Fl is the first threshold applied, and
    THRESHOLD F2 is the second threshold applied.
    
    When the QRS complex is found using the second threshold,
    
    SPKF = 0.25 PEAKF + 0.75 SPKF. 
    
    For irregular heart rates, the first threshold of each set is reduced by half so as to increase the detection sensitivity and to avoid missing beats:
    THRESHOLDII v- 0.5 THRESHOLD II 
    THRESHOLD Fl 0.5 THRESHOLD Fl. 
    
    To be identified as a QRS complex, a peak must be recognized as such a complex in both the integration and bandpass-filtered waveforms.
    
    """
    
    
    print " srate = ",srate, " Hz"
    print " minPulsePeriodSamps ", minPulsePeriodSamps
    
    
    # number of samples before we can fire again
    holdSamps=minPulsePeriodSamps*.7
    
    fireFact=3.0
    
    # TODO work out a decent decay rate here.
    # half life of sort of moving average  
    halfT=4
    halfSamps=halfT/dt
    
    fact1,fact2=halfLifeFactors(halfSamps)
    
    rectAverage=0.0   # keep a record of the average rectified value.
       
    cnt=0
    tPeaks=[]
    
    ARMED,FIRED,PEAKED=range(3)
    
    state=PEAKED
    
    for x1,t1 in zip(x,t):
        rectAverage=rectAverage*fact1+abs(x1)*fact2
        cnt += 1
        
        if state==ARMED:
            if x1 > rectAverage*fireFact:
                state=FIRED
                xPeak=x1
                tPeak=t1
                
        elif state==FIRED:
            if x1 < xPeak:
                state=PEAKED
                tPeaks.append(tPeak)
                xPeaks.append(xPeak)
                cnt=0              
                continue
            
        elif state == PEAKED:
            if cnt > holdSamps:
                state=ARMED
            
    
    
    print tPeaks
        
            

            
    # 50 Hz filter.  
     
    print len(t)