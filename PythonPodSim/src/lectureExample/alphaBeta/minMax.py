#from board import *

from visuals import *
from readNet import *

INF=10000

class Node:

   icount=0
   visit_count=0

   def __init__(self):
      self.hash=Node.icount   # only used for display / debug
      Node.icount=Node.icount+1
      self.val=None
      self.children=[]  # offspring
      self.visit_hash=0   # > 0 is visited

   def addChildX(self,child):
         self.children.append(child)
         child.partent=self

   def shapeOf(self):
      if self.visit_hash > 0:
         return 'box'
      else:
         return 'ellipse'


class MaxNode(Node):

   def __init__(self):
      Node.__init__(self)

   def label(self):
      if self.val == None:
         return " "   # inf"
      else:
         return str(self.val)

   def update(self):


      for c in self.children:
         self.val=max(c.val,self.val)

   def addChild(self):
      child=MinNode()
      self.addChildX(child)
      return child

class MinNode(Node):

   def __init__(self):
      Node.__init__(self)
      self.val=INF

   def label(self):
      if self.val == None:
         return " "   # inf"
      else:
         return str(self.val)

   def update(self):
      for c in self.children:
         self.val=min(c.val,self.val)  

   def addChild(self):
      child=MaxNode()
      self.addChildX(child)
      return child

nodes=[]

root=MaxNode()

readNet("net4.txt",root)

printTree("initialTree.ps",root)



def updateMinMax(node):

   # print " visite : " ,node.hash

   node.visit_hash=Node.visit_count
   Node.visit_count=Node.visit_count+1

   if node.children==None:
      return

   else:
      for c in node.children:
         updateMinMax(c)
      node.update()
      # print " update :" , node.hash,node.val

updateMinMax(root)

printTree("finalTree.ps",root)


