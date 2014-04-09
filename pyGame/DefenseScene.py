import pygame
from pygame.locals import *

import Scene
import Box2D
from Box2D.b2 import *
from Enum import *
from sys import exit

class DefenseScene(Scene.Scene):

    PPM=20.0
    TARGET_FPS=60
    TIME_STEP=1.0/TARGET_FPS
    VELOCITY_ITERATIONS=10
    POSITION_ITERATIONS=10
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT=600

    ground = None
    dynamic_body = None
    world = None
    clock = None

    def DefenseScene(screen):
        self.screen = screen

    def prepare(self):        
        self.world=world(gravity=(0,-10),doSleep=True)
        self.ground=self.world.CreateStaticBody(position=(0,1), shapes=polygonShape(box=(50,5)))
        self.dynamic_body=self.world.CreateDynamicBody(position=(10,15), angle=15)
        self.dynamic_body.CreatePolygonFixture(box=(2,1), density=1, friction=0.3)

        self.clock = pygame.time.Clock()

    def step(self):
        self.screen.fill((0,0,0,0))
        for body in self.world.bodies:
            for fixture in body.fixtures:
                self.computeAndDraw(body, fixture)

        self.world.Step(self.TIME_STEP, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)
        self.world.ClearForces()
        pygame.display.flip()
        self.clock.tick(self.TARGET_FPS)

        for event in self.eventQueue:
            if event.type==KEYDOWN and event.key==K_ESCAPE:
                self.state = STATE.STOPPED
                self.stop()

    def computeAndDraw(self, body, fixture):
        colors = {
            staticBody  : (255,255,255,255),
            dynamicBody : (127,127,127,255),
        }

        #proby nadania ruchu obiektom
        #vel = body.linearVelocity()
        #vel.x = 5
        #body.linearVelocity(vec2(50, 50))

        vertices=[(body.transform * v) * self.PPM for v in fixture.shape.vertices]
        vertices=[(v[0], self.SCREEN_HEIGHT - v[1]) for v in vertices]
        pygame.draw.polygon(self.screen, colors[body.type], vertices)

    def dispose(self):
        for body in self.world.bodies:
            self.world.DestroyBody(body)
        for joint in self.world.joints:
            self.world.DestroyJoint(joint)






##            while not self.endOfLoop:
##            for event in pygame.event.get():
##                if event.type==QUIT:
##                    self.gameExit()
##                elif event.type==KEYDOWN and event.key==K_ESCAPE:
##                    self.endOfLoop=True
##                    self.clearMemory()

