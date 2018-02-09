import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import math
sys.path.append("..\PID\Lib")
import PID

    
def add_ball(space, dw, dh, br):
    mass = 5
    radius = 10
    moment = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, moment)
    body.position = dw/2, dh-10
    shape = pymunk.Circle(body, radius, (0,0))
    shape.elasticity = 0
    shape.friction = 0
    space.add(body, shape)
    return shape

def add_L(space, dw, dh, br):
    lineWidth = 1.0
    elasticity = 0
    friction = 0
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = (dw/2,dh/2)
    topLimit = pymunk.Segment(body, ( -br-2, dw/2), ( br+2, dw/2), lineWidth*5)
    topLimit.elasticity = elasticity
    topLimit.friction = friction
    bottomLimit = pymunk.Segment(body, ( -br-2, -dw/2+5), ( br+2, -dw/2+5), lineWidth*5)
    bottomLimit.elasticity = elasticity
    bottomLimit.friction = friction
    leftLimit = pymunk.Segment(body, ( -br-2, dw/2), ( -br-2, -dw/2+5), lineWidth)
    leftLimit.elasticity = elasticity
    leftLimit.friction = friction
    rightLimit = pymunk.Segment(body, ( br+2, dw/2), ( br+2, -dw/2+5), lineWidth)
    rightLimit.elasticity = elasticity
    rightLimit.friction = friction
    space.add(topLimit, bottomLimit, body)
    
    return topLimit,bottomLimit
   
def main():
    disWidth = 600
    disHeight = 600
    radius = 10
    gravity = -900.0
    bodyPos = 0
    tmpTarget = 0
    Target = 400
    
    Kp = 2.5
    Ki = 1
    Kd = 3.0
    pid = PID.PID(Kp, Ki, Kd)
    pid.setVtarget = Target
    pid.setWindup(100)
    ##-- Control system setting --##
    cMax = 255
    cStep = 13

    pygame.init()
    pygame.key.set_repeat(10, 10)
    screen = pygame.display.set_mode((disWidth, disHeight))
    pygame.display.set_caption("Quadcopter Simulation")
    clock = pygame.time.Clock()

    space = pymunk.Space()

    lines = add_L(space, disWidth, disHeight, radius)
    
    mass = 10
    moment = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, moment)
    body.position = disWidth/2, radius/2
    shape = pymunk.Circle(body, radius, (0,0))
    shape.elasticity = 0.2
    shape.friction = 0.9
    space.add(body, shape)

    targetbody = pymunk.Body(body_type = pymunk.Body.STATIC)
    targetbody.position = (0, 0)
    targetLimit = pymunk.Segment(targetbody, ( 260, Target), ( 285, Target), 2)
    space.add(targetLimit, targetbody)
    
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            elif event.type ==  MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:
                            print 'Pressed LEFT Button!'
                            pos = pygame.mouse.get_pos()
                            mouse_y = pos[1]
                            print 'mouse_y=' + str(mouse_y)
                            pid.setVtarget = disHeight - mouse_y
                        elif index == 1:
                            print 'The mouse wheel Pressed!'
                        elif index == 2:
                            print 'Pressed RIGHT Button!'
                    
        pid.update(shape.body.position.y)
        gravity = pid.output
        if(gravity>cMax):
            gravity = cMax
        if(gravity<-cMax):
            gravity = -cMax
        gravity = round((gravity/cStep))*cStep
        #print gravity
        
        space.gravity = (0.0, gravity)
        space.step(1/50.0)

        screen.fill((255,255,255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    (main())
