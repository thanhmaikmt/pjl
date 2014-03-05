

def matches(g,H):
    for a,b in zip(g,H):
        if b == '*':
            continue
        
        if a != b:
            return False
       
    return True    
    

    
def order_len(H):
    first=None
    last=None
    order=0
    for count in range(len(H)):
        x=H[count]
        if x == '*':
            continue
        
        if first == None:
            first=count
        last=count
        order+=1
        
    n = last-first
    return n,order
    
pop=[['0101110011',9],
     ['1100100111',7],
     ['0100100011',6],
     ['0101100010',5],
     ['0100000000',3],
     ['0101110010',2],
     ['0000100010',1],
     ['0001100110',0]]

H1='*10**1****'
H2='*****00*11'

fit_tot=0.0
for g in pop:
    fit_tot+=g[1]
    
print " Total fitness =",fit_tot

print 'prob select',pop[4][0],' =',pop[4][1]/fit_tot 

print " Order Len H1", order_len(H1)
print " Order Len H2", order_len(H2)


print "genes with ",H1
fit_H1=0.0
for x in pop:
    if matches(x[0],H1):
        print "           ",x[0]
        fit_H1+=x[1]
        
print " prob H1 select=",fit_H1/fit_tot