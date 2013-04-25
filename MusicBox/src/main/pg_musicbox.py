import pgdriver
import pygame 
import OSC
import MB

class Client:
    
    
    def __init__(self):
        pass
    
    
    def handle(self,event):
        if event.type == pygame.KEYUP:
            print "up"
            msg=OSC.OSCMessage("/1/melody/1",[0.0])
            osc_client.send(msg)

        elif event.type == pygame.KEYDOWN:
            print "down"
            msg=OSC.OSCMessage("/1/melody/1",[1.0])
            osc_client.send(msg)

            
        
        
        
addr=MB.get_osc_ip()

print "using ip", addr
osc_client=OSC.OSCClient()
osc_client.connect(addr)
       
pe=pgdriver.PGDriver(Client()) 
pe.run()
pe.stop()
       