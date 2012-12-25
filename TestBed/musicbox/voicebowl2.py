from pyo import *
s = Server().boot()
s.start()
#t = CurveTable([(0,0.0),(512,0.97),(1024,-0.94),(1536,0.0),(8192,0.0000)])



#t.graph()

src=Input(0)

src.out()

#rnd = Randi(min=.97, max=1.03, freq=[.143,.2,.165,.111])



#src.out()




#rnd2 = Randi(min=.5, max=1.0, freq=[.13,.22,.155,.171])
#det = Sig(0.75, mul=rnd2)
#rnd3 = Randi(min=.95, max=1.05, freq=[.145,.2002,.1055,.071])
fx = AllpassWG([src,src], freq=[100,210,500], feed=1., detune=0.5, mul=.25)

fx.out()

s.gui(locals())

