from pygraphviz import *


def printTree(file,root):
    tree=buildTree(root)
    tree.layout(prog='dot')
    tree.draw(file) # ,prog='circo')


#def shapeOf(node):
#   if node.board.status==Status.UNDECIDED:
#      return 'ellipse'
#   elif node.board.status==Status.MAX:
#      return 'triangle'
#   else:
#      return 'box'

def buildTree(root):
   tree=AGraph()    
   tree.add_node(root.hash)
   n=tree.get_node(root.hash)
   n.attr['label']=root.label()
   n.attr['shape']=root.shapeOf()
   buildVisual(root,tree)
   return tree

def buildVisual(parent,tree):

#   print parent.hash," ",
   for child in parent.children:
      tree.add_edge(parent.hash,child.hash);
      n=tree.get_node(child.hash)
      n.attr['label']=child.label();

      e=tree.get_edge(parent.hash,child.hash);
      e.attr['label']=child.move.name

#      if child.master != None:
#         n.attr['label']="*"+child.board.label()
#      else:
#         n.attr['label']=child.board.label()

      n.attr['shape']=child.shapeOf()
      
      buildVisual(child,tree)
#   print

