import subprocess,inspect
import atexit,time,Queue,threading
import MB

class Client:
    """
    Users side of the beat detection system.
    This client sends beats to the server.
    It reads the servers output which should send estimates of the tempo
    e.g.
     client.stomp(time_stamp)   #   send event to the server analysis  
     bpm=client.get_tempo()         #   get current tempo estimate
    
    """
 
    
    def __init__(self,debug=False,t_min=0.5,t_max=1.5):
        
        self.debug=debug
        self.proc=None
      
        self.proc=subprocess.Popen([MB.PYTHON_CMD+" -i ../beat/beatserver.py -g"],shell=True,
                                   stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE)
        
        self.pipe   = self.proc.stdin
        self.stdout = self.proc.stdout
        #print self.proc.pid
        

        self.err_t=threading.Thread(target=self._pipe_reader)
       
        self.q=Queue.Queue()
        self.err_t.start()
        self.tempo=-1
            
        self.hist=[]     
         
        self.beat_len=1.0
        self.bar_len=4.0
        self.t_max=t_max
        self.t_min=t_min
        self.obsevers=[]
        
    def _send(self,cmd):
        self.pipe.write(cmd+"\n")

    def stomp(self,stamp):
        """
        Send an event (time=stamp) to the beat analysis
        """
        text="stomper.add_event("+str(stamp)+",1.0)"
        self._send(text)
        self._send("analysis.doit()")
        
    def _pipe_reader(self):
        while True:
           
            text=self.stdout.readline()
            if len(text) == 0:
                print " end of file "
                return
            #print ":",text
            if self.err_t == None:
                return 
                
            #print ">",text,"<"
            exec("self.zzz="+text)
            #print self.zzz
            #self.hist.append(zzz)
            self.seek_metric()
            for o in self.obsevers:
                o.notify()



    def seek_metric(self):  
            #  self.tempo=float(text)
            x_p=0.0
            t_p=0.0
            for x in self.zzz:
                if x[0] < self.t_min:
                    continue
                elif x[0]> self.t_max:
                    break
                if x[1] > x_p:
                    t_p=x[0]
            if t_p <= 0.0:
                return
                    
            self.beat_len=t_p
                
            x_p=0.0
            t_p=0.0
            
            for x in self.zzz:
                if x[0] < self.beat_len*2.5:
                    continue
                elif x[0]> self.beat_len*5.0:
                    break
                
                x_tmp=x[1]
                
                if x_tmp > x_p:
                    t_p=x[0]
                    
            if t_p <=0:
                return
                  
            self.bar_len=t_p
            
            
  
    def get_barlength(self):
        return self.bar_len

    def get_beatlength(self):
        return self.beat_len
    

    #def get_meter(self):
        
        
    def quit(self):
        print "BEAT CLIENT quitting  .... "
        if self.proc == None:
            return
        self._send("time.sleep(0.5)")
        self._send("quit()")
        
        self.pipe.close()
        #self.stdout.close()
        print " waiting for client to die"
        self.proc.wait()
        print " dead"
        self.proc = None
        print " . . . . . quitted "
        
            
        
        
      
 
if __name__ == "__main__":
     
    c=Client(debug=False)
    
   
    t1=time.time()
    while True:
        foo=raw_input('cmd (type "quit" to exit):')
    
        print foo
        if foo == "quit":
            c.quit()
            time.sleep(1.0)
            break
    
        tt=time.time()-t1
        
        c.stomp(tt)
#         text="stomper.add_event("+str(tt)+",1.0)"
#         #print text
#             
#         c.send(text)
#         c.send("analysis.doit()")
        
   
        
    print "OK I quit" 
    #c.send("quit")    