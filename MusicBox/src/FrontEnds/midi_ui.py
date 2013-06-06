    
import MBmidi   
import MBsetup
import OSC
 
#  create PyMidi to initialize misi system.



mid=MBmidi.MidiEngine()

midi_in=mid.open_midi_in(MBsetup.MIDI_IN_NAMES)   
            
     
        
# define input and output channels
# adjust these for hardware reported by above

print midi_in


    
# simple handler to pass events to midi_out device
# define a hander for midi events
def myhandler(evts):
    """
    This version prints then forwards event to the midi out.
    """

    

    for ee in evts:
        e=ee[0]
        print (e)
        cmd1=e[0]>>4
        
        if cmd1 == MBmidi.NOTEON:
            vel=e[2]
        elif cmd1 == MBmidi.NOTEOFF:
            vel=0.0
        else:
            continue
        
        chan=e[0] & 0xF
        
        cmd="/"+str(chan)+"/melody/"+str(e[1])
        

        print cmd,vel
        msg=OSC.OSCMessage(cmd,[vel/128.0])            
        osc_client.send(msg)
    
 
addr=MBsetup.get_osc_ip()
print "using ip", addr
osc_client=OSC.OSCClient()
osc_client.connect(addr)
# register the handler

mid.set_callback(myhandler) 
   
# start deamon
mid.start()



tt=raw_input("Hit cr to quit:")
#wait a few secs then halt
mid.quit()

