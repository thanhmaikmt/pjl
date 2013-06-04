import subprocess,inspect
import atexit,time,Queue,threading

"""
Users side of the beat detection system.
The client sends beats to the server
"""

class Client:
 
    
    def __init__(self,debug=False):
        self.debug=debug
        self.proc=None
        
        if  not debug:
            self.proc=subprocess.Popen(["python -i ../beat/beatserver.py -g"], shell=True,
                                       stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE)
            
            
#            ,
#                                       stderr=subprocess.STDOUT,
#                                       stdout=        self.pipe.subprocess.PIPE)
            
            self.pipe   = self.proc.stdin
            self.stdout = self.proc.stdout
            #print self.proc.pid
            
    
            self.err_t=threading.Thread(target=self.pipe_reader)
           
            self.q=Queue.Queue()
            self.err_t.start()
            self.tempo=-1
               

    def send(self,cmd):
        self.pipe.write(cmd+"\n")

    def stomp(self,stamp):
        """
        Send an event (time=stamp) to the beat analysis
        """
        text="stomper.add_event("+str(stamp)+",1.0)"
        self.send(text)
        self.send("analysis.doit()")
        
    def pipe_reader(self):
        while True:
           
            text=self.stdout.readline()
            if len(text) == 0:
                print " end of file "
                return
            #print ":",text
            if self.err_t == None:
                return 
            
            print ">",text,"<"
            self.tempo=float(text)
         
    def quit(self):
        print "quitting  .... "
        if self.proc == None:
            return
        self.send("time.sleep(0.5)")
        self.send("quit()")
        
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