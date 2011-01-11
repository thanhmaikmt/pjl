import pygame as pg
from fontmanager import *
from math  import *
from util import *

keys=pg
 
 
def Rect():
    return pg.Rect()


def init_surface(dim_world):
    
        pg.init()
        modes=pg.display.list_modes()
        dim_display=modes[0]
        global fontMgr,display,dim_window
        sx=dim_display[1]/float(dim_world[1])
        sy=dim_display[0]/float(dim_world[0])
        
        if sx < 1 or sy < 1:
            s=min(sx,sy)/1.2
            dim_window=(dim_world[0]*s,dim_world[1]*s)
            print "Small screen: scaling world by ",s

        else:
            dim_window=dim_world

        display = pg.display.set_mode(dim_window)
        pg.display.set_caption('PodSim (press escape to exit)')
        fontMgr = cFontManager(((None, 20), (None, 48), ('helvetica', 24)))
        return pg.Surface(dim_world) #
 
def get_pressed():
    return pg.key.get_pressed()


def draw_string(screen,str1,point,col,size ):
    fontMgr.Draw(screen, None, size,str1,point, col) 



def clock():
    
   return pg.time.Clock() 

def check_for_quit():
    keyinput = pg.key.get_pressed()

    if keyinput[pg.K_ESCAPE] or pg.event.peek(pg.QUIT):
                pg.display.quit()
                return True
            
    return False
            
def grab_events():
    pg.event.pump()
               
def blit(screen):
        zz=pg.transform.scale(screen,dim_window)
        display.blit(zz,(0,0))
        pg.display.flip()
        
      
def draw_world(self,screen):
        if not self.blind:
            for wall in self.walls:
                if "start" in wall.name:
                    col=(255,255,0)
                elif "end" in wall.name:
                    col=(0,255,255)
                else:
                    col=(0,0,255)

                for seg in wall.segments:
                    pg.draw.line(screen,col,(seg[0],seg[1]),(seg[2],seg[3]),6)
        
            col=(100,30,30)
            for t in self.trips:
                pg.draw.line(screen,col,t[0],t[1],2)
                
        
        
        for pod in self.pods:
            pod.draw(screen)
                # raise SystemExit

def draw_pod(self, screen):
        
        state=self.state
        
        if state.collide:
            state.collide_count=100

        outline=rotate_poly(self.pod_poly_ref, state.ang, state)
        
        if state.collide_count>0:
            col=(255,100,100)
            state.collide_count -= 1
        else:
            col=self.col
        pg.draw.polygon(screen,col,outline)
        
        if self.control == None:
            return
        
        if self.control.up > 0.0:
            outline=rotate_poly(self.thrust_poly_ref, state.ang, state)
            pg.draw.polygon(screen,red,outline)
        if self.control.left > 0.0:
            outline=rotate_poly(self.left_poly_ref, state.ang, state)
            pg.draw.polygon(screen,red,outline)
        if self.control.right > 0.0:
            outline=rotate_poly(self.right_poly_ref, state.ang, state)
            pg.draw.polygon(screen,red,outline)

def draw_sensors(self,screen):
        
        state=self.state
        for sensor in self.sensors:
            wallName=sensor.wall
            if wallName== None:
                col=(10,10,10)
            elif "end" in wallName:
                col=(255,255,255)
            else:
                col=(70,70,70)

            dist=sensor.val
            
            p1=(state.x,state.y)
            p2=(state.x+dist*sin(sensor.ang),state.y+dist*cos(sensor.ang))
            pg.draw.line(screen,col,p1,p2,1)
