import sys
from visuals import *
from copy import *

state=[0,0]               # state[0]  is 3l    state[1] is 4l
UNKNOWN,FAIL,DONE=range(3)

class Node:

    hash_count=-1

    def __init__(self,parent,move,state):

        Node.hash_count=Node.hash_count+1
        self.hash=Node.hash_count
        self.visit_hash=self.hash
        self.parent=parent
        self.move=move
        self.label_str="("+str(state[0])+","+str(state[1])+")"

        self.state=deepcopy(state)   # copy current state
        if not parent == None:
            parent.children.append(self)
        self.children=[]
        self.stat=UNKNOWN

    def label(self):
        return self.label_str

    def shapeOf(self):
        return "ellipse"
                   # if state[1] == 2:
                   #     done(child)
class Move1:
    
    def __init__(self):
        self.name="->4l"

    def do(self):
        state[1]=4

    def isValid(self):
        return state[1] < 4


class Move2:
    def __init__(self):
        self.name="->3l"

    def do(self):
        state[0]=3

    def isValid(self):
        return state[0] < 3

class Move3:
    def __init__(self):
        self.name="4l->"
 
    def do(self):
        state[1]=0

    def isValid(self):
        return state[1] > 0

class Move4:
    def __init__(self):
        self.name="3l->"

    def do(self):
        state[0]=0

    def isValid(self):
        return state[0] > 0


class Move5:    
    def __init__(self):
        self.name="3l->4l"

    def do(self):
        avail=4-state[1]
        amount=min(avail,state[0])
        state[1] = state[1] + amount
        state[0] = state[0] - amount

    def isValid(self):
        return state[0] > 0 and state[1] < 4



class Move6:   
    def __init__(self):
        self.name="4l->3l"

    def do(self):
        avail=3-state[0]
        amount=min(avail,state[1])
        state[0] = state[0]+amount
        state[1] = state[1]-amount

    def isValid(self):
        return state[1] > 0 and state[0] < 3


file_name="breadthMoveOrder2"
#moves=[Move1(),Move2(),Move3(),Move4(),Move5(),Move6()]
moves=[Move2(),Move3(),Move1(),Move4(),Move5(),Move6()]
visited=[deepcopy(state)]


def done(leaf):
    while leaf.parent != None:
        print leaf.move.name,"  ", leaf.state
        leaf=leaf.parent
        

def explore(depth,node):
    # print "explore",depth,node.state

    global state,history,visited

    if depth == 0:

        # we are on a leaf so expand the node
        for move in moves:
            #state=deepcopy(state)
            if move.isValid():
                move.do()
             #  print "add1", state
           
                if not state in visited:
                    print "add2", state
                    child=Node(node,move,state)
                    visited.append(deepcopy(child.state))
                    node.children.append(child)
                    if state[0]==2 and state[1]==0:
                        done(child)
                        return DONE
       
                state=deepcopy(node.state)
                
         
        if len(node.children) == 0:
            return FAIL

        return UNKNOWN
 
 
    for child in node.children:
            if child.stat == FAIL:
                continue
            state=deepcopy(node.state)
            child.move.do()
            # print state

        
            stat=explore(depth-1,child)
            if stat == FAIL:
                child.stat=FAIL
            if stat== DONE:
                return DONE
            

    if len(node.children) == 0:
            return FAIL

    return UNKNOWN
    

root=Node(None,None,state)
global_depth=0
   
while  True:
    print "Exploring to depth:" ,global_depth
    stat=explore(global_depth,root)
    if  stat== DONE or stat == FAIL:
        break
    global_depth=global_depth+1


printTree(file_name+".ps",root)







