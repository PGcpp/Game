import pygame
from pygame.locals import *

import Scene
import Box2D
from Box2D.b2 import *
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
        super(screen)
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

        for event in self.eventQueue:
            self.back(event)
            self.mouseEvents(event)

        self.world.Step(self.TIME_STEP, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)
        self.world.ClearForces()
        pygame.display.flip()
        self.clock.tick(self.TARGET_FPS)

    def computeAndDraw(self, body, fixture):
        colors = {
            staticBody  : (255,255,255,255),
            dynamicBody : (127,127,127,255),
        }

        vertices=[(body.transform * v) * self.PPM for v in fixture.shape.vertices]
        vertices=[(v[0], self.SCREEN_HEIGHT - v[1]) for v in vertices]
        pygame.draw.polygon(self.screen, colors[body.type], vertices)

    def mouseEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.dynamic_body.ApplyLinearImpulse(vec2(0, 30), vec2(0, 0), True)
            if event.key == pygame.K_s:
                self.dynamic_body.ApplyForce(vec2(0, -30), vec2(0, 0), True)
            if event.key == pygame.K_a:
                pass
            if event.key == pygame.K_d:
                self.dynamic_body.ApplyForce(vec2(3000, 10), self.dynamic_body.GetWorldPoint((0.0, 0.0)), True)

    def back(self, event):
        for event in self.eventQueue:
            if event.type==KEYDOWN and event.key==K_ESCAPE:
                self.isActive = False           

    def clearMemory(self):
        for body in self.world.bodies:
            self.world.DestroyBody(body)
        for joint in self.world.joints:
            self.world.DestroyJoint(joint)

    def dispose(self):
        self.clearMemory()

    def onExit(self):
        self.clearMemory()
        super(DefenseScene, self).onExit()