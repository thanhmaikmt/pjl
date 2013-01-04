charList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_";


def intFromChar(c):
    return charList.index(c)

piece={'R':'Rock','O':'outlet','P':'painter','G':'goal','S':'splitter'}


#  enumerate sides
sides=('t','r','b','l')

#  helper to get position of mid point
midside=((.5,0),(1,0.5),(0.5,1),(0,0.5))

# vertices 
vert=((0,0),(1,0),(1,1),(0,1))

# arcs for each vertex
seglim=((270,90),(180,90),(90,90),(0,90))


# edge  maps  a side to its local vertices
edge=((0,1), (1,2),(2,3),(3,0))


# Track segment types    in terms of the 2 sides. 
# if it's and arc 3rd item is the vertex to draw arc around
"""         0-tr     1-tb  2-tl    3-rb   4-rl    5-bl     side side pivot  """
seg_sides=((0,1,1), (0,2),(0,3,0),(1,2,2),(1,3),(2,3,3))
          
segments_from_type={'h':(0,),          'm':(0,1),'j':(0,2),'l':(0,3),'n':(0,4),'k':(0,5),
                    'J':(1,),'K':(1,0),          'L':(1,2),'N':(1,3),'P':(1,4),'M':(1,5),
                    'o':(2,),'p':(2,0),'t':(2,1),          'E':(2,3),'u':(2,4),'r':(2,5),
                    'C':(3,),'D':(3,0),'H':(3,1),'s':(3,2),          'I':(3,4),'F':(3,5),  
                    'Q':(4,),'R':(4,0),'V':(4,1),'S':(4,2),'U':(4,3),          'T':(4,5),
                    'v':(5,),'w':(5,0),'A':(5,1),'x':(5,2),'z':(5,3),'B':(5,4)            }


char_from_id=' hmjlnkJKLNPMoptEurCDHsIFQRVSUTvwAxzB'

segments_by_id=(None,(0,),      (0,1),(0,2),(0,3),(0,4),(0,5),
                     (1,),(1,0),      (1,2),(1,3),(1,4),(1,5),
                     (2,),(2,0),(2,1),      (2,3),(2,4),(2,5),
                     (3,),(3,0),(3,1),(3,2),      (3,4),(3,5),  
                     (4,),(4,0),(4,1),(4,2),(4,3),      (4,5),
                     (5,),(5,0),(5,1),(5,2),(5,3),(5,4)       )

def nextClock(x):
    return (x+1)%4

def nextAnti(x):
    return (x+3)%4

colour_name={0:'red',1:'yellow',2:'blue',3:'orange',4:'green',5:'purple',6:'brown'}

split_colour={0:(0,0),1:(1,1),2:(2,2),3:(0,1),4:(1,2),5:(0,2),6:(6,6)}

mix_colours=[[0,3,5,6,6,6,6],
             [3,1,4,6,6,6,6],
             [5,4,2,6,6,6,6],
             [6,6,6,3,6,6,6],
             [6,6,6,6,4,6,6],
             [6,6,6,6,6,5,6],
             [6,6,6,6,6,6,6]]


