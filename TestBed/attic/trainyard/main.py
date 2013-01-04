import world
from pool import *
from yardurl import *
from Tkinter import *

class Context:
    pass



class Run:
    

    def __init__(self):
     
        self.init_gui()
        self.load_puzzle()
        
        
    def init_gui(self):        
        
        
        
        master = Tk()
        self.frame=Frame(master)
        self.frame.pack()
        c=0
        
        
#        b = Button(self.frame, text="RANDOM WORLD", fg="black", command=self.init_world)
#        b.grid(row=0,column=c)
#        c+=1
#        b = Button(self.frame, text="RESET GA", fg="black", command=self.ga_init)
#        b.grid(row=0,column=c)
#        c+=1


        b = Button(self.frame, text="LOAD PUZZLE",fg="black", command=self.random_gene)
        b.grid(row=0,column=c)
        c+=1

        b = Button(self.frame, text="RANDOM GENE", fg="black", command=self.random_gene)
        b.grid(row=0,column=c)
        c+=1
        
        #b = Button(self.frame, text="BUILD FROM GENE", fg="black", command=self.build_from_gene)
        #b.grid(row=0,column=c)
        #c+=1
        
        b = Button(self.frame, text="STEP SIM", fg="black", command=self.step_sim)
        b.grid(row=0,column=c)
        c+=1
        
        b = Button(self.frame, text="RESET SIM", fg="black", command=self.reset_sim)
        b.grid(row=0,column=c)

        c+=1
        
        b = Button(self.frame, text="RUN SIM", fg="black", command=self.run_sim)
        b.grid(row=0,column=c)

        c+=1
        
        
        
        
#        b = Button(self.frame, text="RUN (GA)", fg="black", command=self.run_ga)
#        b.grid(row=0,column=c)
#        c+=1
#        b = Button(self.frame, text="RUN (RANDOM)", fg="black", command=self.run_random)
#        b.grid(row=0,column=c)
#        c+=1
#        b = Button(self.frame, text="STOP", fg="black", command=self.stop)
#        b.grid(row=0,column=c)
#        c+=1
#        self.bb= IntVar()
#        b = Checkbutton(self.frame, text="BREED", fg="black", variable=self.bb,command=self.breed_func)
#        b.grid(row=0,column=c)
        #b.pack()
      
 
        self.canvas = Canvas(self.frame, width=600, height=600)
        self.canvas.grid(row=1,columnspan=c)
        
        self.context=Context()
        self.context.canvas=self.canvas
        self.context.h=60
        self.context.x=10
        self.context.y=10
        
        #w.draw(self.context)                      
    
    
    def load_puzzle(self):
        # Get something to work with.
        # Good ones
        puzzle='2dPQE'

        url = urllib.urlopen("http://trainyard.ca/"+puzzle)
        self.world,self.solution_gene=worldFromUrl(url)
        self.world.rebuild_from_gene(self.solution_gene)
        self.redraw()
        
        
    def init_ga(self):
         
        self.pool=Pool(self.world)
        
        
    def stop(self):
        self.running=False
   
    
    def run_ga(self):
        
        while True:
            gene=self.pool.create()
            
   

    def step_random(self):
        g=self.world.random_gene()
        fit=self.world.evaluate(g)
        
        print "Fitness =",fit
        
        
    def random_gene(self):
        gene=self.world.random_gene()
        self.world.rebuild_from_gene(gene)
        self.canvas.delete(ALL)
        self.world.draw(self.context)   
              
    def step_sim(self):       
        self.world.step()
        self.redraw()
        
    def redraw(self):  
        self.canvas.delete(ALL)
        self.world.draw(self.context)   


    def reset_sim(self):
        self.world.reset()
        self.redraw()  
        
        
    def run_sim(self):
        self.reset_sim()
        while not self.world.done:
            self.step_sim()
             
           

  
      

# Silly        
# puzzle='S3a42'
    

#puzzle='2ey6e'   # OK
#puzzle='2eyfR'   # OK
#puzzle='2esWR'   # OK
puzzle='2ezM4'

#puzzle='2exr6'


puzzle='S2B8q'

puzzle='2ek3R'
puzzle='S3a4M'
puzzle='S3a4N'
puzzle='S3a4S'




run=Run()

mainloop() 
