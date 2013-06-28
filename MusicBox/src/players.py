import MBmusic
import array

class BasicPlayer:
    
        """
        plays a melody instrument using the OSC  message
        """
    
        def __init__(self,inst,score=None,seq=None):

            self.score=score
            self.inst=inst
            self.seq=seq
            self.player=MBmusic.Messenger(inst)
            self.notesOn={}
        
        def play(self,toks,data):     
            if toks[0] == 'xy':
                x=int(float(data[1])*127)
                y=int(float(data[0])*127)
                #print " melody xy",x,y
                self.player.inst.set_cc(12,x)
                self.player.inst.set_cc(13,y)
                
                return
            
            val=float(data[0])
             
            i=int(toks[0])
            
            vel=int(val*127)       
           
            if self.score:
                beat=self.seq.get_stamp()
                pitch=self.score.get_tonality(beat).get_note_of_scale(i,self.score.key)+36
            else:
                pitch=i+48    
            
            #print "play",pitch,vel
            
            if vel != 0:
                assert not self.notesOn.get(pitch)
                self.player.inst.note_on(pitch,vel)
                self.notesOn[pitch]=vel
            else:
                assert self.notesOn.get(pitch)
                self.player.inst.note_off(pitch)
                del self.notesOn[pitch]

        def is_playing(self):
            return len(self.notesOn) > 0
        
        
class ChordPlayer:
        
        def __init__(self,inst,score,seq):
            self.pitches=[]
            self.template=[0,2,4,6]
            self.inst=inst
            self.score=score
            self.seq=seq
            
        def play(self,toks,data):
#           print "chord",toks,data
            
            if toks == "xy":
                y=int(float(data[0])*127)
                x=int(float(data[1])*127)
                self.inst.set_volume(y)
                return
            

            for pitch in self.pitches:
                self.inst.note_off(pitch)
                
            self.pitches=[]
                                        
           # inversion=int(toks[1])     #   TODO
            
            vel=int(float(data[0])*127)
            if vel == 0:
                return
            
            beat=self.seq.get_beat()
            tonality=self.score.get_tonality(beat)
            
            
            for p in range(len(self.template)):
                pit=tonality.get_note_of_chord(self.template[p],self.score.key)+48
                self.inst.note_on(pit,vel)
                self.pitches.append(pit)

        #  Play notes (shift up +12 if pitch is too low)     
#            for p in self.pitches:
#                while p < self.lowest:
#                    p += 12
#                

            
class MelodyPlayer:
    
        """
        plays a melody instrument using the OSC  message
        """
    
        def __init__(self,inst,score=None,seq=None):

            self.score=score
            self.inst=inst
            self.seq=seq
            self.player=MBmusic.Messenger(inst)
        
        def play(self,toks,data):     
            if toks[0] == 'xy':
                x=int(float(data[1])*127)
                y=int(float(data[0])*127)
                print " melody xy",x,y
                self.player.inst.set_cc(12,x)
                self.player.inst.set_cc(13,y)
                
                return
            
            val=float(data[0])
            
#            assert len(toks) >1
             
            i=int(toks[0])
            
            #print "Melody ",val,i
            vel=int(val*127)       
           
            
            if self.score:
                beat=self.seq.get_stamp()
                pitch=self.score.get_tonality(beat).get_note_of_scale(i,self.score.key)+36
            else:
                pitch=i+48    
            
            #print "play",pitch,vel
            
            if vel != 0:
                self.player.inst.note_on(pitch,vel)
            else:
                self.player.inst.note_off(pitch)
                # schedule the note off
                #playable = MBmusic.Playable(MBmusic.NoteOff(pitch), self.player)
                #self.seq.schedule(beat+0.05, playable)
       