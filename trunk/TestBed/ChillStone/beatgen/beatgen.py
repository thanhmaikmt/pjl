from ga import *

import os
import glob

class SampleGene(Gene):
    """
     
    """
    
    maps=None
            
    def __init__(self,pheno=None,**kwargs):
        Gene.__init__(self,pheno,**kwargs)

        if pheno != None:
            self.pheno.samples.append(self)    
 
 
    def randomize(self):
        self.data.sample_id=self.pheno.sample_id
        self.data.trigger_id=self.pheno.trigger_id
       

    def build(self):
        
        infile=self.pheno.sample_files[self.data.sample_id] 
        print "current file is: " + infile

        self._table = pyo.SndTable(path=infile)
        dur = self._table.getDur()
        trig=self.pheno.triggers[self.data.trigger_id].trigger
        self._trigTable = pyo.TrigEnv(trig, table=self._table).out()
    
    def kill(self):
        self._trigTable.stop()
        if do_del:   
            del self._trigTable

    
    
class PhenoSamplePlayer:
    
    def __init__(self):
        self.genes=GeneList()
        self.triggers=GeneList()  
        self.samples=GeneList()
        self.sample_files=[]
        
         
    def randomize(self,**kwargs):
        gene=BeatGene(self)
        gene.randomize()
        gene.setAttr('bpm',20,False)
        self.trig_id=0
      
        for filnam in glob.glob('../samples/drums/*.wav'):
            self.sample_files.append(filnam) 
            
        
        for _ in range(kwargs.get('n_offbeat',6)):
            gene=OffBeatGene(self)
            
            self.trigger_id=random.randint(0,len(self.triggers)-1)
            gene.randomize()   
            
            self.sample_id =random.randint(0,len(self.sample_files)-1)
            
            gene=SampleGene(self)  
            gene.randomize()
            
            
        
        
    def build(self):
        """
        build the nome.
        """
        
        for g in self.genes:
            g.build()
            
        self.built=True
        
    def play(self):
        self.triggers[0].play()


def set_bpm(val):
   pheno.triggers[0].setAttr('bpm',val,True)


def randomize():
    for g in pheno.triggers:
        g.setAttr('pos',random.random(),True)
    
if __name__ == "__main__":
    
    s=pyo.Server(sr=srate,duplex=0).boot()
    s.verbosity=15
    
    pheno=None

    
    def reco():
        
        global pheno
        if pheno != None:
            pheno.kill()
            time.sleep(0.2)
            
        pheno=PhenoSamplePlayer()
        pheno.randomize()
        pheno.build()
    
        #print "Pheno \n",pheno1

        pheno.play()
    
    
        
    
    reco()     
    s.gui(locals())
