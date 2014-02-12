srate=44100.0

import random
import inspect
import math
import pyo
import time

class Param:
    
    def __init__(self,min=0,max=1,scale='lin',unit='float',array=False):
        self.min=min
        self.max=max
        self.scale=scale
        self.unit=unit
        self.array=True
        
    
    #@staticmethod
    def rand(self):
    
        x=random.random()
     
        if self.scale == 'lin': 
            return self.min*x+self.max*(1.0-x)
           
        elif self.scale == 'log':
            K1=math.log(self.min)
            K2=math.log(self.max)-K1
            return math.exp(K1+K2*x)
        
        elif self.scale == 'int' or self.scale == 'choice':
            
            return random.randrange(self.min,self.max)
        
        elif self.scale == 'miditohertz':
            return pyo.midiToHz(random.randrange(self.min,self.max))
            
        else:
            print " I don't know how to do this "
            
    
class Data:
    """
    An object to hold the genetic data of a gene
    Persisted as a pickled blob in the database.
    Add any data you need to be used to build the concrete gene here.
    All the entries in the map associated with a XXXGene subclass must exist 
    in the data otherwise the GUI will get upset.
    """
    pass

do_del=True
#remote=False

class Gene(object):
    """ 
    Base class Gene encapsulates a single unit of the system.
    
    A Gene has a primary role to represent the genetic string.
    a gene can exist without being built as a real pyo objects.
    in this case the pheno parameter  can be None.
       
    To realize a Gene in it's playable form the pheno must be given given to the constructor
    and the gene must be built. Before this call the gene does not depend on pyo. This allows 
    decoupling of the GUI and the the audio engine. 
    
        
        Parameters:
        
        kwargs: can be used to initialize the data for the gene.
               In this case it must initialize all the fields for the Type of Gene
        
               kwargs can be empty then the data can be created randomly by invoking
               the randomize method.
        
        pheno: Once the data is set the pyo representation of a gene is realized by
               invoking the build method. For this to succeed you need to set the pheno
               for the gene.
               
        build: Realises the gene. 
        
            
    """
    
    def __init__(self,pheno,**kwargs):
        """
        generic initialiser.
     
        : Args :
        
            kwargs :  option list of attributes key=value  that is stored in the self.data
            
        """
          
        if pheno != None:
            self.pheno=pheno
            self.data=Data()
            pheno.genes.append(self)
   
        if len(kwargs) > 0:
            for key in kwargs:
                setattr(self.data,key,kwargs[key])
            
        self.ID=None
        
        
    def __str__(self):
        str1=self.__class__.__name__
        ms=inspect.getmembers(self.data)
        for m in ms[2:]:
            str1+=m.__str__()
            
        return str1

    def getScale(self):
        return 1.0
    

    
            
        
    #def __del__(self):
        
    #    print "DELETING",self

    

        
class BeatGene(Gene):
    
    maps={"bpm":Param(20.,400.,'log')}
    
    def __init__(self,pheno=None,**kwargs):
        Gene.__init__(self,pheno,**kwargs)
        if pheno != None:    
            self.pheno.triggers.append(self)   
            
    def randomize(self):
        self.data.bpm=BeatGene.maps['bpm'].rand()
    
    def build(self):
        
        self._beat_dur=60.0/self.data.bpm
        self._ticks_per_beat=self._beat_dur*srate
        self._trig=pyo.Trig()
        self.pos =pyo.Count(self._trig,min=0,max=int(self._ticks_per_beat),mul=1./self._ticks_per_beat)
        self.trigger =pyo.Thresh(self.pos,0.7,dir=1)
        #self._count=0
        
    def play(self):
        print "play trigger"
        self._trig.play()
        print "played"
         
    def getScale(self):
        return srate/2.0
    
    def setAttr(self,attr,val,build):
        setattr(self.data,attr,val)
        if build:
            self.beat_dur=60.0/self.data.bpm
            self.ticks_per_beat=self.beat_dur*srate
            self.pos.max=int(self.ticks_per_beat)
            self.pos.mul=1./self.ticks_per_beat
            
    def kill(self):
        self._trig.stop()
        self.pos.stop()
        self.trigger.stop()
        if do_del:
            del self._trig
            del self.pos
            del self.trigger
            
        
            
class FilterGene(Gene):

    #filtMaps = [Gene.freq_map, Gene.q_map, Gene.mul_map]
            
    maps={"freq":Param(10,srate/2,'log'),
          "q":Param(0.1,500.0,'log'),
          "mul":Param(-2.0,2.0,'lin'),
          "type":Param(2,3,'choice',
                       ['lowpass',
                        'highpass',
                        'bandpass',
                        'bandstop',
                        'allpass']     )}
    
    def __init__(self,pheno=None,**kwargs):
        Gene.__init__(self,pheno,**kwargs)
        if pheno != None:    
            self.pheno.filters.append(self)
            
        
    def randomize(self):
        self.data.freq=FilterGene.maps["freq"].rand()
        self.data.type=FilterGene.maps["type"].rand()
        self.data.q=FilterGene.maps["q"].rand()
        self.data.mul=FilterGene.maps["mul"].rand()  
        self.data.input_id=self.pheno.input_id
      #  self.data.freq_input=self.pheno.envelopes.randomID()
        
        
    
    def setAttr(self,attr,val,build):
        setattr(self.data,attr,val)
        if build:
            setattr(self.filt,attr,val)
            
        
    def build(self):
        self.input=self.pheno.filterIns.get(self.data.input_id)
        self.mul=self.data.mul
        #self.freq_mod=(1.0+self.pheno.envelopes.get(self.data.freq_input).envelope)*self.data.freq
        self.filt=pyo.Biquad(self.input.src,
                            freq=self.data.freq,  #_mod,
                            type=self.data.type,
                            q=self.data.q,
                            mul=self.mul)
           
        self.out=pyo.SPan(self.filt).out()
      
  
    
    def kill(self):
        self.filt.stop()
        self.out.stop()
        if do_del:
            del self.filt
            del self.out
            
        
class DelayGene(Gene):  # not used at the moment probably broken

    
    maps={"delay":Param(0.0,2.0,'lin')}
    
    def __init__(self,pheno=None,**kwargs):       
        Gene.__init__(self,pheno,kwargs) 
#        if len(kwargs) > 0:
#            self.data.delay=kwargs['delay']     
        
    def randomize(self):
        self.data.trig_id=self.pheno.trig_id
        self.data.delay=random.random()             # amount of a beat

    def build(self):
        beat_dur=60.0/self.pheno.bpm
        dur=beat_dur*self.data.delay
        trig=self.pheno.triggers.get(self.data.trig_id).trigger
        self.trigger=pyo.SDelay(trig,delay=dur)
  
        
    def getScale(self):
        return srate/2.0
    
    def setAttr(self,attr,val,build):
        setattr(self.data,attr,val)
        if build:
            self.pheno.bpm=val
            beat_dur=60.0/self.pheno.bpm
            dur=beat_dur*self.data.delay
            self.trigger.delay=dur
            
    
    def kill(self):
        self.trigger.stop()
        if do_del:
            del self.trigger
       
        
class OffBeatGene(Gene):

    
    maps={"pos":Param(0.0,1.0,'lin')}
    
    def __init__(self,pheno=None,**kwargs):       
        Gene.__init__(self,pheno,**kwargs)  
#        if len(kwargs) > 0 :
#            self.data.pos=kwargs['pos']
#    
        if pheno != None:   
            self.pheno.triggers.append(self)
            
    def randomize(self):
        self.data.pos=random.random()             # amount of a beat
        self.data.trig_id=self.pheno.trig_id
        
    def build(self):
      
        pos=self.pheno.triggers.get(self.data.trig_id).pos
        self.trigger=pyo.Thresh(pos,self.data.pos)
 

    def getScale(self):
        return srate/2.0
    
    def setAttr(self,attr,val,build):
        setattr(self.data,attr,val)
        if build:
            self.trigger.setThreshold(val)
        
    def kill(self):
        self.trigger.stop()
        if do_del:
            del self.trigger



class NoiseGene(Gene):
    
    maps=None
    
    def __init__(self,pheno=None,**kwargs):
        Gene.__init__(self,pheno,**kwargs)
        
        if pheno != None:
            self.pheno.noises.append(self)

    def build(self):
        self.noise=pyo.Noise()
        

    def kill(self):
        self.noise.stop()
        if do_del:    
            del self.noise
    
    
class OscGene(Gene):
           
    maps={"type":Param(0,8,'choice',[
                            'Saw up',
                            'Saw down',
                            'Square',
                            'Triangle',
                            'Pulse',
                            'Bipolar pulse',
                            'Sample and hold',
                            'Modulated Sine'])}
          
    def __init__(self,pheno=None,**kwargs):
        Gene.__init__(self,pheno,**kwargs)

        if pheno != None:
            self.pheno.noises.append(self)
   
        
    def randomize(self):
        self.data.type=OscGene.maps["type"].rand()  
        self.data.phrase_id=self.pheno.phrase_id
        
        
    
    def setAttr(self,attr,val,build):
        setattr(self.data,attr,val)
        if build:
            setattr(self.noise,attr,val)
            
        
    def build(self):
        self.pitch=self.pheno.phrases.get(self.data.phrase_id).pitch
        self.noise=pyo.LFO(self.pitch, type=self.data.type)   
      
  
    
    def kill(self):
        self.noise.stop()
        if do_del:
            del self.noise
               
    
            
class GateEnvelopeGene(Gene):  # Broken 
    
    
    maps={"dur":Param(.01,.05,'log')}
      
    def __init__(self,pheno=None,**kwargs):
        Gene.__init__(self,pheno,**kwargs)
 
        if pheno != None:
            self.pheno.envelopes.append(self)
   
        
    def randomize(self):
        self.data.trig_id=self.trig_id
        self.data.amp_id=self.pheno.amp_id
        self.data.dur=GateEnvelopeGene.maps['dur'].rand()


    def build(self):
        trig=self.pheno.triggers.get(self.data.trig_id).trigger
        modul=self.pheno.amps.get(self.data.amp_id).value
        self.envelope=pyo.Gate(trig,risetime=0.001,falltime=self.data.dur,outputAmp=True,mul=modul)
        #self.src=pyo.Gate(trig,risetime=0.001,falltime=self.data.dur,outputAmp=True)

    def setAttr(self,attr,val,build):
        setattr(self.data,attr,val)
        if build:
            self.modulator.falltime=val
        
    def kill(self):
        self.envelope.stop()
        if do_del:
            del self.envelope
 
class ADSREnvelopeGene(Gene):
    """
    
    
    
    
    
    """
    
    
    maps={"attack":Param(.001,.5,'log'),
          "decay":Param(.001,.5,'log'),
          "sustain":Param(.001,1.,'lin'),
          "release":Param(.001,.5,'log')
          }
    
    #maps={"dur":Param(.01,.05,'log')}
      
    def __init__(self,pheno=None,**kwargs):
        Gene.__init__(self,pheno,**kwargs)

        if pheno != None:
            self.pheno.envelopes.append(self)
   
        
    def randomize(self):

#        self.data.trig_on=self.pheno.trig_on
#        self.data.trig_off=self.pheno.trig_off

        self.data.phrase_id=self.pheno.phrase_id
        self.data.attack=ADSREnvelopeGene.maps['attack'].rand()
        self.data.decay=ADSREnvelopeGene.maps['decay'].rand()
        self.data.sustain=ADSREnvelopeGene.maps['sustain'].rand()
        self.data.release=ADSREnvelopeGene.maps['release'].rand()


    def build(self):
#        trig_on=self.pheno.triggers.get(self.data.trig_on).trigger
#        trig_off=self.pheno.triggers.get(self.data.trig_off).trigger
#        self.pulse=pyo.Iter(trig_on+trig_off,choice=[1.0,0.0])
#        

        self.phrase=self.pheno.phrases.get(self.data.phrase_id)
        #self.amp=
        #modul=self.pheno.amps.get(self.data.amp_id).value
        
        self.envelope=pyo.MidiAdsr(self.phrase.amp,
                                   attack=self.data.attack,
                                   decay=self.data.decay,
                                   sustain=self.data.sustain,
                                   release=self.data.release)

        #self.src=pyo.Gate(trig,risetime=0.001,falltime=self.data.dur,outputAmp=True)

    def setAttr(self,attr,val,build):
        setattr(self.data,attr,val)
        if build:
            setattr(self.envelope,attr,val)
        
    def kill(self):
        #self.pulse.stop()
        self.envelope.stop()
        if do_del:
                
            del self.envelope
            #del self.pulse
            
class ModulatedNoiseGene(Gene):
    """
    
    
    """
    
    maps=None
            
    def __init__(self,pheno=None,**kwargs):
        Gene.__init__(self,pheno,**kwargs)

        if pheno != None:
            self.pheno.filterIns.append(self)    
 
 
    def randomize(self):
        self.data.noise_id=self.pheno.noise_id
        self.data.env_id=self.pheno.env_id
     

    def build(self):
        env=self.pheno.envelopes.get(self.data.env_id).envelope
        inp=self.pheno.noises.get(self.data.noise_id).noise
        self.src=inp*env
   
    def kill(self):
        self.src.stop()
        if do_del:   
            del self.src
   
   
   
   
class SequenceGene(Gene):      
 
    maps=None
    """
    Base Class for sequence type objects.
    a list of integers.
    The sub class must provide a lookup method to translate index into
    the actual object.
    The first trigger (start of the bar) is used to increment an index.
     
    """
    
    def __init__(self,pheno=None,**kwargs):       
        Gene.__init__(self,pheno,**kwargs)  

        if pheno != None:
            self.pheno.sequences.append(self)
    
    def randomize(self):
        #self.data.input=0 # env.randomTrigID()
        assert self.pheno != None
        
        self.data.seq=[]
        len1=self.pheno.sequence_len
        for _ in range(len1):
            self.data.seq.append(random.randrange(self.pheno.map_size))      
         
        
         
    def setAttr(self,attr,seq,build):
        setattr(self.data,attr,seq)
         
    def build(self):
        pass
    
    def kill(self):
        if do_del:
            del self.data.seq
        
    

class AmpMapGene(Gene):
    
    #maps=None

    def __init__(self,pheno=None,**kwargs):
        Gene.__init__(self,pheno,**kwargs)       
     
        if pheno != None: 
            self.pheno.amps.append(self)
            

      
    def randomize(self):
        assert self.pheno != None
        range1=self.pheno.map_size     
       
        self.data.map=[]
       
        for _ in range(range1):
            self.data.map.append(random.random())      

    def kill(self):
        pass
    
    def build(self):
        pass
    
   
class PitchMapGene(Gene):
    
    """
    Subclass of Sequence that stores a list of midi notes
    """
 
    def __init__(self,pheno=None,**kwargs):
        Gene.__init__(self,pheno,**kwargs)       
        if pheno != None: 
            self.pheno.notes.append(self)
             
    def randomize(self):
        assert self.pheno != None

        range1=self.pheno.map_size   
        low=self.pheno.midi_low
        high=self.pheno.midi_high
        self.data.map=[]

        for _ in range(range1):
            self.data.map.append(random.randint(low,high))     # TODO SCALES ETC     
    
    def kill(self):
        pass
    
    def build(self):
        pass
            
class PhraseGene(Gene):
    
    """
    Like a midi sequence   
    """
    
    
    def __init__(self,pheno=None,**kwargs):
        Gene.__init__(self,pheno,**kwargs)       
        if pheno != None: 
            self.pheno.phrases.append(self)
    
    def callback(self,i):
        
#        if i == self.n_beats_bar :
#            self.barCount += 1
#            if self.barCount >= self.data.n_bars:
#                self.barCount = 0
#       
#        print  i         
#        print  self.pitch_seq
#        print  self.pitch_map
#        
        ip=self.pitch_seq[i]
        self.pitch.setValue(pyo.midiToHz(self.pitch_map[ip]))    #(i+self.barCount*self.n_per_bar)%len(self.pitch_seq)]]))

        amp=(self.amp_map[self.amp_seq[i]]-self.data.amp_thresh)/(1.0-self.data.amp_thresh)
        amp=max(0,amp)
        
        self.amp.setValue(amp)  # (i+self.barCount*self.n_per_bar)%len(self.amp_seq)]])
        



    def build(self):
        self.barCount=-1      
       
        self.n_beats_bar=len(self.pheno.triggers)  
        self.pitch_seq=self.pheno.sequences.get(self.data.pitch_seq_id).data.seq
        self.pitch_map=self.pheno.notes.get(self.data.pitch_map_id).data.map
        
        self.amp_seq=self.pheno.sequences.get(self.data.amp_seq_id).data.seq
        self.amp_map=self.pheno.amps.get(self.data.amp_map_id).data.map
        
        self.pitch=pyo.Sig(0)
        self.amp=pyo.Sig(0)
        self.callback(0)
        
        
        self.trigFuncs=[]
        
        for i,g in enumerate(self.pheno.triggers):
            self.trigFuncs.append(pyo.TrigFunc(g.trigger,self.callback,arg=i))

    def randomize(self):
        #self.data.input=0 # env.randomTrigID()
        assert self.pheno != None
        self.data.pitch_seq_id=self.pheno.pitch_seq_id
        self.data.pitch_map_id=self.pheno.pitch_map_id
        self.data.amp_seq_id=self.pheno.amp_seq_id
        self.data.amp_map_id=self.pheno.amp_map_id
        self.data.n_bars=self.pheno.n_bars
        self.data.amp_thresh=random.random()
        
    def kill(self):
        
        for t in self.trigFuncs:
            t.stop()
            
        self.amp.stop()
        self.pitch.stop()
      
            
        if do_del:
            del self.amp
            del self.pitch
            del self.trigFuncs
            

class GeneList:
        
        def __init__(self):
            self.list=[]
            
        def append(self,g):
            self.list.append(g)
            
        def __len__(self):
            return self.list.__len__()
         
        def randomID(self):
            assert len(self.list)>0
            return random.randint(0,len(self.list)-1)
        
        def get(self,i):
            return self.list[i]
        
        def index(self,o):
            return self.list.index(o)  
        
        def __iter__(self):
            return self.list.__iter__()
        
        def __getitem__(self,ID):
            return self.list[ID]
        
        def lastID(self):
            return len(self.list)-1


   
                      
class Pheno: 
       
    """
    Top level ga object
    
    Contains: 
      - a Nome which has a list of genes.
      - lists of sources/sinks used to connect the components
         defined by each gene. Genes use indices to these list 
         to build the connections
    
     
    List of Genes.
    
    member data:
     title
     composer
     key       --  database primary key (None if not committed)
     genes     --  genetic info
    """
    
 
            
    
    def __init__(self,title="Title",composer="Anon"):
        self.title=title
        self.composer=composer
        self.ID=None
        self.mum_ID=None
        self.dad_ID=None             
        self.genes=GeneList()
        self.triggers=GeneList()  
        self.amps=GeneList()
        self.notes=GeneList()
        self.noises=GeneList()
        self.filterIns=GeneList()
        self.envelopes=GeneList()
        self.sequences=GeneList()
        self.filters=GeneList()
        self.phrases=GeneList()
        self.built=False
  
        
    def kill(self):
        """
        kill the beast 
        """
       
       
        del self.triggers
        del self.noises
        del self.filterIns
        del self.envelopes   
        del self.amps  
        del self.filters
        del self.sequences
        del self.notes
        del self.phrases
   
        for g in reversed(self.genes):
            g.kill()
            
        del self.genes     
        
              
    def __str__(self):
         
        str1=self.ID.__str__() +": "+ self.title+" "+self.composer+"\n"
        
        for g in self.genes:
            str1 += g.__str__()+"\n"
           
        return str1
    
    def count(self,type1):
        cnt=0
        for g in self.genes:
            if g.type == type1:
                cnt += 1
        return cnt   
            
  
       
    def randomize(self,**kwargs):
        
        """
        create a random representation based on given parameters
        note that the Gene constructor adds it self to the nome genes,
        
        Parameters:
        n_delay       : number of delays
        n_envelope    : number of envelopes
        n_modulation  : noise into envelopes
        n_voice       : number of voices
        """
        
        
        self.n_bars=1
        
        self.midi_low=kwargs.get('midi_low',20)
        self.midi_high=kwargs.get('midi_high',80)
        
        
        self.sequence_len=kwargs.get('n_offbeat',5)+1   # kwargs.get('sequence_len',10)
    
        # create triggers
        gene=BeatGene(self)
        gene.randomize()
        
        self.trig_id=0
      
      
      
        for _ in range(kwargs.get('n_offbeat',5)):
            gene=OffBeatGene(self)
            gene.randomize()
            
            
        self.map_size=20
        
        for _ in range(kwargs.get('n_noise',3)):
          
            #self.sequence_range=self.map_size
            gene=SequenceGene(self)
            gene.randomize()
            
            
            gene=AmpMapGene(self)
            gene.randomize()
            
            gene=PitchMapGene(self)
            gene.randomize()
    
            self.pitch_seq_id=self.sequences.lastID()
            self.pitch_map_id=self.notes.lastID()
            self.amp_seq_id=self.pitch_seq_id
            self.amp_map_id=self.amps.lastID()
        
        
            gene=PhraseGene(self)
            gene.randomize()
            
            gene=NoiseGene(self)
            
            self.phrase_id=self.phrases.lastID()
            gene=ADSREnvelopeGene(self)
            gene.randomize()
            
            self.noise_id=self.noises.lastID()
            self.env_id=self.envelopes.lastID()
           
            gene=ModulatedNoiseGene(self)
            gene.randomize()
            
            self.input_id=self.filterIns.lastID()
            gene=FilterGene(self)
            gene.randomize()
        
        
        for _ in range(kwargs.get('n_osc',5)):
            
            
            gene=SequenceGene(self)
            gene.randomize()
            
            gene=AmpMapGene(self)
            gene.randomize()
            
            gene=PitchMapGene(self)
            gene.randomize()
           
            self.pitch_seq_id=self.sequences.lastID()
            self.pitch_map_id=self.notes.lastID()
            self.amp_seq_id=self.pitch_seq_id
            self.amp_map_id=self.amps.lastID()
        
            gene=PhraseGene(self)
            gene.randomize()
        
            self.phrase_id=self.phrases.lastID()
            
            gene=OscGene(self)
            gene.randomize()
            
            gene=ADSREnvelopeGene(self)
            gene.randomize()
            
            self.noise_id=self.noises.lastID()
            self.env_id=self.envelopes.lastID()
           
            gene=ModulatedNoiseGene(self)
            gene.randomize()
            
            self.input_id=self.filterIns.lastID()
            gene=FilterGene(self)
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
    
 
  
      

class Breeder:
            
        def _sex(self, a, b):
                   
            if b == None or (random.random() > 0.5 and a != None):
                self.pheno.genes.append(a)
            else:
                self.pheno.genes.append(b)
   
        def mate(self, mum, dad):
            self.pheno = Pheno("OffSprung","Hybrid")
            self.pheno.mum_ID = mum.ID
            self.pheno.dad_ID = dad.ID
            if mum.ID == 0 or dad.ID == 0:
                print " Warning uncommitted parent"
                
            map(self._sex, mum.genes, dad.genes)
            
            self.pheno.mum_ID=mum.ID
            self.pheno.dad_ID=dad.ID
                         
            return self.pheno
            

if __name__ == "__main__":
    
    s=pyo.Server(sr=srate,duplex=0).boot()
    s.verbosity=15
    
    pheno=None
    def reco():
        
        global pheno
        if pheno != None:
            pheno.kill()
            time.sleep(0.2)
            
        pheno=Pheno()
        pheno.randomize(sequence_len=40,
                     n_noise=5,
                     n_sequences=10,
                     n_amp_map=10,
                     n_note_map=10,
                     n_osc=20,
                     n_envelope=10,
                     n_enveloped_noise=10,
                     n_offbeat=10,
                     n_filter=20) #n_src,n_delay,n_connect, n_voice)     
        pheno.build()
    
        #print "Pheno \n",pheno1

        pheno.play()
    
    
    reco()     
    s.gui(locals())
