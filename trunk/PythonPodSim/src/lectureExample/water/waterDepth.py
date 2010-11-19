import sys
from copy import deepcopy

state=[0,0]  # state[0]  is 3l    state[1] is 4l
history=[]   # keep a record of the moves

class Move1:
    def do(self):
        history.append([deepcopy(state),"fill 4l"])
        state[1]=4

    def isValid(self):
        return state[1] < 4


class Move2:
    def do(self):
        history.append([deepcopy(state),"fill 3l"])
        state[0]=3

    def isValid(self):
        return state[0] < 3

class Move3:
    def do(self):
        history.append([deepcopy(state),"empty 4l"])
        state[1]=0

    def isValid(self):
        return state[1] > 0

class Move4:
    def do(self):
        history.append([deepcopy(state),"empty 3l"])
        state[0]=0

    def isValid(self):
        return state[0] > 0


class Move5:    
    def do(self):
        history.append([deepcopy(state),"3l into 4l"])
        avail=4-state[1]
        amount=min(avail,state[0])
        state[1] = state[1] + amount
        state[0] = state[0] - amount

    def isValid(self):
        return state[0] > 0 and state[1] < 4



class Move6:   
    def do(self):
        history.append([deepcopy(state),"4l into 3l"])
        avail=3-state[0]
        amount=min(avail,state[1])
        state[0] = state[0]+amount
        state[1] = state[1]-amount

    def isValid(self):
        return state[1] > 0 and state[0] < 3


moves=[Move1(),Move2(),Move3(),Move4(),Move5(),Move6()]
visited=[state]


def done():
    for x in history:
        print x
    sys.exit(0)    

def explore():
    
    global state,history,visited

    for move in moves:
        if move.isValid():
     
            move.do()
     
            if state[1]==2 :
                done()
        
            if not state in visited:
                visited.append(deepcopy(state))
                explore()

            # undo the state       
            state=history[len(history)-1][0]
            history.pop()
            
     

explore()
print "FAILED TO FIND GOAL"






