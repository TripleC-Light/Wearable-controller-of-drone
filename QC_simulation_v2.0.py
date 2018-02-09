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
    lineWidth = 5.0
    elasticity = 1
    friction = 1
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = (0,0)
    topLimit = pymunk.Segment(body, ( 0, dh), ( dw, dh), lineWidth)
    topLimit.elasticity = elasticity
    topLimit.friction = friction
    bottomLimit = pymunk.Segment(body, ( 0, 0), ( dw, 0), lineWidth)
    bottomLimit.elasticity = elasticity
    bottomLimit.friction = friction
    leftLimit = pymunk.Segment(body, ( 0, 0+lineWidth), ( 0, dh-lineWidth), lineWidth)
    leftLimit.elasticity = elasticity
    leftLimit.friction = friction
    rightLimit = pymunk.Segment(body, ( dw, 0+lineWidth), ( dw, dh-lineWidth), lineWidth)
    rightLimit.elasticity = elasticity
    rightLimit.friction = friction
    space.add(topLimit, bottomLimit, leftLimit, rightLimit, body)
    
    return topLimit,bottomLimit
   
def main():
    disWidth = 600
    disHeight = 600
    radius = 10
    bodyPos = 0
    tmpTarget = 0
    Target = 400
    
    Kp = 2
    Ki = 0
    Kd = 2
    pidx = PID.PID(Kp, Ki, Kd)
    pidx.setVtarget = disWidth/2
    pidx.setWindup(100)
    
    pidy = PID.PID(Kp, Ki, Kd)
    pidy.setVtarget = Target
    pidy.setWindup(100)
    ##-- Control system setting --##
    cMax = 255
    cStep = 13

    gravityX = 0
    gravityY = -cMax
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
                            mouse_x = pos[0]
                            mouse_y = pos[1]
                            print 'mouse_x=' + str(mouse_x)
                            print 'mouse_y=' + str(mouse_y)
                            pidy.setVtarget = disHeight - mouse_y
                            pidx.setVtarget = mouse_x
                        elif index == 1:
                            print 'The mouse wheel Pressed!'
                        elif index == 2:
                            print 'Pressed RIGHT Button!'

        
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]
        pidy.setVtarget = disHeight - mouse_y
        pidx.setVtarget = mouse_x            
        pidx.update(shape.body.position.x)
        gravityX = pidx.output
        if(gravityX>cMax):
            gravityX = cMax
        if(gravityX<-cMax):
            gravityX = -cMax
        gravityX = round((gravityX/cStep))*cStep
        
        pidy.update(shape.body.position.y)
        gravityY = pidy.output
        if(gravityY>cMax):
            gravityY = cMax
        if(gravityY<-cMax):
            gravityY = -cMax
        gravityY = round((gravityY/cStep))*cStep
        
        space.gravity = (gravityX, gravityY)
        space.step(1/50.0)

        screen.fill((255,255,255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    (main())
