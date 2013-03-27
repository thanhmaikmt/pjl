#! /usr/bin/env python

class Node:
    def __init__(self,data,next=None):
        self.data = data  # contains the data
        self.tick = data.tick
        self.next = next # contains the reference to the next node
        #self.tick = data.tick
        
    def _insert_after(self,data):
        
        new_node = Node(data,self.next) # create a new node
        self.next=new_node
         
     
class OrderedLinkedList:
    
    """
       Linked List of nodes with data : 
       data must be comparable with <
       TODO: delete nodes
    """
       
    
    def __init__(self):
        self.head=None
        
    

    def insert(self,data):
        """
        create a new Node with data 
        insert into list so it is assending order
        """
        
        if self.head == None:
            self.head=Node(data,None)
            return
        
        ptrPrev=None
        ptrNext=self.head
        
        while ptrNext != None and  ptrNext.tick < data.tick:
            ptrPrev=ptrNext
            ptrNext=ptrNext.next
           
        
        #  ptr.data <     
        if ptrPrev == None:
            self.head=Node(data,self.head)
        else:
            ptrPrev._insert_after(data)
   
       
    def __iter__(self):
        return LinkedListIterator(self)
    
    


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
    
    class Data:
        def __init__(self,tick,mess):
            self.tick=tick
            self.mess=mess
            
            
    nn=Node(Data(1,1))
    nn._insert_after(Data(2,"2"))
    nn._insert_after(Data(3,3))
    nn.next._insert_after(Data(4,4))
    
    
    while nn:
        print nn.mess
        nn=nn.next
        
        
    
    print "-------"
    mylist=OrderedLinkedList()
    mylist.insert(Data(3,3))            
    mylist.insert(Data(1,1))
    mylist.insert(Data(5,5))
    mylist.insert(Data(0,0))
    mylist.insert(Data(2,2))


    
#    mylist.insert(5)
    
    for x in mylist:
        print x.mess
    
    print "---------------------"
    for x in mylist:
        print x.mess
        if x.mess == 3:
            mylist.insert(Data(4,4))