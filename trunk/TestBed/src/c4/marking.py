import c4board
import os
import glob


players={}

class Player:
    
    def __init__(self):
        pass
        self.record=[]

def markgame(f,p1,p2):
    
    opo={p1:p2,p2:p1}
    pover={p1:' ',p2:' '}
        
    
    
    
    b=c4board.Board()
    
    fin=open(f,"r")
    toMove=None
    state=' '
    for line in fin:
        #print line
        toks=line.split(':')
        player=toks[0]
        opop=opo[player]
        
        if toks[1][0] == 'm':
        
            if pover[player] != ' ':
                continue
            
            if toMove == None:
                toMove=toks[0]
                color={toMove:b.to_move,opo[toMove]:c4board.opo[b.to_move]}
            elif player != toMove:
                pover[player]="?Played out of turn:"+opop
                continue
            
            if state != ' ':
                pover[player]="?Played after game over against: "+opop
                continue
            
        
            
            col=int(toks[1][1:])
            b.do_move(col)
            #print b
            
            toMove=opo[toMove]
            
            state=b.state();
            #if state != ' ':
            #    print state
                
        elif toks[1][0] == 'w':
            
            col = color[player]
     
            if pover[player] != ' ':
                pover[player]="?w naughty additional claim:"+opop       
            elif state == ' ':
                pover[player]="?w Invalid win claim for unfinished game:"+opop   
            elif state[0] != col:
                pover[player]="?w Invalid win claim for lost game:"+opop
            else:
                pover[player]='W:'+opop
                
        elif toks[1][0] == 'l':
            
            col = color[player]
            
            if pover[player] != ' ':
                pover[player]="?l  Naughty additional claim:"+opop       
            elif state == ' ':
                pover[player]="?l  Invalid lose claim for unfinished game:"+opop   
            elif state[0] == col:
                pover[player]="?l Invalid lose claim for won game:"+opop
            else:
                pover[player]='L:'+opop
            
            
            
    return pover
            
# directory to log stuff
myHomeDir=os.getcwd()
logDir=os.path.join(myHomeDir,"c4gamelog")

files=glob.glob(logDir+"/*")



    

for f in files:
    toks=f.split('/')
    g=toks[-1]
    toks=g.split('_')
    p1=toks[0]
    p2=toks[1]

    if players.get(p1) == None:
        players[p1]=Player()

    if players.get(p2) == None:
        players[p2]=Player()

    pover=markgame(f,p1,p2)
    
    #print pover
    
    players[p1].record.append(pover[p1])
    players[p2].record.append(pover[p2])
    
    

for p in players:
    
    print p,">", players[p].record
    
#print pover


