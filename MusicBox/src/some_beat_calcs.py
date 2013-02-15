bpm=60.0
pulse_per_beat=4.0
dt=60.0/bpm/pulse_per_beat

print "dt=",dt


from  numpy import *
import time


dt=1
n=1000
x=zeros(n)

for i in range(len(x)):
    if i % 100 == 0:
        x[i]=1.0

start = time.time()


y=correlate(x,x,mode='full')

end =time.time()

y=y[n-1:]

print end-start


from  matplotlib.pyplot import *


t=arange(0,len(y),1)#

ion()
fig=figure()
ax = fig.add_subplot(111)
line1, = ax.plot(t, x, 'r-') 
ylim([0,1])
print "Hello"
ii=10

while True:
    #print "Hello"
    time.sleep(0.5)
    ii=(ii+1)%100+1
    x[:]=0
    for i in range(len(x)):
        if i % ii == 0:
            x[i]=1.0
            
    y=correlate(x,x,mode='full')
    y*=1./n
    line1.set_ydata(y[n-1:])
    fig.canvas.draw()







