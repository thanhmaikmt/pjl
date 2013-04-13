
from OSC import *

if __name__ =="__main__":
    
        listen_address="192.168.0.2"
        port=7110
        c = OSCClient()
        c.connect(listen_address)    # connect back to our OSCServer

        s = ThreadingOSCServer(listen_address, c, return_port=listen_address[1])
        c = OSCClient()
        c.connect(listen_address)    # connect back to our OSCServer
