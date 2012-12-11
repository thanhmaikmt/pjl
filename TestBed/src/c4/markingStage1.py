import c4board
import os
import glob


players={}

class Player:
    
    def __init__(self):
        pass
        self.record=[]



"""
    p1 is being marked
    
    return W for win reported
           w     win not reported
           L     etc
           ?     for some sort of error
"""
def markgame(f,p1,p2):
    
    opo={p1:p2,p2:p1}
    pover={p1:' ',p2:' '}
            
    b=c4board.Board()
    
    fin=open(f,"r")
    toMove=None
    state=' '
    color=None
    
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
                pover[player]="? : Played out of turn against "+opop
                continue
            
            if state != ' ':
                pover[player]="? : Played after game over against "+opop
                continue
            
               
            col=int(toks[1][1:])
            
            if col < 0 or col > 6:
                pover[player]="? : Played illegal move against "+opop
                continue
            
            b.do_move(col)
            #print b
            
            toMove=opo[toMove]
            
            state=b.state();
            if state != ' ':
                print p1,p2,state
                
        elif toks[1][0] == 'w':
    
            if color == None:
                pover[player]="?  : claiming win without moving against "+opop
                continue
                        
            col = color[player]
     
            if pover[player] != ' ':
                pover[player]="? : naughty additional claim against "+opop       
            elif state == ' ':
                pover[player]="? : Invalid win claim for unfinished game against "+opop   
            elif state[0] != col:
                pover[player]="? : Invalid win claim for lost game against "+opop
            else:
                pover[player]='W : win against '+opop
                
        elif toks[1][0] == 'l':
            
            col = color[player]
            
            if pover[player] != ' ':
                pover[player]="? : Naughty additional claim against "+opop       
            elif state == ' ':
                pover[player]="? : Invalid lose claim for unfinished game against "+opop   
            elif state[0] == col:
                pover[player]="? : Invalid lose claim for won game against "+opop
            else:
                pover[player]='L : lose against '+opop
            
            
    if pover[p1]==' ':
        if color == None:
            pover[p1]='? : wtf against '+p2
            
        elif color[p1] == state:
            pover[p1]="w : unclaimed win against " +p2
        elif  color[p2] == state:
            pover[p1]="l : unreported lose against " +p2
        elif state=='D':
            pover[p1]="d : unreported draw against " +p2
        else:
            pover[p1]="?   unfinished game against " +p2
            
    if pover[p2]==' ':
        if color == None:
            pover[p2]='? : wtf against '+p1
        elif color[p2] == state:
            pover[p2]="w : unclaimed win against " +p1
        elif  color[p1] == state:
            pover[p2]="l : unreported lose against " +p1
        elif state=='D':
            pover[p2]="d : unreported draw against " +p1
        else:
            pover[p2]="?   unfinished game against " +p1
            
        
               
    return pover
            
# directory to log stuff
myHomeDir=os.getcwd()

myHomeDir="/home/c4/public_html/marking/"
#myHomeDir="/home/c4/public_html/server/"

logDir=os.path.join(myHomeDir,"c4gamelog")
resultDir=os.path.join(myHomeDir,"results")



files=glob.glob(logDir+"/*")
    
    
    
students=[]

for f in files:
    print f

    toks=f.split('/')
    g=toks[-1]
    toks=g.split('_')
    p1=toks[0]
    p2=toks[1]

    if players.get(p1) == None:
        players[p1]=Player()
        students.append(p1)
        
    if players.get(p2) == None:
        players[p2]=Player()

    pover=markgame(f,p1,p2)
    
    #print pover
    
    players[p1].record.append(pover[p1])
    #players[p2].record.append(pover[p2])
    
    

for p in students:
    
    print "******",p,"****************************************************"
    
    fnameresult=os.path.join(resultDir,p)
    fresult=open(fnameresult,'w')
    
    reportOK=True
    noError=True
    
    for res in  players[p].record:
        fresult.write(res+"\n")
        
        if res[0] =='?':
            noError=False
            reportOK=False
        
        elif res[0] == 'w' or res[0] == 'l' or res[0] =='d':
            reportOK=False
             
        else:
            if res[0] == 'W' or res[0] == 'L' or res[0] =='D':  
                pass
            else:
                print ">",res,"<"
                
    fresult.write("***********************************\n")
    
    fresult.write(" Summary     \n")

    if noError:
        fresult.write(" Plays legally :  ")
    else:
        fresult.write(" Does not plays legally  :  ")
        
    if reportOK:
        fresult.write(" Reports status OK  \n")
    else:
        fresult.write(" Does not report status correctly \n")
        
#print pover


