
""" receiving OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation
"""


import OSC
import time, threading
import socket

def run(wrapper):
    
    
    
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
         if not ip.startswith("127."):
             break
         
         
    print ip
         
         

    # tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
    receive_address = '127.0.0.1', 7110
    receive_address = '192.168.0.8', 7110
    receive_address = '192.168.43.96', 7110
    receive_address = '169.254.250.186', 7110
    receive_address = ip, 7110
    
    
    
    
    # OSC Server. there are three different types of server. 
    s = OSC.OSCServer(receive_address) # basic
    ##s = OSC.ThreadingOSCServer(receive_address) # threading
    ##s = OSC.ForkingOSCServer(receive_address) # forking
    
    
    
    # this registers a 'default' handler (for unmatched messages), 
    # an /'error' handler, an '/info' handler.
    # And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
    s.addDefaultHandlers()
    
    
    
    # define a message-handler function for the server to call.
    def printing_handler(addr, tags, stuff, source):
        print "---"
        print "received new osc msg from %s" % OSC.getUrlStr(source)
        print "with addr : %s" % addr
        print "typetags %s" % tags
        print "data %s" % stuff
        print "---"
    
     # define a message-handler function for the server to call.
    def accel_handler(addr, tags, stuff, source):
        wrapper.set_accel(stuff[0],stuff[1],stuff[2])
    
    # define a message-handler function for the server to call.
    def xy_handler(addr, tags, stuff, source):
        
        wrapper.set_xy(stuff[0],stuff[1])
        return
    
        print "---"
        print "received new osc msg from %s" % OSC.getUrlStr(source)
        print "with addr : %s" % addr
        print "typetags %s" % tags
        print "data %s" % stuff
        print "---"
    
    # define a message-handler function for the server to call.
    def push1_handler(addr, tags, stuff, source):
        
        toks=addr.split('/')
        key=toks[-1]
        wrapper.set_push1(int(key),stuff[0])
        return
    
        print "---"
        print "received new osc msg from %s" % OSC.getUrlStr(source)
        print "with addr : %s" % addr
        print "typetags %s" % tags
        print "data %s" % stuff
        print "---"
    
    
    # define a message-handler function for the server to call.
    def push2_handler(addr, tags, stuff, source):
        toks=addr.split('/')
        key=toks[-1]
        wrapper.set_push2(int(key),stuff[0])
        return
    
        
        print "---"
        print "received new osc msg from %s" % OSC.getUrlStr(source)
        print "with addr : %s" % addr
        print "typetags %s" % tags
        print "data %s" % stuff
        print "---"
    
    # define a message-handler function for the server to call.
    def null_handler(addr, tags, stuff, source):
       pass
    
    def add_push_handlers(root,callback,n):
        s.addMsgHandler(root+"z", null_handler) # adding our function
        
        for i in range(n):
            s.addMsgHandler(root+"1/"+str(i), callback) # adding our function
    
    
    s.addMsgHandler("/print", printing_handler) # adding our function
    s.addMsgHandler("/accxyz", accel_handler) # adding our function
    s.addMsgHandler("/ping", null_handler) # adding our function
    
    add_push_handlers("/1/multipush2/", push2_handler,12) # adding our function
    add_push_handlers("/1/multipush1/", push1_handler,12) # adding our function
    
    s.addMsgHandler("/1/xy1/", xy_handler) # adding our function
    
    
    # just checking which handlers we have added
    print "Registered Callback-functions are :"
    for addr in s.getOSCAddressSpace():
        print addr
    
    
    # Start OSCServer
    print "\nStarting OSCServer. Use ctrl-C to quit."
    st = threading.Thread( target = s.serve_forever )
    st.start()
    
  
    xx = raw_input(" Hit CR TO QUIT")

    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    
    st.join() ##!!!
    print "Done"
    
if __name__ == "__main__":
    class Wrapper:
        
        def set_push1(self,i,val):
            print "set tonality",i,val
#            if val > 0:
#                score.set_tonality(music.tonalities[((i-1)*5)%7])

        def set_xy(self,x,y):
            print "set xy",x,y
            
        def set_accel(self,x,y,z):
            print "accel ",x,y,z
            
            
        def set_push2(self,i,val):
            vel=int(val*100)       
#            pitch=score.get_tonality().get_note_of_scale(i,score.key)+36
            print "play",i,vel
#            
#            if vel != 0:
#                solo_inst.note_on(pitch,vel)
#            else:
#                # schedule the note off
#                playable = music.Playable(music.NoteOff(pitch), solo_player)
#                seq.add_after(.1, playable)




    w=Wrapper()
    run(w)
            
            