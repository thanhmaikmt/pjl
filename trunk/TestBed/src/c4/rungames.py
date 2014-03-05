from subprocess import Popen, PIPE, STDOUT,call

import os

import time

path="c:\\pauls\\C4Progs\\"  # insert the path to the directory of interest

exe=path+"idoit.exe"





dirList=os.listdir(path)
for fname in dirList:
    print fname

p1=call(["c:\\pauls\\C4Progs\\idiot.exe","rdoit1"]) 

time.sleep(1)

p2=call(["c:\\pauls\\C4Progs\\idiot.exe","rdoit2","rdoit1"]) 


#time.sleep(200)