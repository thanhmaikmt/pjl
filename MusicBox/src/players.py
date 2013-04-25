import music

class ChordPlayer:
        
        def __init__(self,inst,score):
            self.pitches=[]
            self.template=[0,2,4,6]
            self.inst=inst
            self.score=score
            
            
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
            
        
            tonality=self.score.get_tonality()
            
            
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
    
    
        def __init__(self,player,score,seq):

            self.score=score
            self.player=player
            self.seq=seq
        
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
            
            print val,i
            vel=int(val*127)       
            pitch=self.score.get_tonality().get_note_of_scale(i,self.score.key)+36
            #print "play",i,vel
            
            if vel != 0:
                self.player.inst.note_on(pitch,vel)
            else:
                # schedule the note off
                playable = music.Playable(music.NoteOff(pitch), self.player)
                self.seq.add_after(.1, playable)
       