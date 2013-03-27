import subprocess,inspect
import atexit,time,Queue,threading

class Client:
 
    
    def __init__(self,debug=False):
        self.debug=debug
        self.proc=None
        
        if  not debug:
            self.proc=subprocess.Popen(["python -i beatserver.py"], shell=True,
                                       stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE)
            
            
#            ,
#                                       stderr=subprocess.STDOUT,
#                                       stdout=        self.pipe.subprocess.PIPE)
            
            self.pipe   = self.proc.stdin
            self.stdout = self.proc.stdout
            #print self.proc.pid
            
                
               

    def send(self,cmd):
        self.pipe.write(cmd+"\n")


  
         
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
        text="stomper.add_event("+str(tt)+",1.0)"
        print text
            
        c.send(text)
        c.send("analysis.doit()")
        
    print "OK I quit" 
    #c.send("quit")    