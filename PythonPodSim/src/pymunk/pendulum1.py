import sys, random
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk


def draw_lines(screen, lines):
    for line in lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle) # 1
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1) # 2
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2])


def add_L(space):
    anchor = pymunk.Body(pymunk.inf, pymunk.inf) # 1
    anchor.position = (300,300)
    
    body1 = pymunk.Body(10, 100) # 2
    body1.position = (350,300)    
    seg1 = pymunk.Segment(body1, (-50, 0), (50.0, 0.0), 5.0)
    
    
    body2= pymunk.Body(10, 100)
    body2.position = (450,300)
    seg2 = pymunk.Segment(body2, ( -50.0, 0), (50.0, 0.0), 5.0)
    
    anchor_body1_pin = pymunk.PinJoint(body1, anchor, (-50,0), (0,0)) # 3    
    body1_body2_pin  = pymunk.PinJoint(body1, body2, (50,0), (-50,0)) # 3    

   # mass=pymunk.Body(10000,10)
   # mass.position = (600,300)
 
   # rotation_center_joint2 = pymunk.PinJoint(body, mass, (0,0), (0,0)) # 3
    
    space.add(seg1, body1, anchor_body1_pin,seg2,body1_body2_pin,body2) # mass,rotation_center_joint2) # 4
    return seg1,seg2

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()
    running = True
    
    #pymunk.init_pymunk()
    space = pymunk.Space()
    space.gravity = (0.0, -10.0)
    
    lines = add_L(space)
    
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
        

        screen.fill(THECOLORS["white"])
        
        
        draw_lines(screen, lines)
        pygame.draw.circle(screen, THECOLORS["red"],(300,300), 5)
        
        space.step(1/50.0)
        
        pygame.display.flip()
        clock.tick(50)
        
if __name__ == '__main__':
    sys.exit(main())
    