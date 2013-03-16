#! /usr/bin/env python

class Node:
    def __init__(self,data,next):
        self.data = data # contains the data
        self.next = next # contains the reference to the next node

    def insert_after(self,data):
        
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
        
        while ptrNext != None and  ptrNext.data < data:
            ptrPrev=ptrNext
            ptrNext=ptrNext.next
           
        
        #  ptr.data <     
        if ptrPrev == None:
            self.head=Node(data,self.head)
        else:
            ptrPrev.insert_after(data)
   
       
    def __iter__(self):
        return LinkedListIterator(self)

class LinkedListIterator:
    
    
    def __init__(self,mylist):
        self.list=mylist
        self.mynext=self.list.head
        #print "Hello"
  
    def next(self):
        
        
        #print "Next"
        # if list is empty we need this
        if self.mynext == None:
            raise StopIteration
        
        ret=self.mynext
        
        self.mynext=ret.next
       
        #print ret
        
        return ret
     

if __name__ == "__main__":
    mylist=LinkedList()
    nn=Node(1,None)
    nn.insert_after(2)
    nn.insert_after(3)
    nn.next.insert_after(4)
    
    
    while nn:
        print nn.data
        nn=nn.next
        
        
    
    print "-------"
    mylist.insert(3)            
    mylist.insert(1)
    mylist.insert(5)
    mylist.insert(0)
    mylist.insert(2)


    
#    mylist.insert(5)
    
    for x in mylist:
        print x.data
        