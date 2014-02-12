from pyo import *

s =Server(audio='coreaudio').boot().start()

sin=Sine(440,mul=.2).out()

s.gui()