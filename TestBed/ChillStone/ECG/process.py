from filters import *


OUTLIER_FACT=5.0
DEFAULT_BPM=70.0      #  fall back BPM if we get stuck
MAX_BPM=120.0
MIN_BPM=40.0



THRESH_HALF_LIFE=0.2   #  time for threshold to decay to half it's value 
THRESH_SCALE=2.0       #  scale the threshold value (decrease to make more sensitive)
N_MEDIAN=13
MAX_MV_AV=3000         # Max scrren val for moving average
     
class Processor:

    def __init__(self,peaker,dt):
        self.peaker=peaker
        self.latency=dt*24
        self.dt=dt
        self.lpf=LPF()
        self.hpf=HPF()
        self.deriv=Dervivative()
        self.aver=MovingAverge()
        self.time=0

        
        
    # process a single ECG value 
    # assuming a sample rate of 200 Hz and  val is normalize in the range -1 -> 1
    def process(self,val):
        
        
        self.y_val=val
                       
        val=self.lpf.process(val)
      
        self.f_val=val   
        
        val=self.hpf.process(val)        
        val=self.deriv.process(val)
        val=val*val
        
        val1=self.aver.process(val)
        self.s_val=val1
        
        self.peaker.process(val1,self.time-self.latency)
        self.time += self.dt
        

# Enum to classify RR pulses 
class RRstate:
    color=((255,255,255),(255,0,0),(0,255,0))
    new=0
    outlier=1
    OK=2
           

        
class Tachiometer:

    def __init__(self,n_med,bpm_client):    
        self.RR=[]
        self.RRmed=[]
        self.RRmedian=Median(n_med)
        self.DTmedian=Median(n_med)
        self.tlast=0.0
        self.state=0    #  waiting for stability
        self.cnt=0
        self.dtLast=None
        self.dtmin=60.0/MAX_BPM
        self.dtmax=60.0/MIN_BPM
        self.RR_state_ptr=0
        self.pt0,self.pt1,self.pt2=None,None,None
        self.bpm=bpm_client
        
        
    def in_dt_range(self,dt):
        return dt < self.dtmax and dt > self.dtmin
        
    def process(self,t,y):
        
        # maintian a median of all candidate peaks
        medRRmag=self.RRmedian.process(y).median_val()
        
        
        #  Maintian a median of all delta times         
        dt=t-self.tlast

        if self.in_dt_range(dt):
            self.DTmedian.process(dt)
        
        # default state of RR peak
        state=RRstate.new    
       
       
       
        if True:   #   Hack to see what no processing does
            ptNew=[t,y,RRstate.OK]    
            
            self.RR.append(ptNew)
            self.bpm.process(ptNew)
        #  TODO filter outliers 
            self.RRmed.append((t,medRRmag))
    
            return
            
        if y > medRRmag*OUTLIER_FACT:   # TO BIG then flag as outlier
            state=RRstate.outlier
            
        ptNew=[t,y,state]    
        
        self.RR.append(ptNew)
        
        
        dt_med=self.DTmedian.median_val()
        
#       If median dt is wild assume a sensible value for peak classification
        if not self.in_dt_range(dt_med):
            dt_med=60./DEFAULT_BPM
            
      
        # if it is not an outlier then lets process it
        # maintain a history of 3 points  pt0 pt1 pt2      ---> time
        #
        
        if state != RRstate.outlier:    
            
            if self.pt0 == None:
                self.pt0=ptNew
    
            elif self.pt1 == None:
                self.pt1=ptNew
            
            else:   #  Here then we have 2 previous points
                
                
                self.pt2=ptNew
                    
                dt01 = self.pt1[0]-self.pt0[0]
                dt12 = self.pt2[0]-self.pt1[0]
                dt02 = dt01+dt12
                
                vdt01=abs(dt01-dt_med)
                vdt02=abs(dt02-dt_med)
                vdt12=abs(dt12-dt_med)
        
                ir01=self.in_dt_range(dt01)
                ir12=self.in_dt_range(dt12)
                
                
                if vdt01 < vdt02 and vdt12 < vdt02:    #   pt1 looks good
                    print ir01
                    self.pt1[2]=RRstate.OK                      #   flag as OK
                    self.pt0=self.pt1                           #   replace pt0 with pt1
                    self.pt1=self.pt2                           #           pt1 with pt2
                    self.bpm.process(self.pt1)
                elif dt01 < self.dtmin: #  pt1 looks spurious
                    self.pt1[2]=RRstate.outlier
                    self.pt1=self.pt2
                elif vdt01 < vdt02:
                    #print " Please handle me "
                    self.pt1[2]=RRstate.OK  
                    self.pt0=self.pt1                           #   replace pt0 with pt1
                    self.pt1=self.pt2                           #           pt1 with pt2
                    self.bpm.process(self.pt1)
                else:
                    self.pt0=self.pt1                           #   replace pt0 with pt1
                    self.pt1=self.pt2                           #           pt1 with pt2
                    print " Handle me"
                    
                    
        #  TODO filter outliers 
        self.RRmed.append((t,medRRmag))
    
    
"""
  convert RR deltas to BPM
"""
class BPM:

    def __init__(self,n_med):    
        self.BPMraw=[]
        self.BPMmedian=[]
        self.medianBPM=Median(n_med)
        self.tlast=0
    
    def process(self,pt):
        
        t=pt[0]
        dt=t-self.tlast
        bpm=60.0/dt
        bpm_med=self.medianBPM.process(bpm).median_val()
        
        self.BPMraw.append((t,bpm))
            
        self.BPMmedian.append((t,bpm_med))         
                
        self.tlast=t
    
 
"""
Peaker takes the moving average filter output.

"""
                        
class Peaker:

    def __init__(self,analysis,dt):
        self.state=0
        self.cnt=0
        self.flast=0
        self.analysis=analysis
        self.averN=MovingDecayAverge(int(THRESH_HALF_LIFE/dt))
        self.delay=Delay(24)
        self.threshLimit=MAX_MV_AV
        self.thresh1=0.0

    def process(self,f,t):
        """
        f is the signal value
        t is the time
        thresh1 is the preak detect threshold
        """
                
#     adaptive thresh    
        thresh1=self.thresh1 = self.delay.process(self.averN.process(min(f,self.threshLimit)*THRESH_SCALE))   

        thresh2=self.thresh1*0.5  #  reset peak detect when signal is half the turnon value.
        
        if self.state == 0:          
            if f > self.flast:
                self.state=1
                self.cnt=0         #  start counting
                self.PEAKI=f
                #print 'armed',f
            
        if self.state == 1:        #  we have detected a positive slope
                      
            if f > thresh1:   #   signal > thresh1 then here we go a QRS is detected
                self.PEAKI = max(f,self.PEAKI)
                self.peakTime=t
                self.state=2
                #print 'QRS'
                
            elif f > self.PEAKI:
              self.PEAKI=max(f,self.PEAKI)  
                
            elif f< self.flast :  #   noise peak detected   
            # Yes record and unarm noise peak detection
                self.PEAKI=0.0
                self.state=0
                #print ' Noise '
                    
        if self.state == 2:  #  We are detecting a peak wait for f < peakVal
        
            if f > self.PEAKI:
                self.PEAKI = max(f,self.PEAKI)      # record max value
               
            elif f < thresh1:   #  peak detected  
        
                
                self.analysis.process(self.peakTime,self.PEAKI)
                
                self.PEAKI=0.0
                self.state=0
                self.cnt=0
                
                #print 'waiting'
                  
        self.flast=f
        
