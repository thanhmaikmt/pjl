
class Scenario:
    
    def __init__(self,id):
        self.id=id
        self.cases=[]
             
    def appendCase(self,case):
        self.cases.append(case)