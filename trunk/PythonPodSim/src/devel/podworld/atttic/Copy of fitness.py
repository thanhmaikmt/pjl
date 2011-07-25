
class Fitness:
    
    def __init__(self,goals):
        self.goals=goals
        
        self.values={}
        
        
    def set_val(self,val):
        self.values[self.goal]=val
        
        
    def next_goal(self):
        for g in self.goals:
            if self.values.__contains__(g):
                continue
            self.goal=g
            return g
        return None
    
    def to_string(self):
        ret=""
        for x in self.values:
            ret += "  "+ x.to_string() +":"+ str(self.values[x])
            
        return ret
    
    def dom_pair(self,a):
        
        
        print "hello lt"

    def __gt__(self,a):
        print "hello gt"
            
            
            