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
 
    
    def __init__(self,debug=False):
        
        self.debug=debug
        self.proc=None
        
        if  not debug:
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
            exec("zzz="+text)
            print zzz
            #  self.tempo=float(text)
        
    def get_interval(self):
        return self.tempo 
  
    def get_bpm(self):
        return 60.0/self.tempo 
        
    def quit(self):
        print "quitting  .... "
        if self.proc == None:
            return
        self.send("time.sleep(0.5)")
        self.send("quit()")
        
        self.pipe.close()/usr/local/bin/python
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