

MIDI_OUT_NAMES=["to ARGO Appli Fluidsynth v9 1","Synth input port (Qsynth1:0)","IAC Driver IAC Bus 1"]
MIDI_IN_NAMES=["MicroKey","microKEY-25 KEYBOARD","Pro24DSP MIDI","Keystation MIDI 1"]
DEBUGGING=False


def get_osc_ip():
    if True:
        return "127.0.0.1",7110
    else:


        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            print ip
            
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
             if not ip.startswith("127."):
                 break
             
        return ip,7110     
        

class priority:
    pass
    
  
priority.score=1
#def EQUALS(x,y):
#    return abs(x-y)<1e-4 