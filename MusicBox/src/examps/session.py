 class Session:
        
        def __init__(self,name):
            self.out=open(name,"w")
            
        def record(self,addr,data):
            stamp=time.time()
            str=str(time)+addr+str(data)+"\n"
            self.out.write(str)
        
        def close(self):
            self.out.close()
                
        
    class SessionPlayer:
        
        def __init__(self,name,seq,client):
            self.fin=open(name,"r")
            self.seq=seq
            self.client=client
            
        def start(self):
            self.start=time.time()
            self.toff=self.start-time
            time,self.addr,self.data=self.next()
            tnext=time+self.toff
            seq.add(tnext,self)
            
        def fire(self):
            self.client.handle(self.addr,self.data)
            self.next()
            time,self.addr,self.data=self.next()
            #  time+toff=start
            tnext=time+self.toff
            seq.add(tnext,self)
            
             
        def next(self):
            line=self.fin.readline()
            toks=line.split()
            tnext=float(toks[0])
            addr=toks[1]
            data=[]
            for x in toks[2:]:
                data.append(float(x))
            
            return time,addr,data
        
   