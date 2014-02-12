import pyo

s=pyo.Server().boot()


def pp():
    print "hello"
    
 
trig=pyo.Sig(1)

tf=pyo.TrigFunc(trig,pp)


s.gui(locals())