from pyo import *

s=Server().boot()


m=Metro(10)

p2=Print(m,method=1)

c=Count(m,min=0,max=10)


p=Print(c,method=1)


m.play()

s.gui(locals())