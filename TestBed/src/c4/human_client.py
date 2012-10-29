import client
import c4board
import settings

def get_human_move(board):
    print board
    mess=raw_input("Enter move : ")
    col=int(mess)
    return col

def brag(state,my_col):

    if state == 'd':
        print " DRAW !" 
    elif state == my_col:
        print " WIN :-)"
    else:
        print " LOSE :-("
        
        
name = raw_input("Enter name :")
    
client.connect(settings.host,settings.port,name)


while True:    
    board=c4board.Board()
    print " Your options are \n", \
        " g XXX       game with XXX they move first\n",\
        " G XXX       game with XXX you move first\n",\
        " L           list who is logged on \n",\
        " q           quit \n",\
        " W           wait for a challenge "
        
    cmd = raw_input(" command:")
    client.send(cmd)
     
    
    
    if len(cmd) == 0:
        continue

    if cmd[0] == 'W':
        my_col=client.wait_for_game()
        state=client.play_a_game(my_col,board,get_human_move)
        brag(state,my_col)
        
    elif cmd[0] == 'g':
        mess=client.get_message()
        print mess
        if mess[0] == '!':
            my_col=c4board.opo[board.to_move]
            state=client.play_a_game(my_col,board,get_human_move)
            brag(state,my_col)
        
    elif cmd[0] == 'G':
        my_col= board.to_move
        state=client.play_a_game(my_col,board,get_human_move)
        brag(state,my_col)
                
    elif cmd[0] == 'q':
        break
    
    elif cmd[0] == 'L':
        who=client.get_player_list()
        for w in who:
            print w
        
client.cleanup()
        
        
        
    