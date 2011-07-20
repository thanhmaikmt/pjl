'''
Created on 21 Dec 2010

@author: pjl
'''

from math import *

huge=1e6
        
def rotate_poly(poly,ang,pos):
    ret=[]
    for p1 in poly:
        x=p1[0]*cos(ang)+p1[1]*sin(ang)+pos.x
        y=-p1[0]*sin(ang)+p1[1]*cos(ang)+pos.y
        ret.append((x,y))
    return ret


def dist(x1,y1,x2,y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)

def limit(x,min,max):
    if x > max:
        return 1
    elif x < min:
        return min
    else:
        return x


def read_points(fin):

    points=[]
    while True:
            line = fin.readline()
            if line[0] == '#':
                continue
                
            if line.isspace() or len(line)==0:
                return points

            toks = line.split(',')
            for tok in toks:
             #   print tok
                if len(tok) != 0 and not tok.isspace():
                    points.append(float(tok))



#  t is distance from p0 to p1
#  s is distance from p2 to p3
def intersect_numpy(p0_x,p0_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y):
    
    
        # scalar    
        s1_x = p1_x - p0_x
        s1_y = p1_y - p0_y
        
        # arrays
    
        s2_x = p3_x - p2_x
        s2_y = p3_y - p2_y

        # array
        fact = (-s2_x * s1_y + s1_x * s2_y)

        #       s       s     a        s       s     a 
        s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) /fact
        
        #       a      s       a       a       s      a
        t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) /fact 

        return (s,t,fact)

#  t is distance from p0 to p1
#  s is distance from p2 to p3
#def intersect2(p0_x,p0_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y):
#    
#
#        s1_x = p1_x - p0_x
#        s1_y = p1_y - p0_y
#        s2_x = p3_x - p2_x
#        s2_y = p3_y - p2_y
#
#        fact = (-s2_x * s1_y + s1_x * s2_y)
#
#    
#        s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) 
#        t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) 
#
#        return (s,t,fact)


#  t is normalized distance from p0 to p1
#  s is normalized distance from p2 to p3
def intersect(p0_x,p0_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y):
    

        s1_x = p1_x - p0_x
        s1_y = p1_y - p0_y
        s2_x = p3_x - p2_x
        s2_y = p3_y - p2_y

        fact = (-s2_x * s1_y + s1_x * s2_y)

        if fact == 0:
            return (huge,huge,0)

        s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / fact
        t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / fact

        return (s,t,fact)
