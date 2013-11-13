from pyo import *

s = Server(buffersize=64).boot()
s.start()

a = Sine(mul=0.01, freq=1000).out()

time.sleep(0.1)

for i in range(0,10000):
        a.freq=i/10
        time.sleep(0.0001)




s.gui(locals())