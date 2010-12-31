'''
Created on 21 Dec 2010

@author: pjl
'''

import pygame as pg
       
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
            
            
                                
            keyinput = pg.key.get_pressed()
        
            # speed up/down  display      
            if keyinput[pg.K_KP_PLUS] or keyinput[pg.K_EQUALS]:
                sim.frameskipfactor = sim.frameskipfactor+1
                print "skip factor" ,sim.frameskipfactor
            
            if keyinput[pg.K_MINUS]:
                sim.frameskipfactor = max(1,sim.frameskipfactor-1)
                print "skip factor" ,sim.frameskipfactor

    # display the performance of the best pod in pool
         #   if  keyinput[pg.K_c]:
         #       pool.proven_list=[]
            
            
            if pool == None:
                return
             
            if pool.reaping and log_file!=None and pool.touched:
                log_file.write(str(sim.ticks) +','+ str(pool.best_fitness())+','+str(pool.average_fitness())+'\n')
                pool.touched=False
                
                    
            # display the performance of the best pod in pool
            if  keyinput[pg.K_b]:
                
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
            if  keyinput[pg.K_p]:
                
                
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
            if not pool.reaping and keyinput[pg.K_r]:
                del pods[:]
                pods.extend(self.pods_copy)
                pool.reaping=True

            # save the pool to a file
            if keyinput[pg.K_s]:
                POOL_FILE_NAME=sim.run_name+".pool"
                file=open(POOL_FILE_NAME,"w")
                pool.save(file)
                file.close()
                
            # reload the pool from a file
            if keyinput[pg.K_l]:
                POOL_FILE_NAME=sim.run_name+".pool"
                file=open(POOL_FILE_NAME,"r")
                pool.load(file)
                file.close()