
import math

def calc(x11,y11,x12,y12,x21,y21,x22,y22,np):
    
    dx1=(x12-x11)/np
    dx2=(x22-x12)/np
    dy1=(y12-y11)/np
    dy2=(y22-y12)/np
    
    x1=x11+dx1/2.0
    y1=y11+dy1/2.0
    x2s=x21+dx2/2.0
    y2s=y21+dy2/2.0
    
    for _1 in range(np):
        
        x2=x2s
        y2=y2s
        for _2 in range(np):  
            dx=x2-x1
            dy=y2-y1
            r=math.sqrt(dx**2+dy**2)
            