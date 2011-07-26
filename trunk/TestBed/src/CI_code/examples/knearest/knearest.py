'''
Created on 19 Jul 2011

@author: pjl

Demonstrate how to find the k nearest distances
Now using a class to encapsulate 

'''




class Knearest:
    
    BIG=1e32                 # bigger than any distance we are likely to encounter
               
    def __init__(self,k):
        self.min_table=k*[(Knearest.BIG,-1)]   # table of    [distance,output]   pairs 
        self.k=k
        
# add a single pair if distance is less than any already stored
    def add(self,dist,out):
        if dist > self.min_table[self.k-1][0]:
            return
        
        for i in range(self.k):         # go through the table
            if dist < self.min_table[i][0]:              # if distance less than a value already stored
                self.min_table.insert(i,[dist,out])      # insert new pair
                self.min_table.pop()                     # discard the last entry to keep list size equal to k
                return

    
    def debug(self):
        print " DEBUG --------------- "
        for i in range(self.k):
            print self.min_table[i][0], self.min_table[i][1]

    def get_knearest(self):     
        # Now construct a dictionary that contains the number occurances of any output
        dict={}     #    output  ->  no of occurances
        for i in range(self.k):                   # iterate on the minimum table
                out=self.min_table[i][1]          
                count=dict.get(out)           
                if count == None:           # if this output  is not in dictionary
                    dict[out]=1             # add an entry with count of 1
                else:
                    dict[out]=dict[out]+1   # otherwise increment the count
        # Now look in the dictionary to find the  output that occurs the most times
        max_occurances=0
        knearest=None
        
        for out in dict:
            if dict[out] > max_occurances:
                max_occurances=dict[out]
                knearest=out
        
        return knearest


def test():
    # test data pairs of distances and values in parallel arrays
    dists = [4,5,2,1,6,7,8,9,1,20]
    outs  = [1,0,2,3,4,0,2,5,2,4]
    
    k=1                     # number of nearest to look at            
    
    knearest=Knearest(k)     # create a Knearest object
    
    # loop on data pairs and construct the minimal distance table
    for i in range(len(dists)):
            knearest.add(dists[i],outs[i])
            knearest.debug()  
            
            
    print knearest.get_knearest()

    
    
if __name__ == "__main__":
    test()
    


            

