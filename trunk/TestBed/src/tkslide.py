from Tkinter import *

master = Tk()
frame=Frame(master)

w = Scale(frame, label="SLider",from_=0, to=100)
w.pack()

w = Scale(frame, label="SLider",from_=0, to=200, orient=HORIZONTAL)
w.pack()
frame.pack()

mainloop()