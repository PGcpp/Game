import pygame
from pygame.locals import *
from Button import *
import VikingFactory
from VikingFactory import *
import CollisionListener
from CollisionListener import *

import Scene
import Box2D
from Box2D.b2 import *
from Enum import *
from sys import exit

class DefenseScene(Scene.Scene):
    
    PPM=20.0
    TARGET_FPS=45
    TIME_STEP=1.0/TARGET_FPS
    VELOCITY_ITERATIONS=10
    POSITION_ITERATIONS=10
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT=600

    world = None
    ground = None
    count = 0

    clock = None

    def DefenseScene(screen):
        self.screen = screen

    def prepare(self):
        self.world = world(gravity=(0,-10), doSleep=True, contactListener=CollisionListener())
        self.ground = self.world.CreateStaticBody(position=(0,1), shapes=polygonShape(box=(50,5)))

        self.box = self.world.CreateDynamicBody(position=(20, 5), angle=0)
        self.box.CreatePolygonFixture(box=(1,1), density=1, friction=0.3)
        self.box.userData = ["arrow"]

        self.clock = pygame.time.Clock()

    def step(self):
        self.screen.fill((0,0,0,0))
        for body in self.world.bodies:
            self.clearViking(body)
            for fixture in body.fixtures:
                self.computeAndDraw(body, fixture)

        self.world.Step(self.TIME_STEP, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)
        self.world.ClearForces()
        pygame.display.flip()
        self.clock.tick(self.TARGET_FPS)

        self.count += 1
        if self.count > self.TARGET_FPS * 5:
            self.count = 0
            self.deployVikings()

        for event in self.eventQueue:
            if event.type==KEYDOWN and event.key==K_ESCAPE:
                self.inGameMenuLoop()

    def deployVikings(self):
        VikingFactory(self.world, -2, 5)

    def clearViking(self, body):
        if body.position[0] > 45:
            self.world.DestroyBody(body)

    def mouseEvents(self, event):
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.viking.body.ApplyForce(vec2(0, 300), self.viking.body.GetWorldPoint((0, 0)), True)
                if event.key == pygame.K_s:
                    self.viking.body.ApplyForce(vec2(0, -300), self.viking.body.GetWorldPoint((0, 0)), True)
                if event.key == pygame.K_a:
                    self.viking.body.linearVelocity = vec2(-5, 0)
                if event.key == pygame.K_d:
                    self.viking.body.linearVelocity = vec2(5, 0)

    def computeAndDraw(self, body, fixture):
        colors = {
            staticBody  : (255,255,255,255),
            dynamicBody : (127,127,127,255),
        }

        vertices=[(body.transform * v) * self.PPM for v in fixture.shape.vertices]
        vertices=[(v[0], self.SCREEN_HEIGHT - v[1]) for v in vertices]
        if body.userData != None and body.userData[0] == "viking":
            self.displayImage(body.userData[1], vertices[0][0], vertices[2][1])
        else:
            pygame.draw.polygon(self.screen, colors[body.type], vertices)

    def dispose(self):
        for body in self.world.bodies:
            self.world.DestroyBody(body)
        for joint in self.world.joints:
            self.world.DestroyJoint(joint)

    def displayImage(self, image, xPos, yPos):
        self.screen.blit(image, (xPos, yPos))
        pygame.display.flip()

    def inGameMenuLoop(self):
        inGameMenuActive = True

        inGameMenuBackground = pygame.image.load("resources/inGameMenuBackground.png")
        self.screen.blit(inGameMenuBackground, (225, 100))
        pygame.display.flip()

        buttons = [None, None]
        buttons[0] = Button(315, 235, "RESUMEGAME")
        buttons[1] = Button(315, 310, "QUITGAME")

        for button in buttons:
            button.displayImage(self.screen)
        
        while inGameMenuActive:
            eventQueue = pygame.event.get()
            for event in eventQueue:
                
                if event.type == pygame.QUIT:
                    inGameMenuActive = False
                    self.onExit()
                    self.state = STATE.EXIT
                    self.stop()
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    for button in buttons:
                        x, y = event.pos
                        if button.isHit(x, y):

                            print button.name
                
                            if button.name == "RESUMEGAME":
                                inGameMenuActive = False
                            
                            if button.name == "QUITGAME":
                                inGameMenuActive = False
                                self.state = STATE.STOPPED
                                self.stop()

