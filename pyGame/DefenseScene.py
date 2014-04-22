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

    showFloorMenu = False
    activeFloorMenu = None

    backgroundTexture = None

    tower = []

    buttons = [None, None, None, None, None]

    clock = None

    defenders = [None, None, None, None] #lista obroncow
    defenderSprite = None

    def DefenseScene(screen):
        self.screen = screen

    def prepare(self):
        print "LECI!"
        self.world = world(gravity=(0,-10), doSleep=True, contactListener=CollisionListener())
        
        self.ground = self.world.CreateStaticBody(position=(0,-2), shapes=polygonShape(box=(64,4)))
        self.groundTexture = pygame.image.load("resources/ground.png")
	self.groundTexture = self.groundTexture.convert()
        self.ground.userData = ["ground"]

        self.backgroundTexture = pygame.image.load("resources/gameBackground.png").convert()

        self.defenderSprite = pygame.image.load("resources/defender_none.png").convert_alpha()

        self.tower.append( pygame.image.load("resources/brick1.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/brick2.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/brick3.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/brick4.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/stone1.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/stone2.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/stone3.png").convert_alpha() )
        self.tower.append( pygame.image.load("resources/stone4.png").convert_alpha() )
        
        self.clock = pygame.time.Clock()

        self.defenders[0] = Defender(self.world, 55,  4, -1)
        self.defenders[1] = Defender(self.world, 55,  8, -1)
        self.defenders[2] = Defender(self.world, 55, 12, -1) 
        self.defenders[3] = Defender(self.world, 55, 16, -1) 

    def step(self):
        #print "FPS: " + str( self.clock.get_fps() )
        self.screen.blit( self.backgroundTexture, (0,0) )
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
            if d.interval > 0:
                if self.count % d.interval == 0: #przegladamy defenderow, jesli ktorys moze strzelac to strzelamy :)
                    d.shoot(35) #ta wartosc ofc powinna byc wyliczona algorytmem wykrywania wikingow, na razie na pale

        if self.count > self.TARGET_FPS * 5:
            self.count = 0
            self.createViking()

        for event in self.eventQueue:
            if event.type==KEYDOWN and event.key==K_ESCAPE:
                self.inGameMenuLoop()

            if event.type == pygame.MOUSEBUTTONUP:
                        for button in self.buttons:
                            if button != None:
                                x, y = event.pos
                                if button.isHit(x, y):

                                    print button.name
                        
                                    if button.name == "FLOOR1":
                                        self.showFloorMenu = True
                                        self.activeFloorMenu = 1

                                    if button.name == "FLOOR2":
                                        self.showFloorMenu = True
                                        self.activeFloorMenu = 2

                                    if button.name == "FLOOR3":
                                        self.showFloorMenu = True
                                        self.activeFloorMenu = 3

                                    if button.name == "FLOOR4":
                                        self.showFloorMenu = True
                                        self.activeFloorMenu = 4
                                    if button.name == "CLOSEFLOORMENU":
                                        self.showFloorMenu = False

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
        self.screen.blit( self.tower[5], (1012, 392) )
        self.screen.blit( self.tower[6], (1023, 308) )
        self.screen.blit( self.tower[7], (1016, 140 ) )

        #rysowanie defenderow
        self.screen.blit( self.defenderSprite, ( 1069, 486 ) )
        self.screen.blit( self.defenderSprite, ( 1069, 406 ) )
        self.screen.blit( self.defenderSprite, ( 1069, 322 ) )
        self.screen.blit( self.defenderSprite, ( 1069, 238 ) )

        #rysowanie tekstury ground
        self.screen.blit( self.groundTexture, (0, 559) )

        #rysowanie stanu kasy
        moneyFont = pygame.font.SysFont("monospace", 25, True)
        moneyLabel = moneyFont.render("Money:", 1, (255,255,0))
        self.screen.blit(moneyLabel, (15, 10))

        amountLabel = moneyFont.render(str(self.count), 1, (255,255,0))
        self.screen.blit(amountLabel, (110, 10))

        #rysowanie przyciskow
        self.buttons[0] = Button(1049, 486, "FLOOR1")
        self.buttons[1] = Button(1049, 406, "FLOOR2")
        self.buttons[2] = Button(1049, 322, "FLOOR3")
        self.buttons[3] = Button(1049, 238, "FLOOR4")

        for button in self.buttons:
            if button != None:
                button.displayImage(self.screen, False)

        #rysowanie floorMenu
        if self.showFloorMenu:
            self.doShowFloorMenu()

    def dispose(self):
        for body in self.world.bodies:
            self.world.DestroyBody(body)
        for joint in self.world.joints:
            self.world.DestroyJoint(joint)
        defenders = [None, None, None, None]
        self.tower = []
            
    def inGameMenuLoop(self):
        inGameMenuActive = True

        inGameMenuBackground = pygame.image.load("resources/inGameMenuBackground.png")
        self.screen.blit(inGameMenuBackground, (440, 100))
        pygame.display.flip()

        buttons = [None, None]
        buttons[0] = Button(530, 235, "RESUMEGAME")
        buttons[1] = Button(530, 310, "QUITGAME")

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

    def doShowFloorMenu(self):
        #tu powinny byc wszystkie przyciski do dodawania do defenderow roznych rzeczy
        floorMenuBackground = pygame.image.load("resources/floorMenu.png").convert_alpha()
        self.screen.blit(floorMenuBackground, (940, 590))

        self.buttons[4] = Button(1200, 590, "CLOSEFLOORMENU")
