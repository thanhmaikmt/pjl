
import sys
import os

import pygame
import pygame.midi
from pygame.locals import *


try:  # Ensure set available for output example
    set
except NameError:
    from sets import Set as set


def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

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
        



def input_main(in_device_id = None,out_device_id=None):
    pygame.init()
    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post

    pygame.midi.init()

    _print_device_info()


    if in_device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = in_device_id

    print ("using input_id :%s:" % input_id)
    i = pygame.midi.Input( input_id )

    if out_device_id is None:
        port = pygame.midi.get_default_output_id()
    else:
        port = out_device_id

    print ("using output_id :%s:" % port)


    instrument=24
    midi_out = pygame.midi.Output(port, 0)
    try:
        midi_out.set_instrument(instrument)


        going = True
        while going:
            events = event_get()
            for e in events:
                if e.type in [QUIT]:
                    going = False
                if e.type in [KEYDOWN]:
                    going = False
                if e.type in [pygame.midi.MIDIIN]:
                    print (e)
                    midi_out.note_on(60, 100)
                     
            if i.poll():
                midi_events = i.read(10)
                # convert them into pygame events.
                midi_evs = pygame.midi.midis2events(midi_events, i.device_id)
    
    
               
    
                for m_e in midi_evs:
                    event_post( m_e )



    finally:
        del midi_out
        pygame.midi.quit()
