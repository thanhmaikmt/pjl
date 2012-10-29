import random

OK=0
ILLEGAL=-1

NCOL=7
NROW=6

opo={'R':'Y','Y':'R'}

class Board:
    
    
    
    def __init__(self):
        
        self.board=[NCOL*[' ']  for _ in range(NROW)]
        self.to_move='R'
        

        
        
    def __str__(self):
        
        str=" 0 1 2 3 4 5 6 \n"
        for row in reversed(self.board):
            str+="|"
            for c in row:
                str+=c+"|"
            str+="\n"
        str+=(2*NCOL+1)*"-"+"\n"
        return str  
     
        
    def do_move(self,col):
        
        for row in self.board:
            if row[col] == ' ':
                row[col]=self.to_move
                self.to_move=opo[self.to_move]
                return OK
        
        return ILLEGAL
        
        
        
    def state(self):
            
                        
        
        lines=(((0,0),(1,0),(2,0),(3,0)),    # columns
               ((0,1),(1,1),(2,1),(3,1)),
               ((0,2),(1,2),(2,2),(3,2)),
               ((0,3),(1,3),(2,3),(3,3)),
               ((0,0),(0,1),(0,2),(0,3)),    # rows
               ((1,0),(1,1),(1,2),(1,3)),
               ((2,0),(2,1),(2,2),(2,3)),
               ((3,0),(3,1),(3,2),(3,3)),
               ((0,0),(1,1),(2,2),(3,3)),    # diagonals
               ((0,3),(1,2),(2,1),(3,0)))
        
        
        for row in range(NROW-3):
            for col in range(NCOL-3):
                for line in lines:
                    prev=' '
                    count=0
                    for p in line:
                        c=self.board[row+p[0]][col+p[1]]
                         
                        if prev != ' ':
                            if c == prev:
                                count += 1
                                if count == 3:
                                    return c+" wins"
                        prev=c
           
                        
                        
        for x in self.board[NROW-1]:
            if x == ' ':
                return  ' '            
            
        return 'draw'
        
        
if __name__ == "__main__":
    
    b=Board()
    print b

    import rand_player
    
    while b.state() == ' ':
        print "\n\n"+b.__str__()
        col=rand_player.get_move(b)
        b.do_move(col)
                
    print b
    
    print b.state()