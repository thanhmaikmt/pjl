from pyo import *


s  = Server().boot()
Fs = s.getSamplingRate()

s.start()

src=Input(0)


buff_time_in_sec=100
delay=1.0

# IN -> Matrix



# Length of grains in samples
SIZE   = int(Fs*buff_time_in_sec)
STAGES = 1

# Number of successive grains kept in memory




period = SIZE /Fs 

matrix = NewMatrix(SIZE, STAGES)

# src = SfPlayer('../snds/baseballmajeur_m.aif', speed=1, loop=True, mul=.3)
m_rec = MatrixRecLoop(src, matrix)

x = Linseg([(0,0), (period,1)],loop=True)
x.play(delay=delay)
y=Sig(0)

out = MatrixPointer(matrix, x, y,1.0).mix(2).out()


#src1.out()

s.gui(locals())

