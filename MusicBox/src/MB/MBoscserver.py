"""
Setup an OSC server
use the supplied cliet to pipe messages to the main application.

"""


import OSC
import time, threading
import socket
import sys
import traceback
import MBsetup as MB


class Server:
    
    debug=False
    
    def __init__(self,addr,map,recorder=None):
        
        
                 
        # tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)

        receive_address = addr
         
        
        # OSC Server. there are three different types of server. 
        self.s = OSC.OSCServer(receive_address) # basic
        ##s = OSC.ThreadingOSCServer(receive_address) # threading
        ##s = OSC.ForkingOSCServer(receive_address) # forking
        
        
        # this registers a 'default' handler (for unmatched messages), 
        # an /'error' handler, an '/info' handler.
        # And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
        self.s.addDefaultHandlers()
        self.s.addMsgHandler("default", self.default_handler) # adding our function
        self.map=map
        self.recorder=recorder
        
    # define a message-handler function for the server to call.
    def default_handler(self,addr, tags, stuff, source):
        try:
            self.handle(addr,stuff,self.recorder)
        except: 
            print "Client error handling "
            print "---"
            print "received new osc msg from %s" % OSC.getUrlStr(source)
            print "with addr : %s" % addr
            print "typetags %s" % tags
            print "data %s" % stuff
            print "---"
            print "Unexpected error:", sys.exc_info()[0]
            traceback.print_exc()
  
    def run(self):
        # just checking which handlers we have added
        print "Registered Callback-functions are :"
        for addr in self.s.getOSCAddressSpace():
            print addr
        
        
        # Start OSCServer
        print "\nStarting OSCServer. Use ctrl-C to quit."
        self.st = threading.Thread( target = self.s.serve_forever )
        self.st.start()
    

    def quit(self):  
        
        self.s.close()
        print "Waiting for Server-thread to finish"
        
        self.st.join() ##!!!
        print "Done"


            
    def handle(self,addr,data,recorder):
            
            # process raw OSC messages
            # delegate next handling using toks[2] of the OSC string
            # the handler is resolved using self.map
            #print addr,data
            
            if recorder != None:
                recorder.record(addr,data)
      
            if self.map==None:
                print addr,data
                return
            
            toks=addr.split('/')
            
            if len(toks) < 3:
                return
            
            # toks[2] of the OSC is used to chose reciever.
            func=self.map.get(toks[2])
            
            if func != None:   # pass end of OSC message to the func
                func(toks[3:],data)
            else:
                if Server.debug:
                    print " No musicbox handler for:", addr
  
    
if __name__ == "__main__":
   
            
             
    addr=MB.get_osc_ip()
    server=Server(addr,None)        
    server.run()

    xx = raw_input(" Hit CR TO QUIT")

    print "\nClosing OSCServer."
    server.stop()
            
            