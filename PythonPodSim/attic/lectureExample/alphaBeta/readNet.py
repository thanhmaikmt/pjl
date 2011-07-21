def readNet(file_name,root):

    nodes=[]

    nodes.append(root)

    f = open(file_name,"r")
    line=f.readline()
    nLayer=int(line)

    iparent=0

    parent=nodes[iparent]
    #print parent

    for l in range(nLayer):
       line=f.readline()
       toks=line.split()
       for t in toks:
          n_child=int(t)
          for i in range(n_child):
             #print parent
             child=parent.addChild()
             nodes.append(child)

          iparent=iparent+1
          parent=nodes[iparent]



    line=f.readline()
    toks=line.split()

    for t in toks:
       nodes[iparent].val=int(t)
       iparent=iparent+1


    return nodes[0]
