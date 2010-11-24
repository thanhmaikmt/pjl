import sys
from copy import deepcopy
from visuals import *

state=[0,0]  # state[0]  is 3l    state[1] is 4l
history=[]   # keep a record of the moves

class Move1:
    def do(self):
        history.append([deepcopy(state),"fill 4l"])
        state[1]=4
        self.name="->4"

    def isValid(self):
        return state[1] < 4


class Move2:
    def do(self):
        history.append([deepcopy(state),"fill 3l"])
        state[0]=3
        self.name="->3"

    def isValid(self):
        return state[0] < 3

class Move3:
    def do(self):
        history.append([deepcopy(state),"empty 4l"])
        state[1]=0
        self.name="4->"


    def isValid(self):
        return state[1] > 0

class Move4:
    def do(self):
        history.append([deepcopy(state),"empty 3l"])
        state[0]=0
        self.name="3->"

    def isValid(self):
        return state[0] > 0


class Move5:    
    def do(self):
        history.append([deepcopy(state),"3l into 4l"])
        avail=4-state[1]
        amount=min(avail,state[0])
        state[1] = state[1] + amount
        state[0] = state[0] - amount
        self.name="3->4"

    def isValid(self):
        return state[0] > 0 and state[1] < 4



class Move6:   
    def do(self):
        history.append([deepcopy(state),"4l into 3l"])
        avail=3-state[0]
        amount=min(avail,state[1])
        state[0] = state[0]+amount
        state[1] = state[1]-amount
        self.name="4->3"

    def isValid(self):
        return state[1] > 0 and state[0] < 3


file_name="depthOrder1.ps"
moves=[Move1(),Move2(),Move3(),Move4(),Move5(),Move6()]


#file_name="depthOrder2.ps"
#moves=[Move4(),Move5(),Move6(),Move1(),Move2(),Move3()]


#file_name="depthOrder3.ps"
#moves=[Move2(),Move3(),Move4(),Move5(),Move6(),Move1()]

visited=[deepcopy(state)]


def done():
    print " Solution ---- "
    for x in history:
        print x
    printTree(file_name,root)        
    sys.exit(0)
    
    
# this is to draw the tree (cosmetic)
class Node:

    hash_count=-1

    def __init__(self,parent,move,state):

        Node.hash_count=Node.hash_count+1
        self.hash=Node.hash_count
        self.visit_hash=self.hash
        self.parent=parent
        self.move=move
        self.label_str="("+str(state[0])+","+str(state[1])+")"

        self.state=[state[0],state[1]]   # copy current state
        if not parent == None:
            parent.children.append(self)
        self.children=[]
      #self.stat=UNKNOWN  

    def label(self):
        return self.label_str

    def shapeOf(self):
        return "ellipse"

    
      
def explore():
    
    print "explore---"
    global state,history,visited,current

    for move in moves:
        if move.isValid():
            
            move.do()
            
            if not state in visited:
                print history[len(history)-1]
                current=Node(current,move,state)
                visited.append(deepcopy(state))
                if state[0]==2 and state[1] == 0:
                    done()
            
                explore()
                
            # undo the state       
            state=history[len(history)-1][0]
            history.pop()
            
    current=current.parent
    print "---backtrack"
     

root=Node(None,None,state)
current=root

explore()












