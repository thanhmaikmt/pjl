
""" 
Make a stream from a whole directory of files 
"""
 
class MultiFileStream:
    
    def __init__(self,dir,file_name_client):
    
        import glob
        self.client=file_name_client
        
        self.fn_iter=glob.glob(dir+"/*.txt").__iter__()
        self.fin=None
        self.next_file()
        
    def next_file(self):
        
        print " NEXT FILE  . . ."
        self.file_name=self.fn_iter.next()
        print self.file_name
        
        if self.client:
            self.client.notify(self.file_name)
            
        print "XX" 
        if self.file_name:
            print "YY"
            if self.fin:
                self.fin.close()
            print " opening", self.file_name
            self.fin=open(self.file_name,"r")
            
            if not self.fin:
                print "oops could not open"
        else:   
            self.fin=None
        
    def readline(self):
        if self.fin == None:
            return None
        
        while True:
            line=self.fin.readline()
            if line:
                return line
            
            self.next_file()
            
            if not self.fin:
                return None
            
            
            
