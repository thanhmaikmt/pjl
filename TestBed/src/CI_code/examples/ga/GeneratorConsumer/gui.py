
import random 

from Tkinter import *
import world


xMax=600
yMax=600
marg=20
d_size=10


def draw_consumers(consumers,w):
    for c in consumers:
        sz=1+c.demand*d_size/world.Consumer.maxDemand
        w.create_rectangle(c.x-sz, c.y-sz, c.x+sz, c.y+sz, fill="blue")


def draw_generators(generators,w):
    for g in generators:
        if g.used:
            sz=1+g.capacity*d_size/world.Generator.maxCapacity
            w.create_oval(g.x-sz, g.y-sz, g.x+sz, g.y+sz, fill="red")

def draw_lines(lines,w):
    for l in lines:
        if l.capacity > 0:   
            w.create_line(l.a.x, l.a.y, l.b.x, l.b.y, fill="white")


def draw_world(world,canvas,anno):
    canvas.delete(ALL)
    draw_lines(world.lines,canvas) 
    draw_generators(world.generators,canvas) 
    draw_consumers(world.consumers,canvas) 
    canvas.create_text(3,yMax,text=anno,anchor=NW)
    
def draw_world_init(w,canvas):
    canvas.delete(ALL)
    for c in w.consumers:
        sz=1+c.demand*d_size/world.Consumer.maxDemand
        canvas.create_rectangle(c.x-sz, c.y-sz, c.x+sz, c.y+sz, fill="blue")

    for g in w.generators:
            sz=1+g.capacity*d_size/world.Generator.maxCapacity
            canvas.create_oval(g.x-sz, g.y-sz, g.x+sz, g.y+sz, fill="red")
   
    
        

def random_point():
    x=marg+random.random()*(xMax-2*marg)
    y=marg+random.random()*(yMax-2*marg)
    return x,y


