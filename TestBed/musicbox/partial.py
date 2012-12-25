from pyo import *
s = Server().boot()


import math
    
    
    
class PartialOsc:
    
    
    def __init__(self,part,sr,size):
            
        init_phase=part.initialPhase()
        
        # pyo want phase as a number between 0 - 1
        init_phase=init_phase/math.pi/2.0
        
        if init_phase < 0.0:
            init_phase+=1.0
            
        assert init_phase >= 0.0 and init_phase < 1.0
            
    
        ampNoiseList=[(0,0)]
        ampToneList=[(0,0)]
        freqList=[(0,0)]
        
        cnt=0
        fade=.001
        
        for bp in part:
            t_sec=bp.time()
        
            f=bp.frequency()    
            a=bp.amplitude()
            bw=bp.bandwidth()
        
            if cnt == 0:
                if t_sec < fade:
                    t=int((t_sec-fade)*sr)
                else:
                    t=1
                          
                ampToneList.append((t,0))
                ampNoiseList.append((t,0))
                freqList.append((t,f))
        
            t=int(t_sec *sr)
            ampTone = a*math.sqrt( 1. - bw )
            ampNoise = a*math.sqrt( 2. * bw ) ;  
            ampToneList.append((t,ampTone))
            ampNoiseList.append((t,ampNoise))   
            freqList.append((t,f))
            cnt=cnt+1
        
        
        t=int((t_sec+fade)*sr)
                          
        ampToneList.append((t,0))
        ampNoiseList.append((t,0))
        freqList.append((t,f))
        
        assert t < size
        
        dur=float(size)/sr

        ampNoiseList.append((size-1,0))
        ampToneList.append((size-1,0))
        freqList.append((size-1,f))

        
        self.ampToneTab=LinTable(ampToneList,size)
        self.ampNoiseTab=LinTable(ampNoiseList,size)
        self.freqTab=LinTable(freqList,size)
        
        self.ampTone=Osc(table=self.ampToneTab,freq=1.0/dur)
        self.ampNoise=Osc(table=self.ampNoiseTab,freq=1.0/dur)
        self.freq=Osc(table=self.freqTab,freq=1.0/dur)
        
        self.white = Noise() 
        self.mod=Biquad(self.white, freq=500, q=1, type=0, mul=self.ampNoise, add=self.ampTone)
                                
        self.osc=Sine(freq=self.freq,mul=self.mod,phase=(init_phase/math.pi/2.0))
        
        
    def out(self):
        self.osc.out()



class LorisSynth:
    
    def __init__(self,parts,sr,size):
        
        self.oscs=[]
        
        for part in parts:
            osc=PartialOsc(part,sr,size)
            self.oscs.append(osc)

        
    def out(self):
        for osc in self.oscs:
            osc.out()
            
            



import loris, os, time

print ' Using Loris version', loris.version()




def analysis(file,resolutionHz,freqDrift,ampFloor,fund):

    a = loris.Analyzer( resolutionHz)
    a.setFreqDrift(freqDrift  )
    a.setAmpFloor( ampFloor )
    
    
    path = os.getcwd()
    cf = loris.AiffFile( file )
    v = cf.samples()
    samplerate = cf.sampleRate()
    size=len(v)
    
    clar = a.analyze( v, samplerate )
    
    loris.channelize( clar, fund )
    loris.distill( clar )
    return clar,size,samplerate
    
  
def analysis(file,resolutionHz,freqDrift,ampFloor,fund):
  
    a = loris.Analyzer( 270 )       # reconfigure Analyzer
    a.setFreqDrift( 30 )
    v = loris.AiffFile( os.path.join(path, 'flute.aiff') ).samples()
    flut = a.analyze( v, samplerate )
    
    # loris.channelize( flut, loris.createFreqReference( flut, 291*.8, 291*1.2, 50 ), 1 )
    refenv = a.fundamentalEnv()
    loris.channelize( flut, refenv, 1 )
    loris.distill( flut )
  


    
path = os.getcwd()
file = os.path.join(path, 'clarinet.aiff')    
clar,size,samplerate=analysis(file,390,30,-80,415)


synth=LorisSynth(clar,samplerate,size)
synth.out()

s.gui(locals())
        
