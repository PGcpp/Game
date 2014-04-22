import pygame
from pygame.locals import *
from Button import *
import VikingFactory
from VikingFactory import *
import Bullet
from Defender import *
import CollisionListener
from CollisionListener import *

import math
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

    world = None
    ground = None
    groundTexture = None
    count = 0

    tower = []

    clock = None

    defenders = [] #lista obroncow
    defenderSprite = None

    def DefenseScene(screen):
        self.screen = screen

    def prepare(self):
        self.world = world(gravity=(0,-10), doSleep=True, contactListener=CollisionListener())
        
        self.ground = self.world.CreateStaticBody(position=(0,-2), shapes=polygonShape(box=(64,4)))
        self.groundTexture = pygame.image.load("resources/ground.png")
	self.groundTexture = self.groundTexture.convert()
        self.ground.userData = ["ground"]

        self.defenderSprite = pygame.image.load("resources/defender_none.png").convert_alpha()

        self.tower.append( pygame.image.load("resources/brick1.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/brick2.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/brick3.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/brick4.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/stone1.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/stone2.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/stone3.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/stone4.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/steel1.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/steel2.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/steel3.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/steel4.png").convert_alpha() )
        
        self.box = self.world.CreateDynamicBody(position=(20, 5), angle=0)
        self.box.CreatePolygonFixture(box=(1,1), density=1, friction=0.3)
        self.box.userData = ["arrow"]

        self.clock = pygame.time.Clock()

        self.defenders.append( Defender(self.world, 60, 10, 100) ) #bedziemy strzelac raz na 100 klatek
        self.defenders[0].addBullet( 1, 1, 1, 10, "resources/bullet1.png" )

        self.defenders.append( Defender(self.world, 60, 14, 50) )
        self.defenders[1].addBullet( 1, 1, 15, 10, "resources/bullet1.png" )

        self.defenders.append( Defender(self.world, 60, 18, 200) )
        self.defenders[2].addBullet( 1, 1, 30, 10, "resources/bullet1.png" )

    def step(self):
        print "FPS: " + str( self.clock.get_fps() )
        self.screen.fill((0,0,0,0))
        for body in self.world.bodies:
            self.destroyViking(body)
            for fixture in body.fixtures:
                self.computeAndDraw(body, fixture)

        self.world.Step(self.TIME_STEP, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)
        self.world.ClearForces()
        pygame.display.flip()
        self.clock.tick(self.TARGET_FPS)

        self.checkAndDestroyBullet()

        self.count += 1
        
        for d in self.defenders:
            if self.count % d.interval == 0: #przegladamy defenderow, jesli ktorys moze strzelac to strzelamy :)
                d.shoot(35) #ta wartosc ofc powinna byc wyliczona algorytmem wykrywania wikingow, na razie na pale

        if self.count > self.TARGET_FPS * 5:
            self.count = 0
            self.createViking()

        for event in self.eventQueue:
            if event.type==KEYDOWN and event.key==K_ESCAPE:
                self.inGameMenuLoop()

    def createViking(self):
        VikingFactory(self.world, -2, 5)

    def destroyViking(self, body):
        if body.position[0] > 64:
            self.world.DestroyBody(body)

    def checkAndDestroyBullet(self):
        if self.world.contactListener.count > 0:
            for body in self.world.contactListener.bodiesToDestroy:
                if body != None:
                    self.world.DestroyBody(body)
            self.world.contactListener.bodiesToDestroy = [None, None, None, None, None, None, None, None, None, None]
            self.world.contactListener.count = 0

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
            self.screen.blit(body.userData[1], (vertices[0][0], vertices[2][1]))
        if body.userData != None and (body.userData[0] == "bullet" or body.userData[0] == "bulletShooted"):   
            self.screen.blit( pygame.transform.rotate(body.userData[1], (body.angle * 57.3) ), (vertices[0][0], vertices[2][1]))
        else:
            pygame.draw.polygon(self.screen, colors[body.type], vertices)

        #rysowanie tekstury wiezy
        self.screen.blit( self.tower[4], (999, 476) )
        self.screen.blit( self.tower[5], (1012, 396) )
        self.screen.blit( self.tower[2], (1023, 312) )
        self.screen.blit( self.tower[3], (1030, 228) )
        self.screen.blit( pygame.image.load("resources/top.png").convert_alpha(), (1035, 180) )

        #rysowanie defenderow
        self.screen.blit( self.defenderSprite, ( 1069, 486 ) )
        self.screen.blit( self.defenderSprite, ( 1069, 406 ) )
        self.screen.blit( self.defenderSprite, ( 1069, 322 ) )
        self.screen.blit( self.defenderSprite, ( 1069, 238 ) )

        #rysowanie tekstury ground
        self.screen.blit( self.groundTexture, (0, 559) )

    def dispose(self):
        for body in self.world.bodies:
            self.world.DestroyBody(body)
        for joint in self.world.joints:
            self.world.DestroyJoint(joint)

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

