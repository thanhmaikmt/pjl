import sys
sys.path.append('../MB')
  
import MBmidi   
import MBsetup  
import time
#  create PyMidi to initialize misi system.



mid=MBmidi.MidiEngine()

midi_out=mid.open_midi_out(MBsetup.MIDI_OUT_NAMES)
  
            
inst=MBmidi.Instrument(midi_out.out,0)     
inst.set_reverb(80)
 
NRPN_MSB_CC=99
NRPN_LSB_CC=98

DATA_MSB_CC=6
DATA_LSB_CC=38



def msb_lsb_bipolar(val):
    vvv=0x2000 + int(val*4096)
    lsb=vvv & 0x7f
    msb= (vvv >> 8) 
    return msb,lsb


def msb_lsb_raw(vvv):
    #vvv=0x2000 + val
    lsb=vvv & 0x7f
    msb= (vvv >> 7) 
    return msb,lsb


m,l=msb_lsb_raw(0)
print hex(m*128+l)



for i in range(-2000,2000):
    msb,lsb=msb_lsb_raw(i)
    print i,msb*128+lsb-0x2000
    assert i == (msb*128+lsb)    
    

def pan(val):    
    inst.set_cc(99, 120)       
    inst.set_cc(98, 17)
    
    msb,lsb=msb_lsb_bipolar(val)
    print hex(msb),hex(lsb)       
    inst.set_cc(DATA_LSB_CC, lsb)
    inst.set_cc(DATA_MSB_CC, msb)    
    
def initialFilterQ(val):
    # rangel 0-1   (-ve treated as 0)
    # 0 is flat
    # initialFilterQ cB 0 0 None 960 96 dB 0 None
    inst.set_cc(99, 120)       
    inst.set_cc(98, 9)
    
    msb,lsb=msb_lsb_raw(val)
    print "Q:",hex(msb*128+lsb)       
    inst.set_cc(DATA_LSB_CC, lsb)
    inst.set_cc(DATA_MSB_CC, msb)    
    
def initialFilterFc(val):
    # 1500 ---  13500 

    inst.set_cc(99, 120)       
    inst.set_cc(98, 8)
    
    msb,lsb=msb_lsb_raw(val)
    #print hex(msb),hex(lsb)       
    inst.set_cc(DATA_LSB_CC, lsb)
    inst.set_cc(DATA_MSB_CC, msb)    
       
    
def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

pitch=48


q=960

while True:
   for q in range(0,96000,1000):  
     print hex(q)  
     initialFilterQ(q)
     initialFilterFc(1500)
     inst.note_on(pitch, 120)
     for f in range(1500,13500,200):
        initialFilterFc(f)     
        time.sleep(.01)
        inst.note_off(pitch)
    
    
#wait a few secs then halt
mid.quit()

