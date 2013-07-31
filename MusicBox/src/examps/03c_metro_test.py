import sys
sys.path.append('../MB')

import MB
import dlinkedlist


context=MB.Context(seqtype=MB.SequencerBPM)
context.seq.set_bpm(100)

pl=dlinkedlist.OrderedDLinkedList()


pl.append(0,("1",("1",)))
pl.append(1,("2",("0.8",)))
pl.append(2,("2",("1",)))
pl.append(3,("2",("0.8",)))


phrase=MB.Phrase(pl.head,pl.tail)

player=context.create_player(chan=9,pipe_to_beat=False)


context.start(None)
player.play_phrase(pl,2,4)



    


        
    