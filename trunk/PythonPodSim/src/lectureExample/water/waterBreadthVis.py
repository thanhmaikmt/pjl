import sys
from visuals import *
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

        self.state=[state[0],state[1]]   # copy current state
        if not parent == None:
            parent.children.append(self)
        self.children=[]
        self.stat=UNKNOWN

    def label(self):
        return self.label_str

    def shapeOf(self):
        return "ellipse"

    def expand(self):

        print "expand", self.state,depth
        global state

        for move in moves:
            state=[self.state[0],self.state[1]]
            if move.isValid():
                move.do()
                print "add1", state
           
                if not state in visited:
                    print "add2", state
                    child=Node(self,move,state)
                    visited.append(child.state)
                    self.children.append(child)
                    if state[1] == 2:
                        done(child)
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


moves=[Move1(),Move2(),Move3(),Move4(),Move5(),Move6()]
visited=[state]


def done(leaf):
    while leaf.parent != None:
        print leaf.move.name,"  ", leaf.state
        leaf=leaf.parent
        

def explore(depth,node):
    # print "explore",depth,node.state

    global state,history,visited

    if depth == 0:
        node.expand()
        if len(node.children) == 0:
            return FAIL

        return UNKNOWN
 
 
    for child in node.children:
            if child.stat == FAIL:
                continue
            state=[node.state[0],node.state[1]]
            child.move.do()
            # print state

            if state[1]==2 :
                done(child)
                return DONE

            stat=explore(depth-1,child)
            if stat == FAIL:
                child.stat=FAIL
            if stat== DONE:
                return DONE
            

    if len(node.children) == 0:
            return FAIL

    return UNKNOWN
    

root=Node(None,None,state)
depth=0
   
while  explore(depth,root) != DONE:
    print "Exploring to depth:" ,depth
    depth=depth+1


printTree("finalTree.ps",root)


print "FAILED TO FIND GOAL"






