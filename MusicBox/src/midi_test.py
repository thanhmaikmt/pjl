    
from midi import  *  
    
       
if __name__ == "__main__":
    
    # test code
    #  create PyMidi to initialize misi system.
    mid=Engine()

    
    # print devicess
    devs=mid.device_info()
    
    midi_in=-1
    midi_out=-1
    
    for dev in devs:
        if dev.input:
            print dev.id,dev.name
            if "microKEY" in dev.name:
                midi_in=dev.id
                
        if dev.output:
            print dev.id,dev.name
            if "MusicBox" in dev.name:
                midi_out=dev.id
                
                
         
            
    # define input and output channels
    # adjust these for hardware reported by above
    
    print midi_in,midi_out
    mid.set_midi_in(midi_in)
    mid.set_midi_out(midi_out)
    
    
    #evts=[[[0b10110000,0,120],0],[[0b10110000,32,0],0]]
    #mid.midi_out.write(evts)
    #vts=[[[0b10110000,0,120],0],[[0b10110000,32,0],0]]
    #mid.midi_out.write([[[0xc0,0],0]])
    
        
    # simple handler to pass events to midi_out device
    # define a hander for midi events
    def myhandler(evts):
        """
        This version prints then forwards event to the midi out.
        """
        for e in evts:
            e[0][0]+=1
               
        mid.midi_out.write(evts)
        print (evts)
     
    # register the handler
    mid.set_callback(myhandler) 
       
    # start deamon
    mid.start()
    
    
    
    tt=raw_input("Hit cr to quit:")
    #wait a few secs then halt
    mid.halt()
    
    