import pygame.midi as midi

midi.init()

for i in range( midi.get_count()):
            r = midi.get_device_info(i)
            (interf, name, input, output, opened) = r
    
            in_out = ""
            if input:
                in_out = "(input)"
            if output:
                in_out = "(output)"
    
            print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
                   (i, interf, name, opened, in_out))