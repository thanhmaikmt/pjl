'''
Created on 19 Jul 2011

@author: pjl

Demonstrate how to find the k nearest distances

'''


BIG=1e32                 # bigger than any distance we are likely to encounter
k=6                      # number of nearest to look at
min_table=k*[(BIG,-1)]   # table of    [distance,output]   pairs 

minval=1e32                      
        
        
# add a single pair if distance is less than any already stored
def add(dist,out):
    for i in range(k):         # go through the table
        if dist < min_table[i][0]:              # if distance less than a value already stored
            min_table.insert(i,[dist,out])      # insert new pair
            min_table.pop()                     # discard the last entry to keep list size equal to k
            return

    
def debug():
    print " DEBUG --------------- "
    for i in range(k):
        print min_table[i][0],min_table[i][1]
        

# test data pairs of distances and values in parallel arrays
dists = [4,5,2,1,6,7,8,9,1,20]
outs  = [1,0,2,3,4,0,2,5,2,4]
            
# loop on data pairs and construct the minimal distance table
for i in range(len(dists)):
        add(dists[i],outs[i])
        debug()  
        

# Now construct a dictionary that contains the number occurances of any output
dict={}     #    output  ->  no of occurances
for i in range(k):                   # iterate on the minimum table
        out=min_table[i][1]          
        count=dict.get(out)           
        if count == None:           # if this output  is not in dictionary
            dict[out]=1             # add an entry with count of 1
        else:
            dict[out]=dict[out]+1   # otherwise increment the count
        
print dict


# Now look in the dictionary to find the  output that occurs the most times
max_occurances=0
val=None

for out in dict:
    if dict[out] > max_occurances:
        max_occurances=dict[out]
        val=out

# Phew 
# Print output value that occurs the most times in the k nearest list.
print val
            

