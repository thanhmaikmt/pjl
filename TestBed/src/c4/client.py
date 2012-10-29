import socket
import sys
import signal
import Queue

import c4board
import random
import time
#import atexit

disp=True
cleaned=False

def connect(host,port,name):
    global client_socket,rque,buff ,messq   
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
   
    # Catch some signals
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
   # atexit.register(cleanup)
    rque  = Queue.Queue()
    messq = Queue.Queue()
    buff = ""
#                if self.opo != None:
#                    #self.opo.send(data[0])
#                    self.opo.opo=None
#                    self.opo=None
 
 
 def logon(name):
     send(name)
     
# Keyboard Interrupt handler and cleanup routine
def cleanup(*args):
    global client_socket,cleaned
    if cleaned:
        return
    print " Cleaning up "
    # Close the client socket
    client_socket.send("\n") 
    client_socket.send("a") 
    time.sleep(1)
    client_socket.close()
    client_socket = None
    print " Bye bye"
    cleaned=True
    #sys.exit(-1)
              
def send(data):
    client_socket.send(data + "\n")    
       
def send_move(col):
    data = "m " + str(col)
    send(data)    


def get_message():
    if rque.empty():
        replenish()
    mess = rque.get()
    return mess
    
def get_player_list():
    who=[]
    send("L")

    while True:
        mess=get_message()
        print mess
        if mess[0] == '+':
            who.append(mess[1:].strip())
        if mess[0] == '$':
            return who
    
    
        
def replenish():
    global buff,rque,connected
    try:
        data = client_socket.recv(512)
            #print "!"+data+"!"
                    
        if len(data) == 0:
            print " len(data) == 0 in recieve "
            rque.put("q")
            connected = False
                
        for c in data:
            if c == '\n':
                mess = buff.strip()
                rque.put(mess)
                buff = ""
            else:
                buff += c
                                         
    except:
        print " Exception in receive "
        #rque.put("q")
        cleanup()
       
                             
             
def get_opo_move():
    global opo_aborted
    while True:
        mess = get_message()
        if mess[0] == 'm':
            return int(mess[2:])
        if mess[0] == 'a':
            opo_aborted=True
            return -1
        
        messq.put(mess)
         
def wait_for_game(board):
    global opo_aborted
    opo_aborted=False
    while True:
        if rque.empty():
            replenish()
        mess = rque.get()
        
        print mess
        
        if mess[0]=='G':
            my_color=c4board.opo[board.to_move]
            return my_color
        elif mess[0] == 'g':
            my_color=board.to_move
            return my_color
        
        messq.put(mess)
    
    
def check_for_game_end(board,my_color):
    state=board.state()
    if state == ' ':
        return ' '   
            
    if state[0] == my_color:
        send("w")
    elif state[0] == 'd':
        send("d")
    else:
        send("l")
         
    return state[0]
        

    
def get_message():
        if rque.empty():
            replenish()
        mess = rque.get()
        return mess
          
def play_a_game(my_color,board,get_my_move):
        
        global opo_aborted
        opo_aborted=False
          
        if disp:
            print  "Game: to_move: ",my_color
            print board
                
                           
        while True:
    
            if opo_aborted:
                print "opo aborted"
                return 'a';
            
            if board.to_move != my_color:
                col=get_opo_move()
            else:
                col=get_my_move(board)
                send_move(col)
                 
                            
            board.do_move(col)
            
            if disp:
                print board
                
            state=check_for_game_end(board,my_color)
            
            if state[0] !=  ' ':
                return state[0]
