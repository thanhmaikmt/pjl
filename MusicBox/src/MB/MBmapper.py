import players
import MBmusic

# deprecated just us a dictionary 

class Mapper:
    
    def __init__(self,seq,score,chord_inst,solo_inst):
        self.map={"melody":self.melody,
                  "tonality":self.tonality,
                  "chordNote":self.chordNote,
                  "chord":self.chord,
                  "xy":self.xy}
        
        
        self.chord_player=players.ChordPlayer(chord_inst,score,seq)
        self.melody_player=players.MelodyPlayer(solo_inst,score,seq)
        self.score=score
        
        
    def xy(self,toks,data):
        self.melody_player.inst.set_cc(16,min(data[0],127))
        self.melody_player.inst.set_cc(17,min(data[1],127))
        
    def tonality(self,toks,data):
        
        val1=int(toks[0])
        val2=int(toks[1])
        trig=float(data[0])
        
        print "MAP: tonality",toks,data
        
        if val2 >= 0:
            self.score.set_tonality(MBmusic.tonalities[(val2)%7])
     
        
    def chord(self,toks,data):
        self.chord_player.play(toks,data)
                  
    def chordNote(self,toks,data):
        
        print "MAP: chordNote",toks,data
       
    def melody(self,toks,data):
        """
        Plays a note of the scale in the current tonality
        """
          
        print "MAP: melody ",toks,data
        
        self.melody_player.play(toks,data)



        
class SimpleMapper:
    
    def __init__(self,player):
        self.player=player
        
    def map(self,toks,data):
        self.player.play(toks,data)



class SoloMapper:
    
    def __init__(self,seq,score,melody):
        self.map={"melody":melody.handler}
        
        
    def xy(self,toks,data):
        pass
    
    def tonality(self,toks,data):
        pass
      
        
    def chord(self,toks,data):
        self.chord_player.play(toks,data)
                  
    def chordNote(self,toks,data):
        
        print "MAP: chordNote",toks,data
       
    def melody(self,toks,data):
        """
        Plays a note of the scale in the current tonality
        """
          
        print "MAP: melody ",toks,data
        
        self.melody_player.play(toks,data)
