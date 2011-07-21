from simulation import *
import pygame 

class CursorControl:

    def process(self,sensor,state,dt):
        control=Control()
        keyinput = pygame.key.get_pressed()

        if keyinput[pg.K_LEFT]:
            control.left=1

        if keyinput[pg.K_RIGHT]:
            control.right=1

        if keyinput[pg.K_UP]:
            control.up=1

        if keyinput[pg.K_DOWN]:
            control.down=1

        return control

