import pygame.midi as pgmidi
import threading
import time
import atexit
from mbconstants import *



class Device:
    
    def __init__(self,id,interf, name, input, output, opened):
        self.id=id
        self.interf=interf
        self.name=name
        self.input=input
        self.output=output
        self.opened=opened
        self.channels=16*[None]
        
    def allocate_channel(self,id):
        if self.channels[id] != None:
            raise MidiError("MidiChannel already allocated",self.name+str(id))
        
        inst=Instrument(self.out,id)
        return inst
        
    
class MidiEngine(threading.Thread):
        
    def __init__(self):
        pgmidi.init()
        # register tidy up function to be called at exit.
    
        threading.Thread.__init__(self);
        #atexit.register(self.halt)
        # defualt handler prints midi evts
        self.handler=self.default_handler
     
        
        # print devicess
        self.devs=self.device_info()
        
        self.out_dev=[]
        self.in_dev=[]
        self.running=False
        
        
    def open_midi_out(self,midi_out_names):
        midi_out_id=-1
        for name in midi_out_names:
            for dev in self.devs:
                        
                if dev.output:
                
                    if name in dev.name:
                        print "OPENING MIDI OUT", dev.id,dev.name

                        midi_out_id=dev.id
                        o=pgmidi.Output(midi_out_id, 0)
                        dev.out=o
                        self.out_dev.append(dev)
                        return dev
                        break
                    
        mess="None of the list of devices was found: ["+",".join(midi_out_names)+"]"
        raise MidiError("Device not found :",mess)
        
    
        
    def open_midi_in(self,midi_in_names):
        midi_id=-1
                
        for name in midi_in_names:
            for dev in self.devs:
                        
                if dev.input:
        
                    if name in dev.name:
                        print "OPENING MIDI IN", dev.id,dev.name
                        midi_in_id=dev.id
                        o=pgmidi.Input(midi_in_id, 0)
                        self.in_dev.append(o)
                        dev.o=o
                        return dev
                        break
                    
              
        raise MidiError("Device not found :","None of the list of devices was found")
        
        
        
    def device_info(self):
        devs=[]
        for i in range( pgmidi.get_count()):
            r = pgmidi.get_device_info(i)
            (interf, name, input, output, opened) = r
            devs.append(Device(i,interf, name, input, output, opened))
            in_out = ""
            if input:
                in_out = "(input)"
            if output:
                in_out = "(output)"
    
            print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
                   (i, interf, name, opened, in_out))
            
        return devs
            
#    def set_midi_in(self,midi_in):    
#        self.midi_in = pgmidi.Input(midi_in)
#    
#    
#    def set_midi_out(self,midi_out):    
#        self.midi_out = pgmidi.Output(midi_out, 0)
    

    def default_handler(self,evts):
        print (evts)

    def write(self,evts):
        self.midi_out.write(evts)
                
    def set_callback(self,handler):
        self.handler=handler
        
    def run(self):
        """ Called from the Thread start()
        """
                 
        if self.handler == None:
            raise MidiError("No callback function:"," Use set_callback(some_handler)")
            
        self.running=True
        midi_in=self.in_dev[0]
        
        while self.running: 
            # TODO look at all input devices          
            if midi_in.poll():
                midi_events = midi_in.read(10)
                self.handler(midi_events)
            else:
                time.sleep(0.001)
                 
        print " quitting pgmidi deamon"
            
    def _halt(self):
        
        print  "MidiEngine  Halting Sequener"
        if not self.running:     # make sure we don't do this twice
            return
        
        self.running=False      # flag deamon to halt.
        self.join()             # wait for thread to halt
        print  "Midi Engine Threads joined OK"
#        self.cleanup()
        
    def quit(self):
        """ Quits the midi system releasing the midi devices.
        """
        
        if self.running:
            self._halt()
            

        for dev in self.out_dev:
            for i in range(len(dev.channels)):
                if dev.channels[i]!= None:
                    dev.channels[i].all_note_off()
                    
        pgmidi.quit()
           
        print  "MidiEngine Halted"
     

class Instrument:
    
    
    def __init__(self,midi_out,channel):
        """Create an instument,
        
        A midi out device and a channel number
        """
        
        self.midi_out=midi_out
        self.channel=channel
        
        

    def note_on(self, note, velocity):
        """turns a midi note on.  Note must be off.
        Output.note_on(note, velocity=None, channel = 0)

        Turn a note on in the output stream.  The note must already
        be off for this to work correctly.
        """
        if DEBUGGING:
            print self.channel,note,velocity
            
        self.midi_out.write_short(0x90+self.channel, note, velocity)

    def note_off(self, note, velocity=None):
        """turns a midi note off.  Note must be on.
        Output.note_off(note, velocity=None, channel = 0)

        Turn a note off in the output stream.  The note must already
        be on for this to work correctly.
        """
        if velocity is None:
            velocity = 0

        self.midi_out.write_short(0x80 + self.channel, note, velocity)


    def set_instrument(self, instrument_id):
        """select an instrument, with a value between 0 and 127
        Output.set_instrument(instrument_id, channel = 0)

        """
        if not (0 <= instrument_id <= 127):
            raise ValueError("Undefined instrument id: %d" % instrument_id)

        self.midi_out.write_short(0xc0+self.channel, instrument_id)
        
    def set_volume(self,val):
        
        #  7 vol 11 expression
        print " Set volume",val
        self.midi_out.write_short(0xb0+self.channel,7,val)
        
        
    def all_note_off(self):
        
        #evts=[[[0b1011 0000,120,0],0]]
        self.midi_out.write_short(0xb0+self.channel,120)
        
    def write(self,evts):
        self.midi_out.write(evts)
        

class MidiError(Exception):
    """Exception raised for errors in the midi systen

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg
            
    def get_message(self):
        return self.expr+self.msg                    
    
