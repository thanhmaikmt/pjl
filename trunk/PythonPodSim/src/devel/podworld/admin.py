'''
Created on 21 Dec 2010

@author: pjl
'''

import gui
       
class Admin:  # use me to control the simulation
              # see comments to see what key hits do
        
    def process(self,sim):   
        
            # this is called just before each time step
            # do admin tasks here

            # global pods
            agents=sim.agents
            pool=sim.pool
            world=sim.world
            log_file=sim.log_file
            
            
                                
            keyinput = gui.get_pressed()
        
            # speed up/down  display      
            if keyinput[gui.keys.K_KP_PLUS] or keyinput[gui.keys.K_EQUALS]:
                sim.frameskipfactor = sim.frameskipfactor+1
                print "skip factor" ,sim.frameskipfactor
            
            if keyinput[gui.keys.K_MINUS]:
                sim.frameskipfactor = max(1,sim.frameskipfactor-1)
                print "skip factor" ,sim.frameskipfactor

    # display the performance of the best pod in pool
         #   if  keyinput[gui.keys.K_c]:
         #       pool.proven_list=[]
            
            
            if pool == None:
                return
             
            if pool.reaping and log_file!=None and pool.touched:
                if len(pool.list) > 0:
                    log_file.write(str(sim.ticks) +','+ str(pool.list[0].dom)+'\n')
                pool.touched=False
                
                    
            if keyinput[gui.keys.K_z]:
                pool.debug("Z")
                
            # display the performance of the best pod in pool
            if  keyinput[gui.keys.K_b]:
                
                if pool.reaping:    # if reaping copy existing to allow restore
                    self.pods_copy=copy(pods)
                    pod=pods[0]
                    del pods[:]
                    pods.append(pod)
                else:
                    pod=pods[0]
                    
                plug.init_pod(pod,world)    
                pod.control.brain=pool.create_best()
                pool.reaping=False
             
            # display the performance of the most proven pod
            if  keyinput[gui.keys.K_p]:
                
                
                if pool.reaping:    # if reaping copy existing to allow restore
                    self.pods_copy=copy(pods)
                    pod=pods[0]
                    del pods[:]
                    pods.append(pod)
                else:
                    pod=pods[0]
                    
                    
                world.init_pod(pod)
                pod.ang += random()-0.5    # randomize the intial angle
                pod.control.brain=pool.create_most_proven()
                pool.reaping=False   
                
            # go back into evolution mode after looking at best pod   
            if not pool.reaping and keyinput[gui.keys.K_r]:
                del pods[:]
                pods.extend(self.pods_copy)
                pool.reaping=True

            # save the pool to a file
            if keyinput[gui.keys.K_s]:
                POOL_FILE_NAME=sim.run_name+".pool"
                file=open(POOL_FILE_NAME,"w")
                pool.save(file)
                file.close()
                
            # reload the pool from a file
            if keyinput[gui.keys.K_l]:
                POOL_FILE_NAME=sim.run_name+".pool"
                file=open(POOL_FILE_NAME,"r")
                pool.load(file)
                file.close()