

# TCP server example
import socket
import threading
#import port
import sys
import Queue

if len(sys.argv) >= 2:
    port=int(sys.argv[2])
    host=sys.argv[2]
else:
    port=5000
    host=""    
    
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#name= socket.gethostname() 
#print "hostname=",name
server_socket.bind((host, port))
server_socket.listen(5)

print "TCPServer Waiting for client on port "+str(port)

connections={}


class Connection(threading.Thread):
    
    
    def __init__(self,client_socket,address):
        threading.Thread.__init__(self)
        self.client_socket=client_socket
        self.address=address
        self.opo=None
           
        self.rque=Queue.Queue()
        self.buff=""
        self.start()    
        
     
    def send(self,data):
        self.client_socket.send(data+"\n")
        print self.name+">"+data
        
        
    def recieve(self):
        
        while(self.rque.empty()):
            ret=self.replenish()
            
        return self.rque.get()
            
    def replenish(self):
        
        
        try:
            data = self.client_socket.recv(512)
            #print "!"+data+"!"
                
            if len(data) == 0:
                #print " len(data) == 0 in recieve "
                self.rque.put("q")
                return
            
            for c in data:
                if c == '\n':
                    mess=self.buff.strip()
                    if len(mess) > 0:
                        self.rque.put(mess)
                    self.buff=""
                else:
                    self.buff += c
                     
                    
        except:
            print self.name + " Exception in receive ! "
            self.rque.put("q")
    
    def close(self):
        print " Closing "+self.name+" ... ",          
             
        self.client_socket.close()
        
        if self.opo != None:
            if self.opo.opo != None:
                self.opo.send("a "+self.name)
                self.opo.opo=None
        
        del connections[self.name]
           
        print " closed"            
        
  
    def run(self):
 
        print " Accepting connection from ", address," ... ",       
        self.name=self.recieve()   
        connections[self.name]=self
        print self.name
        
        # print connections
        # loops until connection is broke or we recieve a 'Q' or 'q'
        
        while True:
            
          
            data=self.recieve()
            print self.name+ "<"+data
             
            
            if len(data) == 0  or data[0] == 'Q' or data[0] == 'q':   
                self.close()
                return
            
            elif data[0] == 'L':
                #print "listing"
                for key in connections.keys():
                    self.send("+"+key)
                    
                self.send("$")
     
            elif data[0] == 'm' and self.opo != None:
                self.opo.send(data) 
                    
            elif data[0] == 'g' or data[0] == 'G' and self.opo == None:
                if self.opo != None:
                    self.send("? you are already playing "+self.opo.name+" ?")
                else:
                    opo_name=data[2:].strip()
                    opo=connections.get(opo_name)
                    
                    if opo == None:
                        self.send("? "+ opo_name + " is not playing ?")    
                    else:
                        if opo.opo == None:
                            self.opo=opo
                            self.opo.send(data[0]+" "+self.name)
                            opo.opo=self
                          
                        else:
                            self.send("? "+ opo.name+ " is already playing "+opo.opo.name+" ?")
                    
            elif data[0] == 'w' or data[0] == 'l' or data[0] == 'd':
                
                if self.opo != None:
                    #self.opo.send(data[0])
                    self.opo.opo=None
                    self.opo=None
                    
                else:
                    self.send("! you are not playing a game !")


            
# Keyboard Interrupt handler and cleanup routine
def cleanup(*args):
    print 'Exiting'
 
    global server_socket
 
    # Close the server socket
    server_socket.close()
    server_socket = None
 
    # Wait for all threads
    for _,c in connections.items():
        c.join()
 
    sys.exit(0)


import signal 

# Catch some signals
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)



                    
while 1:
    client_socket, address = server_socket.accept()
 
    Connection(client_socket,address)
       
cleanup()