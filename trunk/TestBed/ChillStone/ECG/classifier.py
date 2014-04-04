
import circbuf

class QRSCollector:
    
    
    def __init__(self,pre_rr,post_rr,file_name,latency):
        self.fout=open(file_name,"w")
        self.pre_rr=pre_rr;
        self.post_rr=post_rr;
        
        n = pre_rr+post_rr;
        
        self.latency=latency
        
        self.buff=circbuf.CircularBuffer(n);
        self.state=0
        

    def save(self):
        
        xx=self.buff.get_window()
        self.fout.writeln(str(xx))
        
        
    def process(self,ecg_val,peak):
        
        """ 
        process an ecg value
        peak is true if we are on a RR peak. (not strictly true due to latency)
        """
        
        self.buff.add(ecg_val)
        
        if self.state == 0 :   # RESET
        
            cnt_L=0
            cnt_R=0
            self.state=1
            
        elif self.state == 1:   # WAIT FOR PRE_RR to fill   /   RESET if there is a peak
            
            if peak:
                self.state=0
            elif self.cnt_L == self.pre_rr:
                self.state=2
            else:
                self.cnt_L+=1
        
        elif self.state == 2:  # PRE_RR full so wait for a peak
            
            if peak:
                self.state = 3
        
        elif self.state == 3:  # PRE_RR full and peak has occured
            
            if peak:   #  ooops better not use this one
                self.state = 0
            elif self.cnt_R == self.post_rr:
                self.save()
                self.state=0
            else:
                self.cnt_R += 1
                
        else:
            
            print  " oooops this should not have happened "
                 
            
                    
    def quit(self):
        self.fout.close()