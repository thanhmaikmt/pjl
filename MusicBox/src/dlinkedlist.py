#! /usr/bin/env python

class DNode:
    
    """
    Node in a DLinkedList
    All the management is done byt he list
    """
    def __init__(self,time,data):
        self.data = data  # contains the data
        self.time = time
        
        
     
class OrderedDLinkedList:
    
    """
       Doubly Linked List of nodes with data : 
       data must be comparable with <
       TODO: delete nodes
    """
       
    
    def __init__(self):
        self.head=None
        self.tail=None
        
    

    def _insert_after(self,node,time,data):
        assert time >= node.time
        assert not node.next or node.next.time >= time
        
        newNode=DNode(time,data) # create a new node
    
        if node == self.tail:
            self.tail=newNode
        else:
            node.next.prev=newNode
    
        # new links
        newNode.prev=node
        newNode.next=node.next

        
# fix existing ptrs
        if node.next:
            node.next.prev=newNode
        
        node.next=newNode
        
    def append(self,time,data):
        if self.head == None:
            self.init(time,data)
            return

        self._insert_after(self.tail, time, data)
        
    def init(self,time,data):
            #  Epmpty list so just create the head
            self.head=DNode(time,data)
            self.head.next=None
            self.head.prev=None
            self.tail=self.head
            return
    
    def insert(self,time,data,after):
        """
        create a new Node with data 
        insert into list so it is assending order
        if after is not None we assume that time > after.time
        otherwise we have to search the whole list.

        """

        if self.head == None:
            self.init(time,data)
            return
        
        if after == None:
                # start looking from the start of the list
                ptrPrev=None
                ptrNext=self.head
        else:
            ptrPrev=None
            ptrNext=after
                
        while ptrNext != None and  ptrNext.time <= time:
            ptrPrev=ptrNext
            ptrNext=ptrNext.next
           
        
        # ptrPrev is the node just before the given time
        # it will be None if new time is before the head
        if ptrPrev == None:
            # if it is none then we replace the head
            assert ptrNext==self.head
            newNode=DNode(time,data)
            newNode.next=self.head
            newNode.prev=None
            
            self.head.prev=newNode
            self.head=newNode
            
            assert self.tail != None            
        else:
            # otherwise insert a node after ptrPrev
            self._insert_after(ptrPrev,time,data)
         
        
   
       
    def __iter__(self):
        return DLinkedListIterator(self)
    
              
                       
    def reverse(self):
        return Reversed(self)

class Reversed:
    
    def __init__(self,list):
        self.list=list
        
    def __iter__(self):
        return DLinkedListIteratorReversed(self.list)
        
        

class DLinkedListIterator:
    
    """
     Insertions after current position are OK
    """
    
    def __init__(self,mylist):
        self.list=mylist
        self.current=None
        
        #print "Hello"
  
    def seek(self,tt):
        """
        position iterator so the pointer.time is less than tt
        or None if not possible
        """
        self.current=self.list.tail    
        while self.current != None and tt > self.current.time:
            self.current=self.current.prev
            
        return self.current
    
    def peek(self):
        
        if self.current== None:
            return None
        
        return self.current.next
            
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


class DLinkedListGrazer:
    
    """
     Insertions after current position are OK
    """
    
    def __init__(self,mylist):
        self.list=mylist
        self.ptr=None
        
        #print "Hello"
  
    def seek(self,stamp):
        
        """
        position iterator so 
             ptr.time is <= stamp  AND (ptr.next == None OR  ptr.next.time > stamp)
        or None if not possible
        return the first node after tt
        """
        
        if self.list.tail == None:
            return None
        
        if self.list.tail.time <= stamp:
            self.ptr=self.list.tail
            return self.ptr
            
        if self.ptr == None:
            self.ptr=self.list.tail
            
        while self.ptr.next != None and stamp > self.ptr.next.time:
            self.ptr=self.ptr.prev
                    
                      
        return self.ptr
    
   
    def advance(self,stamp):
        """ 
        we should have already done a seek(stamp1)
        advance will return the next node after ptr providing ptr.next.time <= stamp
        the ptr is advanced 
        """
        
        assert self.ptr != None
       
        if self.ptr.next != None and self.ptr.next.time <= stamp:
            self.ptr=self.ptr.next
            return self.ptr
       
        return None

    
class DLinkedListIteratorReversed:
    
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
            self.current=self.list.tail
            return self.current
                
        mynext=self.current.prev
        
        if mynext == None:
            raise StopIteration
        
        self.current=mynext
           
        return mynext
     

if __name__ == "__main__":
            
   
    mylist=OrderedDLinkedList()
    mylist.insert(3,"31",None)           
    mylist.insert(1,1,None)
    mylist.insert(5,5,None)
    mylist.insert(0,0,None)
    mylist.insert(2,2,None)
    mylist.insert(3,"32",None)   
    mylist.insert(4.5,"float",None)         


    for x in mylist:
        print x.time,x.data
    print "=============="
    for x in mylist.reverse():
        print x.time,x.data