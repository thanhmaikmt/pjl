
import linkedlist

        
        
class Event:
    
    def __init__(self,tick,message):
        self.tick=tick
        self.message=message
        
    def __gt__(self,a):
        return self.tick > a.tick
    
    def __lt__(self,a):
        return self.tick < a.tick
    
    def __eq__(self,a):
        return self.tick == a.tick
        
        

class Message(Event):
    
    def __init__(self,event,player):
        self.player=player
        Event.__init__(self,event.tick,event.message)
        
    def send(self):
        self.player.play(self.message)
    
    
class Phrase:
    
    def __init__(self):
        self.list=linkedlist.OrderedLinkedList()
        
        
    def add(self,tick,message):
        self.list.insert(Event(tick,message))
 
         
    def __iter__(self):
        return self.list.__iter__()

        
  
class Scheduler:

    def __init__(self,phrase,player):
        self.phrase=phrase   
        self.player=player   
        
    def schedule(self,start,to,sequencer):
        
        for node in self.phrase:
            if node.data.tick < start:
                continue
            if node.data.tick > to:
                break
            sequencer.add(Message(node.data,self.player))
            
    
if __name__ == "__main__":    
    
    phrase=Phrase()
    phrase.add(0,"one")
    phrase.add(3,"three")
    phrase.add(4,"four")
    phrase.add(2,"two")
    phrase.add(2,"anothertwo")
   
    class Player:
        
        def play(self,event):
            print event
    
    
    
    worker=Scheduler(phrase,Player())
    
    import sequencer
    
    seq=sequencer.Sequencer()
    worker.schedule(0,10,seq)
    
    seq.start()
    


        
    