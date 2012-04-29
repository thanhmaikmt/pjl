from pyo import  *
  
class Genome:
    
    def __init__(self):
        self.generatorGenes=[]
        self.triggerGenes=[]
        self.tableGenes=[]
        self.triggerableGenes=[]
    
            

class Piece:
    
    def __init__(self):
        self.generators=[]
        self.triggers=[]
        self.triggerables=[]
        
    def play(self):
        for genome in self.generators:
            genome.out()
 
          
    
class Factory:
    
    def __init__(self):
            #print "Hello"
            
            # list of different types of pyo objects
            self.tables=[CosTable,SquareTable]
            self.generators = [FM,Sine,SineLoop] 
            self.triggers  = [Metro,Beat]
            self.trigables = [TrigEnv]
            
            
            self.lookup ={'input':[],'table':[]}
            
            
            # lookup to find a list of instances of a given object
            self.classTable=self.tables
            self.classTable+=self.generators
            self.classTable+=self.triggers
            self.classTable+=self.trigables
            #print self.classTable
        
                
                #for t in self.generators:
        #    print t
        #    print getargspec(t.__init__)
        
        
    def build(self,genome):
        p=Piece()
        
        
        
        
        # create objects that do not require parameters first
        for g in genome.generatorGenes:
            x=self.generators[g[0]]()
            p.generators.append(x)
            self.lookup['input'].append(x)
            
        for g in genome.triggerGenes:
            p.triggers.append(self.triggers[g[0]]())
        
        for g in genome.tableGenes:
            x=self.tables[g[0]]()
            p.tables.append(x)
            self.lookup['table'].append(x)
    
        print "Tables:", self.lookup['table']
        print "Inputs:",self.lookup['input']
        
            
        for g in genome.triggerableGenes:
            tt=self.trigables[g[0]]
            
            print tt,getargspec(tt.__init__)
            argspec=getargspec(tt.__init__)
            nargs=len(argspec.args)-len(argspec.defaults)-1
            
            for i in range(1,nargs+1):
                print "We need a" ,argspec.args[i],"id=",g[i]
            
        
        return p
    
    
    def build_from_code(self,snippet): 
        
            fin=open(snippet)
            self.code=fin.read()
            fin.close()
            #print code
            
            try:
                # execfile(snippet,globals(),locals())
                exec self.code
            except Exception, info:
                print "Error '%s' happened on line %d" % (info[0], info[1][1])
                
            print "------------------ x[1] -------------------"
            for x in locals().items():
                if x[0] == 'self':
                    continue
                
                cls=x[1].__class__
                
                if not cls in self.classTable:
                    print "Not in my table ",x
                    continue
                
                
                id=self.classTable.index(cls)
                pri
                    
            return locals()