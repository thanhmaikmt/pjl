import threading
import serial,serial.tools.list_ports
import time
from const import  *

""" 
Make a stream from a whole directory of files 
"""
 
class MultiFileStream:
    
    def __init__(self,dir,file_name_client,dt=0):
    
        import glob
        self.client=file_name_client
        self.dt=dt
        self.fn_iter=glob.glob(dir+"/*.txt").__iter__()
        self.fin=None
        self.next_file()
        
    def next_file(self):
        
        print " NEXT FILE  . . ."
        if self.fin:
            self.fin.close()
     
        try:
            self.file_name=self.fn_iter.next()
            print self.file_name
            if self.client:
                self.client.notify(self.file_name)
     
        except StopIteration:
            print " No more data files"
            self.fin=None
            self.file_name=None
            raise
            
    
        if self.file_name:
            print " opening", self.file_name
            self.fin=open(self.file_name,"r")
            
            if not self.fin:
                print "oops could not open"
        else:   
            self.fin=None
        
    def readline(self):
        
        if self.dt > 0:
            time.sleep(self.dt)
            
        if self.fin == None:
            return None
        
        while True:
            line=self.fin.readline()
            if line:
                return line
            
            self.next_file()
            
            if not self.fin:
                return None
            
            
     
       
            

class EcgSource (threading.Thread):
    
    
    LIVE,LIVE_RECORD,FILE,FILE_LIVE=range(4)
    
    def __init__(self,processor,mutex,mode,data_dir):
        
        threading.Thread.__init__(self)
#         self.mode=mode
        self.fout=None
        self.mutex=mutex
        self.processor=processor
        # MUTEX for gui and data processing synschronization
  
        #  mode 0 - OFFLINE scans all test_data  recordings
        #       1- online using USB to grab realtime data from arduino + SCG shild
    
        self.Record=False
        
        serial.tools.list_ports.main()
        
        #  ---------------  SERIAL PORT FOR ECG -----------
        # WINDOWS      does this work with the leonardo? Does not report the port in the list.
        #serial_port='COM4'
        
        # MAC
        # serial_port="/dev/tty.usbmodem1421"   #  LEFT on mac air
        serial_port="/dev/tty.usbmodem1411"     #  RIGHT on mac air
                
        # ubuntu
        #ser_port = "/dev/ttyACM0"          
        
        self.fout=None
        self.Replay=False
        self.file_mode=False
        
        #self.controlller=controller
        
        #  Set up ECG input dpending on mode
        if mode == EcgSource.FILE or mode == EcgSource.FILE_LIVE:
            
            class Client:
                
                def notify(self,name):
                    global caption
                    caption=name
            
            if mode == EcgSource.FILE_LIVE:
                dt=DT
                self.Replay=False
          
            else:
                dt=0
                self.Replay=True
                         
            source=MultiFileStream(data_dir,Client(),dt)
            self.file_mode=True
            
            
        elif mode == EcgSource.LIVE or mode == EcgSource.LIVE_RECORD:
        
            if mode == EcgSource.LIVE_RECORD:
                file_name="data/"+time.strftime("%b%d_%H_%M_%S")+".txt"
                self.fout=open(file_name,"w")    
                
        
            source = serial.Serial()
            source.port=serial_port
            # wait for opening the serial connection.
            while True:    
                try:
                    source.open()
                    break
                except:
                    print " Waiting for serial connection on ",serial_port
                    time.sleep(1)
            
            print " Using USB serial input "
        
        self.source=source
       
    # Read ECG values and feed the processor
    def run(self):
       
       
     
        # Maximium value for raw ECG stream    
        fullScale=1024
        
        # dc should be half fullScale
        ref=fullScale/2.0    
            
        
        count=0
        valLast=0    #  just used to do a crude down sampling 400Hz --> 200Hz
        self.stopped=False
        
        while not self.stopped:
            
            try:
                response=self.source.readline()
            except StopIteration:
                return
#             print response
            
            if response=="":
                continue
            
            if self.fout:
                self.fout.write(response)
                
            try:
                raw=float(response)
            except:
                print "error",response
                continue
    
            # map onto a -1  to +1 range            
            val=(raw-ref)/fullScale  
            
            # crude down sampler  400 Hz --> 200 Hz
            if (count % 2) == 0:
                val=(val+valLast)*0.5
                count += 1
            else:
                valLast=val
                count +=1
                continue
       
            self.processor.process(val,self.Replay,self)
            
        print " THREAD QUITTING "
            
    def quit(self):
        
        print " ASK ECG TRHEAD TO QUIT "
        
        self.stopped=True
        
        
        # join thread to avoid hanging pythons
        self.join()
        
        print " ECG THREAD QUIT "
        
        if self.fout:
            self.fout.close()
  
    def get_caption(self):
        if self.file_mode:
            return self.source.file_name
        else:
            return " LIVE "
        
if __name__ == "__main__":

    class Client:
        
        def process(self,val,replay):
            print val
                
    ecg_src=EcgSource(Client(),threading.Lock(),mode=EcgSource.LIVE)
    
    ecg_src.start()
    
    ecg_src.join()
 
     
         