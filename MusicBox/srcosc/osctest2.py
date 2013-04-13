
from OSC import OSCServer,OSCClient, OSCMessage
import sys
from time import sleep
import types



server = OSCServer( ("0.0.0.0", 8000) )
client = OSCClient()
client.connect( ("192.168.0.2", 7110) )

def handle_timeout(self):
    print ("Timeout")

server.handle_timeout = types.MethodType(handle_timeout, server)



while True:
    server.handle_request()

server.close()
