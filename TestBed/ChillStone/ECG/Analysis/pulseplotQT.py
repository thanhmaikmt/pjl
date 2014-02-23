from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
from  util import *

app = QtGui.QApplication([])
view = pg.GraphicsView()

l = pg.GraphicsLayout(border=(100,100,100))
view.setCentralItem(l)
view.show()
view.setWindowTitle('ECG')
view.resize(1200,600)


name=QtGui.QFileDialog.getOpenFileName(directory='../data/')
xx=readECG(name)

# Crude down sample 400-->200 Hz
nSamps=len(xx)/2

x=np.zeros(nSamps)
t=np.zeros(nSamps)

srate=200
dt=1.0/srate
time=0.0

for i in range(nSamps):
     x[i]=xx[2*i]+xx[2*i+1]
     t[i]=time
     time+=dt
     
# 200ms is min time between pulses
minPulsePeriodSamps=200e-3*srate

# A Real-Time QRS Detection Algorithm

# IEEE TRANSACTIONS ON BIOMEDICAL ENGINEERING, VOL. BME-32, NO. 3, MARCH 1985


x50=np.zeros(50)
y1=np.zeros(nSamps)
y2=np.zeros(nSamps)
y3=np.zeros(nSamps)
y4=np.zeros(nSamps)
y5=np.zeros(nSamps)
x2=np.zeros(nSamps)



#  LPF  6 samples delay
#   y(nT) = 2y(nT - T) - y(nT - 2 T) + x(nT) - 2x(nT- 6T)+x(nT- 12T)

for i in range(12,nSamps):
    y1[i] = 2*y1[i-1] - y1[i-2] +  x[i] - 2*x[i-6] + x[i-12]

    
# HPF  16 samples delay
# y(nT) = 32x(nT - 16 T) - [y(nT - T) + x(nT) - x(nT - 32 T)]

for i in range(32,nSamps):
    y2[i]=32*y1[i-16] -  (y2[i-1]   + y1[i]  - y1[i-32])
 

# Derivative  2 samples delay
#  y(nT) = (1/8 T) [-x(nT - 2 T) - 2x(nT - T)+ 2x(nT + T) + x(nT+ 2T)]   


for i in range(2,nSamps-2):
    y3[i]= (1.0/8.0/dt) *( -y2[i-2] - 2*y2[i-1]  + 2* y2[i+1]  + y2[i+2])
    
    
# Square   y[nT]= x[nT]^2    0 sample delay

for i in range(nSamps):
    y4[i]= y3[i]*y3[i]
    

#  Moving window integration  30 sample delay 
# y(nT) = (1/N) [x(nT- (N - 1) T) +x(nT- (N - 2) T)
    
sumWin=0
N=30

for i in range(nSamps):
    sumWin += y4[i]
    y5[i] = sumWin/N
    if i >= N:
        sumWin -= y4[i-N]

# Threshold detection

thresh1=2.0e7
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

for f,ttt in zip(y5,t):
    
    tt=ttt-24*dt   #  compensate for processing delay
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
      
        elif f< flast :  #   noise peak detected   
            PEAKI = max(PEAKI,f)            # Yes record and unarm noise peak detection
            NPKI = 0.125 * PEAKI + 0.875*NPKI
            npkis[0].append(t)
            npkis[1].append(NPKI)
            PEAKI=0.0
            state=0
            print '1->0 NPKI =' ,NPKI
                
    if state == 2:  #  We are detecting a peak wait for f < peakVal
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
    
    

# Make something like a pulse for pyqtplot

xx=[0]
yy=[0]
dt=.02

for xxx,yyy in zip(peaksQRStime,peaksQRSval):
    xx.append(xxx)
    yy.append(0)
    xx.append(xxx)
    yy.append(yyy)
    xx.append(xxx+dt)
    yy.append(yyy)
    xx.append(xxx+dt)
    yy.append(0)

i1=0
i2=len(t)




l.nextRow()
l2 = l.addLayout(colspan=1, border=(50,0,0))
l2.setContentsMargins(10, 10, 10, 10)




pp = l2.addPlot()
pp.plot(xx,yy)
pp.showGrid(x=True,y=True,alpha=.9)
ppref=pp

l2.nextRow()
pp=l2.addPlot()
pp.plot(t[i1:i2],x[i1:i2])   #
pp.showGrid(x=True,y=True,alpha=.9)
pp.setXLink(ppref)

l2.nextRow()
pp = l2.addPlot()
pp.plot(t[i1:i2],y5[i1:i2])  #
pp.setXLink(ppref)    
pp.showGrid(x=True,y=True,alpha=.9)


## Start Qt event loop unless running in interactive mode.

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
