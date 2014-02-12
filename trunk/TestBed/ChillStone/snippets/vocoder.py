from pyo import *
s = Server().boot()
s.start()
sf = SfPlayer('./samples/nessaAllTrim.wav', loop=True)

freq=100+Noise(10)
ex = Blit(freq=freq)


voc = Vocoder(sf, ex, freq=80, spread=1.2, q=20, slope=0.5)

out = voc.mix(2).out()

s.gui(locals())