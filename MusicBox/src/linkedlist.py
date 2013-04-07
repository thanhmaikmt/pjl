#! /usr/bin/env python

class Node:
    
    def __init__(self,time,data,next=None):
        self.data = data  # contains the data
        self.tick = time
        self.next = next # contains the reference to the next node
        #self.tick = data.tick
        
    def _insert_after(self,time,data):
        assert time >= self.tick
        assert not self.next or self.next.tick >= time
        
        new_node = Node(time,data,self.next) # create a new node
        self.next=new_node
         
     
class OrderedLinkedList:
    
    """
       Linked List of nodes with data : 
       data must be comparable with <
       TODO: delete nodes
    """
       
    
    def __init__(self):
        self.head=None
        
    

    def insert(self,time,data):
        """
        create a new Node with data 
        insert into list so it is assending order
        """
        
        if self.head == None:
            self.head=Node(time,data,None)
            return
        
        ptrPrev=None
        ptrNext=self.head
        
        while ptrNext != None and  ptrNext.tick <= time:
            ptrPrev=ptrNext
            ptrNext=ptrNext.next
           
        
        #  ptr.data <     
        if ptrPrev == None:
            self.head=Node(time,data,self.head)
        else:
            ptrPrev._insert_after(time,data)
   
       
    def __iter__(self):
        return LinkedListIterator(self)
    
    def debug(self):
          for x in self:
              print (x.data)


class LinkedListIterator:
    
    """
     Insertions after current position are OK
    """
    
    def __init__(self,mylist):
        self.list=mylist
        self.current=None
        
        #print "Hello"
  
    def next(self):
        
        #print "Next"
        # if list is empty we need this
        if self.current == None:
            self.current=self.list.head
            return self.current
        
        
        mynext=self.current.next
        
        if mynext == None:
            raise StopIteration
        
        self.current=mynext
           
        return mynext
     

if __name__ == "__main__":
            
   
    mylist=OrderedLinkedList()
    mylist.insert(3,"31")           
    mylist.insert(1,1)
    mylist.insert(5,5)
    mylist.insert(0,0)
    mylist.insert(2,2)
    mylist.insert(3,"32")            
 
    mylist.debug()
    
    
##    mylist.insert(5)
#    

#    
#    print "---------------------"
#    for x in mylist:
#        print x.data.mess
#        if x.data.tick == 3:
#            mylist.insert(Data(4,4))