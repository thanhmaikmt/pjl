import numpy
import util
        
"""
static int y1 = 0, y2 = 0, x[26], n = 12;
int y0;
x[n] = x[n + 13] = data;
y0 = (y1 << 1) - y2 + x[n] - (x[n + 6] << 1) + x[n + 12];
y2 = y1;
y1 = y0;
y0 >>= 5;
if(--n < 0)
n = 12;
return(y0);
"""
class LPF:
    
    def __init__(self):
        self.y1 = 0
        self.y2 = 0
        self.x=numpy.zeros(26)
        self.n = 12
        
    
    def process(self,data):
    
        self.x[self.n] = self.x[self.n + 13] = data;
        y0 = 2*self.y1 - self.y2 + self.x[self.n] - (2*self.x[self.n + 6]) + self.x[self.n + 12];
        self.y2 = self.y1
        self.y1 = y0
        y0 *= 32
        self.n -= 1
        if self.n < 0:
            self.n = 12
        return y0

"""
static int y1 = 0, x[66], n = 32;
int y0;
x[n] = x[n + 33] = data;
y0 = y1 + x[n] - x[n + 32];
y1 = y0;
if(--n < 0)
n = 32;
return(x[n + 16] - (y0 >> 5));
}
"""
        
class HPF:
    
    def __init__(self):
        self.y1 = 0
        self.x=numpy.zeros(66)
        self.n = 32
    
    def process(self,data):
    
        self.x[self.n] = self.x[self.n + 33] = data;
        y0 = self.y1 + self.x[self.n] - self.x[self.n + 32]
        self.y1 = y0;
        self.n -=1
        if self.n < 0:
            self.n = 32
        return self.x[self.n+16]-y0/32.0


"""
int Derivative(int data)
{
int y, i;
static int x_derv[4];
/*y = 1/8 (2x( nT) + x( nT - T) - x( nT - 3T) - 2x( nT -  4T))*/
y = (data << 1) + x_derv[3] - x_derv[1] - ( x_derv[0] << 1);
y >>= 3;
for (i = 0; i < 3; i++)
x_derv[i] = x_derv[i + 1];
x_derv[3] = data;
return(y);
"""
class Dervivative:
    
    def __init__(self):
        self.y = 0
        self.i = 0
        self.x_derv=numpy.zeros(4)
  
    def process(self,data):
    
        y = 2*data + self.x_derv[3] -self.x_derv[1]- 2*self.x_derv[0]
        y = y/8
        self.x_derv[0]=self.x_derv[1]
        self.x_derv[1]=self.x_derv[2]
        self.x_derv[2]=self.x_derv[3]
        self.x_derv[3]=data
        return y

"""
static int x[32], ptr = 0;
static long sum = 0;
long ly;
int y;
if(++ptr == 32)
ptr = 0;
sum -= x[ptr];
sum += data;
x[ptr] = data;
ly = sum >> 5;
if(ly > 32400) /*check for register overflow*/
y = 32400;
else
y = (int) ly;
return(y);
"""

class MovingAverge:
    
    def __init__(self):
        self.sum = 0
        self.ptr = 0
        self.x=numpy.zeros(32)
  
    def process(self,data):
    
        self.ptr+=1
        if self.ptr== 32:
            self.ptr=0
        self.sum -= self.x[self.ptr]
        self.sum += data
        self.x[self.ptr]=data
        
        return self.sum/32.0


class MovingAvergeN:
    
    def __init__(self,N):
        self.sum = 0.0
        self.ptr = 0
        self.x=numpy.zeros(N)
        self.N=N
  
    def process(self,data):
    
        self.ptr+=1
        if self.ptr == self.N:
            self.ptr=0
        self.sum -= self.x[self.ptr]
        self.sum += data
        self.x[self.ptr]=data
        
        return self.sum/self.N

class MovingDecayAverge:
    
    def __init__(self,N):
        self.sum = 0.0
        self.ptr = 0
        self.fact1,self.fact2=util.halfLifeFactors(N)
        
  
    def process(self,data):
    
        self.sum=self.sum*self.fact1+data*self.fact2
        return self.sum
    
    
class Delay:
    
    
    def __init__(self,N):
        
        self.buff=numpy.zeros(N)
        self.N=N
        self.ptr=0
        
        
    def process(self,data):
        
        ret=self.buff[self.ptr]
        self.buff[self.ptr]=data
        self.ptr+=1
        
        if self.ptr == self.N:
            self.ptr=0
            
        return ret
        
    

