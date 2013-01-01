charList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_";


def intFromChar(c):
    return charList.index(c)

piece={'R':'Rock','O':'outlet','P':'painter','G':'goal','S':'splitter'}


#  enumerate sides
sides={0:'t',1:'r',2:'b',3:'l'}

#  helper to get position of mid point
midside={0:(.5,0),1:(1,0.5),2:(0.5,1),3:(0,0.5)}

# vertices 
vert=[(0,0),(1,0),(1,1),(0,1)]

# arcs for each vertex
seglim=[(270,90),(180,90),(90,90),(0,90)]


# edge  maps  a side to its local vertices
edge={0:(0,1),1:(1,2),2:(2,3),3:(3,0)}


# Track segment types    in terms of the 2 sides. 
# if it's and arc 3rd item is the vertex to draw arc around
"""         0-tr     1-tb  2-tl    3-rb   4-rl    5-bl     side side pivot  """
seg_sides=[(0,1,1), (0,2),(0,3,0),(1,2,2),(1,3),(2,3,3)]
          
segments_from_type={'J':(1,),'C':(3,),'h':(0,),'v':(5,),'V':(4,1),'j':(0,2),'o':(2,),
                 'U':(4,3),'B':(5,4),'Q':(4,),'t':(2,1),'z':(5,3),'l':(0,3),'N':(1,3),
                 'M':(1,5),'u':(2,4),'R':(4,0),'A':(5,1),'L':(1,2),'D':(3,0),'P':(4,1)}

def nextClock(x):
    return (x+1)%4

def nextAnti(x):
    return (x+3)%4

colour_name={0:'red',1:'yellow',2:'blue',3:'orange',4:'green',5:'purple'}