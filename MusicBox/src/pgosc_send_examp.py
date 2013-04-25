"""
Make a OSC controller using pygame
"""



import pgdriver
import OSC
import socket


class Client:


    def __init__(self):
        pass
    
    def handle(self,event):
        print event
        msg=OSC.OSCMessage("/1/rotary1",[5,6,7,8])
        osc_client.send(msg)


for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
      if not ip.startswith("127."):
          break
   
#ip="127.0.0.1"   
addr=(ip,7110)
print addr


if __name__ == "__main__":
    
    # define a message-handler function for the server to call.
    def default_handler(addr, tags, stuff, source):
            print "---"
            print "received new osc msg from %s" % OSC.getUrlStr(source)
            print "with addr : %s" % addr
            print "typetags %s" % tags
            print "data %s" % stuff
            print "---"
       
    s = OSC.OSCServer(addr) # basic
    s.addDefaultHandlers()
    s.addMsgHandler("default", default_handler) # adding our function
    import threading
    st = threading.Thread( target = s.serve_forever )
    st.start()
         
     
        

osc_client=OSC.OSCClient()
osc_client.connect(addr)

pe=pgdriver.PGDriver(Client()) 
pe.run()


      