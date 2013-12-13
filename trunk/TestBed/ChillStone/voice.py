#!/usr/bin/env python
# encoding: utf-8
"""
Hand-written pulsar synthesis.

"""
from pyo import *
import random
import inspect

srate=44100

freqMap=SLMap(20., srate/2., 'log', 'freq', 100.0)
qMap=SLMap(0.1, 500., 'log', 'q', 1.0)
mulMap=SLMap(-2.0, 2, 'lin', 'mul', 1.0)
filtMaps = [freqMap, qMap, mulMap]



class Gene:
    def __str__(self):
        return inspect.getmembers(self).__str__()

def myrand(min,max):
    fact=random.random()
    val=min+(max-min)*fact
    return val

class GeneList:
    
    def __init__(self,n):
        self.list = []
        for i in range(n):
            self.list.append(randomGene())


        
def randomGene():
    gene=Gene()
    gene.freq=myrand(10,srate/2)
    gene.type=int(myrand(0,5))
    gene.q=myrand(0,500)
    gene.mul=myrand(-1,1)  
    return gene

class Choir:

    def __init__(self,input,genes):
        self.voices=[]
        for gene in genes.list:
            self.voices.append(Voice(input,gene))
    
    def rebuild(self,genes):
        
        for gene,voice in zip(genes.list,self.voices):
            voice.rebuild(gene)

class Voice:
    
    def __init__(self,input,gene):
        #print " VELO"
        #print gene
        self.filt=Biquadx(input, freq=gene.freq,type=gene.type, q=gene.q,mul=gene.mul)
        # print " VELO 2"    
        
        self.x=self.filt*srate

        self.compress=Clip(self.x)
       
        self.pan=SPan(self.compress).out()
          
        self.filt.ctrl(filtMaps)
        self.compress.ctrl()

    def rebuild(self,gene):
        print gene
        self.filt.freq=gene.freq
        self.filt.type=gene.type
        self.filt.q=gene.q
        self.mul=gene.mul

if __name__ == "__main__":
    input = Metro(1)


    n=1
    print "Hello"
    genes=GeneList(n)

    print "Hello 2"
    choir=Choir(input,genes)

    print "Hello"
    def x():
        genes=GeneList(n)
        choir.rebuild(genes)


    input.play(delay=.5)
    s.gui(locals())