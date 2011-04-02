import sys, random
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk

def add_ball(space):
    mass = 1
    radius = 14
    inertia = pymunk.moment_for_circle(mass, 0, radius) # 1
    body = pymunk.Body(mass, inertia) # 2
    x = random.randint(120,380)
    body.position = x, 550 # 3
    shape = pymunk.Circle(body, radius) # 4
    space.add(body, shape) # 5
    return shape

def draw_ball(screen, ball):
    p = int(ball.body.position.x), 600-int(ball.body.position.y)
    pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 2)


def draw_lines(screen, lines):
    for line in lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle) # 1
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1) # 2
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2])

def add_static_L(space):
    body = pymunk.Body(pymunk.inf, pymunk.inf) # 1
    body.position = (300,300)    
    l1 = pymunk.Segment(body, (-150, 0), (255.0, 0.0), 5.0) # 2
    l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, 50.0), 5.0)
            
    space.add_static(l1, l2) # 3
    return l1,l2

def add_L1(space):
    rotation_center_body = pymunk.Body(pymunk.inf, pymunk.inf) # 1
    rotation_center_body.position = (300,300)
    
    body = pymunk.Body(10, 10000) # 2
    body.position = (300,300)    
    l1 = pymunk.Segment(body, (-150, 0), (255.0, 0.0), 5.0)
    l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, 50.0), 5.0)
    
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,0), (0,0)) # 3    

    space.add(l1, l2, body, rotation_center_joint) # 4
    return l1,l2

def add_L(space):
    rotation_center_body = pymunk.Body(pymunk.inf, pymunk.inf)
    rotation_center_body.position = (300,300)
    
    rotation_limit_body = pymunk.Body(pymunk.inf, pymunk.inf) # 1
    rotation_limit_body.position = (200,300)
    
    body = pymunk.Body(10, 10000)
    body.position = (300,300)    
    l1 = pymunk.Segment(body, (-150, 0), (255.0, 0.0), 5.0)
    l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, 50.0), 5.0)
    
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,0), (0,0)) 
    joint_limit = 25
    rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-100,0), (0,0), 0, joint_limit) # 2

    space.add(l1, l2, body, rotation_center_joint, rotation_limit_joint)
    return l1,l2

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
    space.gravity = (0.0, -900.0)
    
    lines = add_L(space)
    balls = []
    
    ticks_to_next_ball = 10
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
        
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        screen.fill(THECOLORS["white"])
        
        for ball in balls:
            draw_ball(screen, ball)
        
        draw_lines(screen, lines)
        pygame.draw.circle(screen, THECOLORS["red"], (300,300), 5)
        
        space.step(1/50.0)
        
        pygame.display.flip()
        clock.tick(50)
        
if __name__ == '__main__':
    sys.exit(main())
    