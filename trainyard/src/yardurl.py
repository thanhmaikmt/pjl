
import urllib,re
from world import *
from defs import *


 

def decode_goal(string,ptr,posC,w):
        
            ptr+=1
            val1=intFromChar(string[ptr])
            
            sideList=[]
          
            if val1 >=8:
                sideList.append(3)
                val1 -=8
           
            if val1 >= 4:
                sideList.append(2)
                val1 -=4
                
            if val1 >= 2:
                sideList.append(1)
                val1 -=2
           
            if val1 == 1:
                sideList.append(0)
            
            ptr+=1
            val2=intFromChar(string[ptr])
            ncolors=val2+1
        
            cnt=0
            
            colourList=[]
            
            for _ in range((ncolors-1)/2+1):
                ptr+=1
                charValue=intFromChar(string[ptr])
                #rint charValue
                c1=charValue/7
                colourList.append(c1)
                cnt+=1
                if cnt == ncolors:
                    break
                c2=charValue%7
                colourList.append(c2)
                cnt+=1
              
            #print piece[c],":", "sides=",sideList,"colours=",ncolors,colourList
            goal=Goal(w.cells[posC],sideList,colourList)
            #w.goals.append(goal)
            ptr  += 1
            posC += 1
            return ptr,posC



def decode_outlet(string,ptr,posC,w):
        
            
            colourList=[]
            ptr+=1
            val1=intFromChar(string[ptr])
            
            sideInt=(val1/9)
         
            ncolour=(val1%9)+1
            
            #rint "Ncolor=",ncolour
                 
            cnt=0                 
            for _ in range((ncolour-1)/2+1):
                ptr+=1
                charValue=intFromChar(string[ptr])
                #rint charValue
                c1=charValue/7
                
                colourList.append(c1)
                
                cnt+=1
                if cnt == ncolour:
                    break
                
                c2=charValue%7
                colourList.append(c2)
                cnt+=1
                
            #print sideInt
            #print piece[c],":", "sides=",sides[sideInt],"colours=",colourList
            o=OutLet(w.cells[posC],sideInt,colourList)
            
            ptr  += 1
            posC += 1
            return ptr,posC
        
def decoder(string):
    
    n = len(string)
    
    width=intFromChar(string[0])
    height=intFromChar(string[1])
    
    
    print "Size is:",width,height
    
    w=World(width,height)
    
    gene=w.blank_gene()
    
    ptr=2
    
    posC=0
    solution=False
    
    while ptr < n:
        c=string[ptr]
        
        if c == '_':
            solution=True
            ptr+=1
            posC=0
            continue
        
     
        
        if c == '0':
            posC+=10
            ptr+=1
            continue
        
        else:
            inc=ord(c)-ord('0')
            if inc < 10 and inc > 0:
                posC += inc
                ptr+=1
                #print posC
                continue

        pos=Pos(posC,w.width)
        
        
        if solution:
            #print "track(",pos.x,",",pos.y,")=",c
            #trk=Track(w.cells[posC],segments_from_type[c],c)
            gene.str[posC]=char_from_id.index(c)
            #w.tracks.append(trk)
            ptr+=1
            posC+=1
            continue
                 
        
        #print c
    
        
        if c == 'S':
            ptr+=1
            side=intFromChar(string[ptr])
            ptr+=1
            split=Splitter(w.cells[posC],side)
            #w.splitters.append(split)
            posC+=1
          
            
            
        elif c == 'G':
            ptr,posC=decode_goal(string,ptr,posC,w)
            
        elif c == 'O':
            ptr,posC=decode_outlet(string,ptr,posC,w)
            
        elif c == 'P':
            ptr+=1
            cval=intFromChar(string[ptr])
            ptr+=1
            sval=intFromChar(string[ptr])
            
            sideA=sval/7
            sideB=sval%7
            p=Painter(w.cells[posC],sideA,sideB,cval)
            
            #w.painters.append(p)
            ptr  += 1
            posC += 1

        elif c=='R':
            #print " Rock"
            r=Rock(w.cells[posC])
            ptr+=1
            posC += 1
      
    print gene.str
    
          
    return w,gene
        
        
def worldFromUrl(url):
    for line in url:
        #print line
        if 'ys:"' in line:
            print line
            x=re.findall('"([^"]*)"',line)
            return decoder(x[0])
    
    
if __name__ == "__main__":
    
    puzzle='2ey6e'

    # Get something to work with.
    url = urllib.urlopen("http://trainyard.ca/"+puzzle)
    worldFromUrl(url)
    