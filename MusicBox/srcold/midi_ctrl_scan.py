"""
Scan for Midi controller numbers. Launch this script from a terminal.

"""
from pyo import *
import time

pm_list_devices()
num=3                          # 3 work    5 home
# num = input("Enter your Midi interface number : ")

s = Server(duplex=0)
s.setMidiInputDevice(num)
s.boot().start()

n=Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1, add=0)

p=Print(n['pitch'],1)

print "Play with your Midi controllers..."

def pp(x): 
    print "controller number =", x



scan = CtlScan(pp, False)

scan.play()

s.gui(locals())
  
  