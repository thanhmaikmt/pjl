
import random 

from Tkinter import *


xMax=600
yMax=600
marg=20
d_size=10


def draw_consumers(consumers,w):
    for c in consumers:
        w.create_rectangle(c.x, c.y, c.x+c.size, c.y+c.size, fill="blue")


def draw_generators(generators,w):
    for g in generators:
        w.create_oval(g.x, g.y, g.x+g.size, g.y+g.size, fill="red")

def draw_lines(lines,w):
    for l in lines:   
        w.create_line(l.a.x, l.a.y, l.b.x, l.b.y, fill="white")
        

    

def random_point():
    x=marg+random.random()*(xMax-2*marg)
    y=marg+random.random()*(yMax-2*marg)
    return x,y


