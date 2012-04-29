from pyo import  *
from ga import  *




serv=Server().boot()

        
	   		
	   	

#anal=Analyse()
   	
	   	#fin=open(snippet)
	   	#code=fin.read()
#execfile("examps.py")
#print locals()

def works():
    low_freqs = [midiToHz(m+7) for m in [36,43.01,48,55.01,60]]
    mid_freqs = [midiToHz(m+7) for m in [60,62,63.93,65,67.01,69,71,72]]
    high_freqs = [midiToHz(m+7) for m in [72,74,75.93,77,79.01]]
    freqs = [low_freqs,low_freqs,mid_freqs,mid_freqs,high_freqs]
    
    chx = Choice(choice=freqs, freq=[1,2,3,3,4])
    port = Port(chx, risetime=.001, falltime=.001)
    sines = SineLoop(port, feedback=[.06,.057,.033,.035,.016], mul=[.15,.15,.1,.1,.06])
    pan = SPan(sines, pan=[0, 1, .2, .8, .5]).out()
    
    serv.gui(locals())



def test():
    anal = Factory()
    loc=anal.build_from_code("examps.py")
    serv.gui(loc)

    	   	
    
def gene():
    genome = Genome()
    genome.generatorGenes.append([0])
    genome.triggerGenes.append([0])
    genome.triggerableGenes.append([0,0,0])
    factory = Factory()
    p=factory.build(genome)
    p.play()


test()