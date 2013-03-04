import pygame
import pygame.locals as pgl
import pygame.midi 
from   pygame.locals import *


try:  # Ensure set available for output example
    set
except NameError:
    from sets import Set as set




def _print_device_info():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
               (i, interf, name, opened, in_out))
        

midi_i = 3 ; midi_o = 8;

pygame.init()


pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post

pygame.midi.init()


_print_device_info()

midi_in = pygame.midi.Input(midi_i)
#window = pygame.display.set_mode((468, 60))


instruments=[6,28,13]

midi_out = pygame.midi.Output(midi_o, 0)

for i in range(len(instruments)):
    midi_out.set_instrument(instruments[i],i)


mt = None
going = True
while going:
    events = event_get()
    for e in events:
        if e.type in [pgl.QUIT]:
            going = False
        if e.type in [pgl.KEYDOWN]:
            going = False
        if e.type in [pygame.midi.MIDIIN]:
            print (e), mt
            pitch=e.data1
            vel=e.data2
            if e.data1 > 60:
                midi_out.note_on(pitch, vel,0)
            else:
                midi_out.note_on(pitch, vel,1)
                
    if midi_in.poll():
        midi_events = midi_in.read(10)
        
        for x in midi_events:
            print (x)   
        midi_out.write(midi_events)
            
            
        #mt = pygame.midi.time()
        # convert them into pygame events.
        #midi_evs = pygame.midi.midis2events(midi_events, midi_in.device_id)

        #for m_e in midi_evs:
        #    event_post( m_e )

del midi_in
del midi_out

pygame.midi.quit()