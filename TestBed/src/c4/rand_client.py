import client
import c4board           
import random
import settings
import select
import tty
import termios           
import sys

def get_random_move(board):
    
    mylist=[]
    for col in range(c4board.NCOL):
        if board.board[c4board.NROW-1][col] == ' ':
            mylist.append(col)
                
    assert len(mylist) > 0
    return random.choice(mylist)          
  
def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


name = "RAND"   
 
client.connect(settings.host,settings.port,name)
 
board=c4board.Board()
my_col=client.wait_for_game(board)
client.play_a_game(my_col,board,get_random_move)

client.cleanup() 
