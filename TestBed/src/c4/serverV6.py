#!/usr/bin/env python
# Game server

# You can change the port and logDir if you wish
port=4005

import os

# directory to log stuff
myHomeDir=os.getcwd()
logDir=os.path.join(myHomeDir,"c4gamelog")


#
# Note that with sockets the data in a send may be buffered so a recieve can comprise several 
# sends (this occurs when the sends happen in quick succession). 
# To make "packets" all messages are sent with "\n" separators.
# 


import socket
import threading
import sys
import Queue
import os
import time


# set the default host name and port.

host=""
if len(sys.argv) >= 2:
    port=int(sys.argv[2])


# open the socket.
# some people claim using SO_REUSEADDR helps with sock reallocation
# ( e.g. error message claims socket is in use)
# I still get problems when using eclipse but hopefully in production it should be OK.
    
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((host, port))
server_socket.listen(5)

print "TCPServer Waiting for client on port:"+str(port)

# Each client has a connection
# use dictionary to map user names onto it's connection
connections={}


# keep a log of all the games played in the following directory
# create it if need be.
# abort if unable to create.
# TODO check for write permission


if not os.path.exists(logDir):
    print logDir," Does not exist trying to create it."
    try:
        os.makedirs(logDir)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        raise
    except OSError as e:
        print "OS error({0}): {1}".format(e.errno, e.strerror)
        raise
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    
    if os.path.exists(logDir):
        print "Create log directory :",logDir
    else:
        print "Failed to create ",logDir," and did not catch any error. This should not happen  . . .  aborting !!"
        sys.exit()

else:
    print "Using existing log directory :",logDir
    
    
    
    
    
# not used yet
LOG_LEVEL=1

# place holder for a better error reporting scheme
def server_error(str1):
    print str1

# class to hold information about a game
# only exists whilst a game is in progress
# use for communication and logging of games

class Game:
    
    def __init__(self,challenger,opo,tag):
        """
        Create the object with the 2 players.
        """
        self.challenger=challenger
        self.opo=opo
        
        cnt=0
                
        # create the basic name
        base_name=logDir+"/"+challenger.name+"_"+opo.name+"_"+tag+"_"
        
        while True:   # add a unique number to distinguish games
            file_name=base_name+str(cnt)
            if not os.path.exists(file_name):
                self.log=open(file_name,"w")
                break
            cnt +=1
            
        #flags to be set when each player leaves game
        self.challengerX=False
        self.opoX=False    
        
    def record_move(self,who,data):
        
        str1=who.name+":"+data+"\n"
        self.log.write(str1)
        self.log.flush()
        #if self.opoX or self.challengerX:
        #    self.end_game() 
           
    def record_end(self,who,data):
       
        if who == self.challenger:
            self.challengerX=True
        elif who == self.opo:
            self.opoX=True
        else:
            server_error(" Ooops in game.record_end("+who.name+","+data+")")
            
        str1=who.name+":"+data+"\n"
        self.log.write(str1)
        self.log.flush()
        
        if self.opoX and self.challengerX:
            self.end_game()

            
    def end_game(self):
            self.log.close()
            if LOG_LEVEL>0:
                print "Game over "+ self.challenger.name+" " + self.opo.name
            self.challenger=None
            self.opo=None
       
    def opo_of(self,who):
        if who == self.challenger:
            return self.opo
        elif who == self.opo:
            return self.challenger
        else:
            server_error(" game.opo_of("+who.name+") attempt to find opo of game you are not playing!")
            return None
        

class Connection(threading.Thread):
    """
    Each player has a connection to talk to the server
    Each connection has it's own thread.
    """
    
    def __init__(self,client_socket,address):
        threading.Thread.__init__(self)
        self.client_socket=client_socket
        self.address=address
             
        self.rque=Queue.Queue()
        self.buff=""
        self.game=None
        self.name=self.getName()
        self.start()    
        
     
    def myopo(self):
        if self.game==None:
            return None
        
        return self.game.opo_of(self)
        
    
    def send(self,data):
        self.client_socket.send(data+"\n")
        if LOG_LEVEL>0:
            print self.name+">"+data
        
        
    def recieve(self):
        """
        Returns the next line of the input queue.
        If need be fills the input buffer with a line.
        """
        while(self.rque.empty()):
            self.replenish()
            
        return self.rque.get()
            
    def replenish(self):
        """
        Read data from the client socket and put this in the input queue
        until a "\n" is encountered.
        """
        
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
            server_error(self.name + " Exception in receive ! ")
            self.rque.put("q")
    
    def close(self):
        print self.name+": Closing "+" ... "          
          
        if client_socket != None:   
            self.client_socket.close()
            
        self.client_socket=None;
        
        if self.myopo() != None:
            if self.myopo().myopo() != None:
                try:
                    self.myopo().sendIfOpen("a "+self.name)
                except:
                    pass
                #self.opo.opo=None
                
    #    if self.game != None:
     #       self.game.leave(self)
        
        if connections.has_key(self.name):
            del connections[self.name]
           
        print self.name+": closed"            
        
  
    def sendIfOpen(self,data):
        if self.client_socket==None:
            return
        
        try:
            self.send(data)
        except:
            print " oops exception in sendIfOpen "
        
    def run(self):
 
        print self.name+": Accepting connection from ", address
        
        while True:       
            name=self.recieve()  
            c=connections.get(name)
            if c == None:
                self.sendIfOpen("! OK ")
                break
            else:
                self.sendIfOpen("? Sorry the name "+ name + " is being used by another player try another name ")
                self.close()
                return
                
        self.name=name
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
                for key,c in connections.items():
                    if c.game == None:
                        self.sendIfOpen("+"+key)
                    else:
                        opo_name=c.game.opo_of(key)
                        if opo_name != None:
                            self.sendIfOpen("+"+key+"  "+opo_name)
                        else:
                            self.sendIfOpen("+"+key)
                            
                    
                self.send("$")
     
            elif data[0] == 'm':
                # 
                no_opo=False
                cnt =0
                while self.myopo() == None:
                        
                    time.sleep(.1)
                    cnt+=1
                    if cnt > 10:
                        server_error(self.name+": Received a move but opponent not registered in my game ")
                        no_opo=True
                        break
                        
                if not no_opo:
                    self.game.record_move(self,data)
                    opo=self.myopo();
                    if opo != None:
                        opo.sendIfOpen(data) 
               
                    
            elif data[0] == 'g' or data[0] == 'G' and self.myopo() == None:
                
                # challenge to play. Must send a ! (OK)  or ?  error
                if self.myopo() != None:
                    self.send("? you are already playing "+self.myopo().name)
                else:
                    opo_name=data[2:].strip()
                    opo=connections.get(opo_name)
                    
                    if opo == None:
                        self.sendIfOpen("? "+ opo_name + " is not playing.")    
                    elif opo == self:
                        self.sendIfOpen("? sorry you can not play against your self ")
                    else:
                        if opo.game == None:
                            self.game=Game(self,opo,data[0])
                            opo.game=self.game;
                            self.sendIfOpen("! "+ opo_name + " accepted")      # important to send acceptance before invite    
                            self.myopo().sendIfOpen(data[0]+" "+self.name)     # (otherwise we can get a response from opo before acknowledgement)
                            
                        else:
                            self.sendIfOpen("? "+ opo.name+ " is already playing "+opo.myopo().name)
                    
            elif data[0] == 'w' or data[0] == 'l' or data[0] == 'd' or data[0] == 'a':


               
                if self.game != None: 
                    
                    self.myopo().sendIfOpen("a")     
             
                    self.game.record_end(self,data)
                    self.game=None
                    

                    
                                
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
          
       