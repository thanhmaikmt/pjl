
""" receiving OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation
"""


import OSC
import time, threading
import socket
import sys
import traceback

class OSCDriver:
    def __init__(self,client):
        
        
        
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
             if not ip.startswith("127."):
                 break
             
             
        print ip
             
             
    
        # tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
#        receive_address = '127.0.0.1', 7110
#        receive_address = '192.168.0.8', 7110
#        receive_address = '192.168.43.96', 7110
#        receive_address = '169.254.250.186', 7110
        receive_address = ip, 7110
        
        
        
        
        # OSC Server. there are three different types of server. 
        self.s = OSC.OSCServer(receive_address) # basic
        ##s = OSC.ThreadingOSCServer(receive_address) # threading
        ##s = OSC.ForkingOSCServer(receive_address) # forking
        
        
        
        # this registers a 'default' handler (for unmatched messages), 
        # an /'error' handler, an '/info' handler.
        # And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
        self.s.addDefaultHandlers()
        self.client=client
        self.s.addMsgHandler("default", self.default_handler) # adding our function
         
    
    # define a message-handler function for the server to call.
    def default_handler(self,addr, tags, stuff, source):
        try:
            self.client.handle(addr,stuff)
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
    

    def stop(self):  
        
        self.s.close()
        print "Waiting for Server-thread to finish"
        
        self.st.join() ##!!!
        print "Done"

if __name__ == "__main__":
    class Client:
        
        def handle(self,addr,data):
            print addr,data
            
            
            
    server=OSCserver(Client())        
    server.run()

    xx = raw_input(" Hit CR TO QUIT")

    print "\nClosing OSCServer."
    server.stop()
            
            