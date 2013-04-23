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
   
ip="127.0.0.1"   
addr=(ip,7110)
print addr


if __name__ == "__main__":
        s = OSC.OSCServer(addr) # basic
        
        

osc_client=OSC.OSCClient()
osc_client.connect(addr)



pe=pgdriver.PGDriver(Client()) 
pe.run()


      