from visuals import *
from readNet import *

INF=10000

class Node:

   icount=0
   visit_count=-1

   def __init__(self):
      self.hash=Node.icount   # only used for display / debug
      Node.icount=Node.icount+1
      self.val=None
      self.children=[]  # offspring
      self.visit_hash=-1

   def addChildX(self,child):
         self.children.append(child)
         child.partent=self

   def shapeOf(self):
      if self.visit_hash >= 0:
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

   def visit(self,alpha,beta):

      # parent can already achieve minVal

      # print  "visit : ", self.hash,minVal,maxVal,self.val,self.children


      Node.visit_count=Node.visit_count+1
      self.visit_hash=Node.visit_count
   
    
      if len(self.children) == 0:
         return self.val

      self.val=-INF

      for c in self.children:
         valNew=c.visit(alpha,beta)

         if valNew > self.val:
            self.val=valNew

         if valNew > alpha:
            alpha=valNew
         if alpha >= beta:
            return self.val
                  
      return self.val
     
   def addChild(self):
      child=MinNode()
      self.addChildX(child)
      return child

class MinNode(Node):

   def __init__(self):
      Node.__init__(self)
      #self.val=INF

   def label(self):
      if self.val == None:
         return " "   # inf"
      else:
         return str(self.val)

   def visit(self,alpha,beta):

      # print  "visit : ", self.hash,minVal,maxVal,self.val,self.children

      Node.visit_count=Node.visit_count+1
      self.visit_hash=Node.visit_count

      if len(self.children) == 0:
         return self.val

      self.val=INF

      for c in self.children:
         valNew=c.visit(alpha,beta)

         if valNew < self.val:
            self.val=valNew

         if  valNew < beta:
            beta = valNew

         if beta <= alpha:
            return self.val

      return self.val

   def addChild(self):
      child=MaxNode()
      self.addChildX(child)
      return child


import sys

root=MaxNode()

if len(sys.argv) > 1:
   net=sys.argv[1]
else:
   net="net2"


readNet(net+".txt",root)

printTree(net+"_init.ps",root)

root.visit(-INF,INF)

printTree(net+"_final.ps",root)


