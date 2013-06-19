import numpy
import math


        
u0=math.pi*4e-7


def kernel2D(r):
    return -math.log(r)


def calc(x11,y11,x12,y12,x21,y21,x22,y22,np,kernel):
    
    lenx1=x12-x11
    lenx2=x22-x21
    leny1=y12-y11
    leny2=y22-y21
    len1=math.sqrt(lenx1**2+leny1**2)
    len2=math.sqrt(lenx2**2+leny2**2)
    
    area=len1*len2
    
    darea=area/(np*np)

    const=darea*u0/2.0/math.pi
    
    dlen=math.sqrt(darea)
    dtol=dlen*0.01
    dsing=dlen/4.0
    
    dx1=lenx1/np
    dx2=lenx2/np
    dy1=leny1/np
    dy2=leny2/np
    
    x1s=x11+dx1/2.0
    y1s=y11+dy1/2.0
    x2s=x21+dx2/2.0
    y2s=y21+dy2/2.0
    
    sum=0.0
    for i in range(np):
        
        x1=x1s+i*dx1
        y1=y1s+i*dy1
        
        for j in range(np):
              
            x2=x2s+j*dx2
            y2=y2s+j*dy2
            
            dx=x2-x1
            dy=y2-y1
          #  print i,j,dx,dy

            r=math.sqrt(dx**2+dy**2)
            
            if r > dtol: 
                term=const*kernel(r)
            else:
                term=const*kernel(dsing)
            sum+=term
            
    return sum



class Strip:
    
    def __init__(self,xA,xB,yA,yB,n):
        self.xA=xA
        self.xB=xB
        self.yA=yA
        self.yB=yB
        self.length=math.sqrt((xA-xB)**2+(yB-yA)**2)
        self.dlen=self.length/n
        self.n=n
        
    def make_M(self,np): 
        
        ##print xA,xB
        #print yA,yB
        xA=self.xA
        xB=self.xB
        yA=self.yA
        yB=self.yB
        n=self.n
        
        dx=(xB-xA)/n
        dy=(yB-yA)/n
        
        
        M=numpy.zeros(shape=(n,n))
        
        for i in range(n):
            x11=xA+i*dx
            x12=x11+dx
            y11=yA+i*dy
            y12=y11+dy
            for j in range(n):
                x21=xA+j*dx
                x22=x21+dx
                y21=yA+j*dy
                y22=y21+dy
                K=calc(x11,y11,x12,y12,x21,y21,x22,y22,np,kernel2D)    
                M[i][j]=K
            
            
        return M
        
        
        



    
if __name__ == "__main__":
    
    
    
    len=1.0
    theta=0.5
    cos_theta=math.cos(theta)
    sin_theta=math.sin(theta)
    
    xA=10.0
    xB=xA+len*cos_theta
    yA=10.0
    yB=yA+len*sin_theta
    n=1
   
    np=50
    
    for np in range(1,200):
    
        strip=Strip(xA,yA,yA,yB,n)        
        M=strip.make_M(np) 
        print np,M
        