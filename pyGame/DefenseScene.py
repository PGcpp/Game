import pygame
from pygame.locals import *
from Button import *
from Viking import *
import Bullet
from Defender import *
import CollisionListener
from CollisionListener import *
from TowerFloor import *
from random import uniform

import math
import Scene
import Box2D
from Box2D.b2 import *
from Enum import *
from sys import exit

class DefenseScene(Scene.Scene):
    
    PPM=20.0
    TARGET_FPS=60.0
    TIME_STEP=1.0/TARGET_FPS
    VELOCITY_ITERATIONS=10
    POSITION_ITERATIONS=10
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT=600
    INTERVAL1 = 10
    INTERVAL2 = 15
    INTERVAL3 = 20

    world = None
    ground = None
    groundTexture = None
    count = 0

    showFloorMenu = False
    refreshFloorMenu = True #czy nalezy odswiezyc FloorMenu (oraz grounda!)
    activeFloorMenu = None

    floorMenuStoreTexture = None
    
    showFloorMenuStore = False
    refreshFloorMenuStore = True #czy nalezy odswiezyc FloorMenuStore (oraz grounda!)

    backgroundTexture = None

    towerFloors = [None, None, None, None]

    buttons = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

    clock = None

    money = None

    vikingId = 0
    vikings = {}
    vikingCount = 0
    vikingWave = 0

    def DefenseScene(screen):
        self.screen = screen

    def prepare(self):
        self.world = world(gravity=(0,-10), doSleep=True, contactListener=CollisionListener())
        
        self.ground = self.world.CreateStaticBody(position=(0,-2), shapes=polygonShape(box=(64,4)))
        self.groundTexture = pygame.image.load("resources/ground.png")
        self.groundTexture = self.groundTexture.convert()
        self.ground.userData = ["ground"]

        self.backgroundTexture = pygame.image.load("resources/gameBackground1.png").convert()

        self.floorMenuTexture = pygame.image.load("resources/floorMenu.png").convert_alpha()

        self.floorMenuStoreTexture = pygame.image.load("resources/floorMenuStore.png").convert_alpha()

        self.towerFloors[0] = TowerFloor( self.world, 1,  999/self.PPM, 476/self.PPM ,["resources/brick1.png", "resources/stone1.png"], 100 )
        self.towerFloors[1] = TowerFloor( self.world, 2, 1012/self.PPM, 392/self.PPM ,["resources/brick2.png", "resources/stone2.png"], 100 )
        self.towerFloors[2] = TowerFloor( self.world, 3, 1023/self.PPM, 308/self.PPM ,["resources/brick3.png", "resources/stone3.png"], 50 )
        self.towerFloors[3] = TowerFloor( self.world, 4, 1016/self.PPM, 140/self.PPM ,["resources/brick4.png", "resources/stone4.png"], 100 )
                
        self.towerFloors[0].setDefender("CATAPULT")
        self.towerFloors[1].setDefender("NONE")
        self.towerFloors[2].setDefender("ARCHER")
        self.towerFloors[3].setDefender("SLINGER")

        self.clock = pygame.time.Clock()

        self.money = 10000

        self.initialDraw()

    def step(self):
        #print "FPS: " + str( self.clock.get_fps() )
        
        self.screen.blit( self.backgroundTexture, (0,0) )

        #rysowanie tekstury wiezy
        for tF in self.towerFloors:
            self.screen.blit( tF.image[tF.level], (tF.xPos * 20, tF.yPos * 20) )
        #rysowanie defenderow
        self.screen.blit( self.towerFloors[0].defender.image, ( 1069, 486 ) )
        self.screen.blit( self.towerFloors[1].defender.image, ( 1069, 406 ) )
        self.screen.blit( self.towerFloors[2].defender.image, ( 1069, 322 ) )
        self.screen.blit( self.towerFloors[3].defender.image, ( 1069, 238 ) )

        for body in self.world.bodies:
            self.manageBody(body)
            for fixture in body.fixtures:
                self.computeAndDraw(body, fixture)

        self.world.Step(self.TIME_STEP, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)
        self.world.ClearForces()
        pygame.display.flip()
        self.clock.tick(self.TARGET_FPS)
        self.count += 1
        self.deployVikings()
        
        for t in self.towerFloors:
            if t.defender.interval > 0:
                if self.count % t.defender.interval == 0: #przegladamy defenderow, jesli ktorys moze strzelac to strzelamy :)
                    t.defender.shoot(35) #ta wartosc ofc powinna byc wyliczona algorytmem wykrywania wikingow, na razie na pale

        for event in self.eventQueue:
            if event.type==KEYDOWN and event.key==K_ESCAPE:
                self.inGameMenuLoop()
            self.handleFloorMenu(event)

    def deployVikings(self):
        if self.count % ((self.TARGET_FPS - self.vikingWave * 10) * self.INTERVAL1) == 0:
            for i in range(5 + self.vikingWave):
                self.vikings[self.vikingId] = Viking(self.world, VIKING.TYPE_1, self.vikingId, uniform(-20, 0), 5)
                self.vikingId += 1
                self.vikingCount += 1
            if self.vikingCount % 10 == 0:
                self.vikingWave += 1
        if self.vikingWave >= 2:
            if self.count % ((self.TARGET_FPS - self.vikingWave * 10) * self.INTERVAL2) == 0:
                for i in range(1 + self.vikingWave):
                    self.vikings[self.vikingId] = Viking(self.world, VIKING.TYPE_2, self.vikingId, uniform(-10, 0), 5)
                    self.vikingId += 1
        if self.vikingWave >= 4:
            if self.count % ((self.TARGET_FPS - self.vikingWave * 10) * self.INTERVAL3) == 0:
                for i in range(1 + self.vikingWave):
                    self.vikings[self.vikingId] = Viking(self.world, VIKING.TYPE_3, self.vikingId, uniform(-10, 0), 5)
                    self.vikingId += 1
            
    def manageBody(self, body):
        if body.userData != None and body.userData[0] == BULLET.HIT:
            self.world.DestroyBody(body)
        elif body.userData != None and body.userData[0] == VIKING.HIT:
            viking = self.vikings[body.userData[2]]
            if (viking.health - viking.body.userData[3]) <= 0:
                self.killViking(viking)
            else:
                viking.body.userData[0] = VIKING.NOT_HIT
                viking.health = viking.health - viking.body.userData[3]
                viking.body.userData[3] = None

        elif body.userData != None and body.userData[0] == VIKING.NOT_HIT:
            if body.position[0] > 50:
                viking = self.vikings[body.userData[2]]
                viking.body.linearVelocity = vec2(0, 0)
                viking.body.userData[0] = VIKING.ATTACK
                
        elif body.userData != None and body.userData[0] == BULLET.NOT_HIT:
            if body.position[1] < 3.0:
                self.world.DestroyBody(body)

        elif body.userData != None and body.userData[0] == VIKING.ATTACK:
            viking = self.vikings[body.userData[2]]
            viking.attackInterval -= 1
            if viking.attackInterval == 0:
                print "Viking " + str(viking.vikingId) + " deal " + str(viking.damage) + " dmg to tower"
                viking.attackInterval = 60

    def killViking(self, viking):
        self.world.DestroyBody(viking.body)
        if viking.name == VIKING.TYPE_1:
            self.money += viking.money
            self.showMoney()
        elif viking.name == VIKING.TYPE_2:
            self.money += viking.money
            self.showMoney()
        else:
            self.money += viking.money
            self.showMoney() 
        del self.vikings[viking.vikingId]
        viking = None


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
        
        if body.userData != None and (body.userData[0] == VIKING.NOT_HIT or body.userData[0] == VIKING.ATTACK):
            self.screen.blit(body.userData[1], (vertices[0][0], vertices[2][1]))
        if body.userData != None and body.userData[0] == BULLET.NOT_HIT:    
            self.screen.blit( pygame.transform.rotate(body.userData[1], (body.angle * 57.3) ), (vertices[0][0], vertices[2][1]))
        #else:
        #    pygame.draw.polygon(self.screen, colors[body.type], vertices)

        #rysowanie floorMenu
        if self.showFloorMenu:
            self.doShowFloorMenu()
        else:
            self.buttons[5] = None
            self.buttons[6] = None
            self.buttons[7] = None
            self.buttons[8] = None
            self.buttons[9] = None
            self.buttons[10] = None
            self.buttons[11] = None

        #rysowanie floorMenuStore
        if self.showFloorMenuStore:
            self.doShowFloorMenuStore()
        else:
            self.buttons[12] = None
            self.buttons[13] = None
            self.buttons[14] = None
            self.buttons[15] = None
            self.buttons[16] = None
            self.buttons[17] = None
            self.buttons[18] = None

        for button in self.buttons:
            if button != None:
                button.displayImage(self.screen, False)

    def initialDraw(self):

        backgroundTexture2 = pygame.image.load("resources/gameBackground2.png").convert()
        self.screen.blit(backgroundTexture2, ( 1034, 0 ) )

        #rysowanie tekstury ground
        self.screen.blit( self.groundTexture, (0, 559) )

        #rysowanie przyciskow
        self.buttons[0] = Button(1049, 486, "FLOOR1")
        self.buttons[1] = Button(1049, 406, "FLOOR2")
        self.buttons[2] = Button(1049, 322, "FLOOR3")
        self.buttons[3] = Button(1049, 238, "FLOOR4")
        self.buttons[4] = Button(1230, 20, "SHOWMENU")

        self.showMoney()

    def showMoney(self):
        self.screen.blit( self.groundTexture, (0, 559) )
        moneyFont = pygame.font.SysFont("monospace", 25, True)
        moneyLabel = moneyFont.render("Money:", 1, (255,255,0))
        self.screen.blit(moneyLabel, (15, 600))

        amountLabel = moneyFont.render(str(self.money), 1, (255,255,0))
        self.screen.blit(amountLabel, (110, 600))

    def dispose(self):
        for body in self.world.bodies:
            self.world.DestroyBody(body)
        for joint in self.world.joints:
            self.world.DestroyJoint(joint)
            
        for b in self.buttons:
            b = None
            
        for t in self.towerFloors:
            t = None
            
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

    def handleFloorMenu(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
                    for button in self.buttons:
                        if button != None:
                            x, y = event.pos
                            if button.isHit(x, y):

                                print button.name

                                if button.name == "SHOWMENU":
                                    self.inGameMenuLoop()
                    
                                if button.name == "FLOOR1":
                                    self.showFloorMenu = True
                                    self.refreshFloorMenu = True
                                    self.activeFloorMenu = 0

                                if button.name == "FLOOR2":
                                    self.showFloorMenu = True
                                    self.refreshFloorMenu = True
                                    self.activeFloorMenu = 1

                                if button.name == "FLOOR3":
                                    self.showFloorMenu = True
                                    self.refreshFloorMenu = True
                                    self.activeFloorMenu = 2

                                if button.name == "FLOOR4":
                                    self.showFloorMenu = True
                                    self.refreshFloorMenu = True
                                    self.activeFloorMenu = 3
                                    
                                if button.name == "CLOSEFLOORMENU":
                                    self.showFloorMenu = False
                                    self.refreshFloorMenu = True
                                    self.showMoney()
                                    
                                if button.name == "UPGRADEFLOORLEVEL":
                                    if self.money >= 7000 and self.towerFloors[self.activeFloorMenu].level < 1:
                                        self.towerFloors[self.activeFloorMenu].level += 1
                                        self.towerFloors[self.activeFloorMenu].hp = 100 * (self.towerFloors[self.activeFloorMenu].level + 1)
                                        self.money -= 7000

                                        self.refreshFloorMenu = True
                                        
                                if button.name == "FIXTOWERFLOOR":
                                    cost = (100 - self.towerFloors[self.activeFloorMenu].hp) * 5

                                    if self.money >= cost and self.towerFloors[self.activeFloorMenu].hp < (100 * (self.towerFloors[self.activeFloorMenu].level + 1) ):
                                        self.towerFloors[self.activeFloorMenu].hp = (100 * (self.towerFloors[self.activeFloorMenu].level + 1) )
                                        self.money -= cost

                                        self.refreshFloorMenu = True

                                if button.name == "BUYDEFENDER":
                                    self.showFloorMenu = False
                                    self.refreshFloorMenu = True
                                    self.showFloorMenuStore = True
                                    self.refreshFloorMenuStore = True

                                if button.name == "SELLDEFENDER":
                                    self.money += COSTS.DEFENDER[self.towerFloors[self.activeFloorMenu].defender.name]
                                    self.towerFloors[self.activeFloorMenu].setDefender("NONE")
                                    self.refreshFloorMenu = True

                                if button.name == "CLOSEFLOORMENUSTORE":
                                    self.showFloorMenu = True
                                    self.refreshFloorMenu = True
                                    self.showFloorMenuStore = False
                                    self.refreshFloorMenuStore = True

    def doShowFloorMenu(self):

        if self.refreshFloorMenu:

            self.refreshFloorMenu = False

            self.showMoney() #to nam od razu czysci stare menu
            
            #tlo menu
            self.screen.blit(self.floorMenuTexture, (940, 590))

            #przycisk do wylaczania menu
            self.buttons[5] = Button(1200, 590, "CLOSEFLOORMENU")

            #wypisywanie zawartosci menu - tekst
            floorMenuFont = pygame.font.SysFont("monospace", 12, True)
            LevelLabel = floorMenuFont.render("LVL:", 1, (0,0,0))
            LevelValue = floorMenuFont.render(str( self.towerFloors[self.activeFloorMenu].level ), 1, (0,0,0))
            HPLabel = floorMenuFont.render("HP:", 1, (0,0,0))
            HPValue = floorMenuFont.render(str( self.towerFloors[self.activeFloorMenu].hp ), 1, (0,0,0))
            UpgradeLevelValue = floorMenuFont.render("7000$", 1, (100,100,0))
            FixTowerFloorValue = floorMenuFont.render(str( ((100 * (self.towerFloors[self.activeFloorMenu].level + 1) ) - self.towerFloors[self.activeFloorMenu].hp) * 5 ) + "$", 1, (0,100,0))

            dName = str( self.towerFloors[self.activeFloorMenu].defender.name )
            if len(dName) <= 4:
                dName = '  '+dName
            elif len(dName) <= 6:
                dName = ' '+dName
                
            DefenderNameLabel = floorMenuFont.render( dName, 1, (0,0,0))
            AttackLabel = floorMenuFont.render("ATTACK:", 1, (0,0,0))
            ReloadLabel = floorMenuFont.render("RELOAD:", 1, (0,0,0))
            SpeedLabel = floorMenuFont.render(" SPEED:", 1, (0,0,0))

            self.screen.blit(LevelLabel, (950, 630))
            self.screen.blit(LevelValue, (980, 630))
            self.screen.blit(UpgradeLevelValue, (980, 645))
            self.screen.blit(HPLabel, (950, 668))
            self.screen.blit(HPValue, (970, 668))
            self.screen.blit(FixTowerFloorValue, (980, 685))

            self.screen.blit(DefenderNameLabel, (1035, 625))
            self.screen.blit(AttackLabel, (1105, 650))
            self.screen.blit(ReloadLabel, (1105, 670))
            self.screen.blit(SpeedLabel,  (1105, 690))

            #unit
            self.screen.blit(self.towerFloors[self.activeFloorMenu].defender.icon, (1045, 640) )

            #wypisywanie zawartosci menu - przyciski/grafiki

            self.buttons[6] = Button(995, 628, "UPGRADEFLOORLEVEL")
            #upgradeTowerFloorButton.displayImage(self.screen, False)

            self.buttons[7] = Button(950, 685, "FIXTOWERFLOOR")
            #fixButton.displayImage(self.screen, False)

            self.buttons[8] = Button(1180, 647, "UPGRADEFLOORLEVEL")
            self.buttons[9] = Button(1180, 667, "UPGRADEFLOORLEVEL")
            self.buttons[10] = Button(1180, 687, "UPGRADEFLOORLEVEL")

            if self.towerFloors[self.activeFloorMenu].defender.name == "NONE":
                self.buttons[11] = Button(1049, 690 ,"BUYDEFENDER")
            else:
                DefenderCostLabel = floorMenuFont.render( str( COSTS.DEFENDER[ self.towerFloors[self.activeFloorMenu].defender.name ] ), 1, (100,100,0))
                self.screen.blit(DefenderCostLabel,  (1062, 690))
                self.buttons[11] = Button(1028, 690 ,"SELLDEFENDER")

    def doShowFloorMenuStore(self):

        if self.refreshFloorMenuStore:
            
            self.refreshFloorMenuStore = False

            self.showMoney() #to nam od razu czysci stare menu
            
            #tlo menu
            self.screen.blit(self.floorMenuStoreTexture, (855, 590))

            #przycisk do wylaczania sklepu
            self.buttons[12] = Button(1200, 590, "CLOSEFLOORMENUSTORE")

            #ikony defenderow
            self.screen.blit(pygame.image.load("resources/defenderIco_spearman.png").convert_alpha(), (870, 600) )
            self.screen.blit(pygame.image.load("resources/defenderIco_slinger.png").convert_alpha(),  (930, 600) )
            self.screen.blit(pygame.image.load("resources/defenderIco_archer.png").convert_alpha(),   (990, 600) )
            self.screen.blit(pygame.image.load("resources/defenderIco_catapult.png").convert_alpha(), (1050, 600) )
            self.screen.blit(pygame.image.load("resources/defenderIco_cannon.png").convert_alpha(),   (1110, 600) )
            self.screen.blit(pygame.image.load("resources/defenderIco_wizard.png").convert_alpha(),   (1170, 600) )

            #podpisy defenderow
            floorMenuStoorFont = pygame.font.SysFont("monospace", 10, True)
            storeSpearmanLabel = floorMenuStoorFont.render("SPEARMAN", 1, (0,0,0))
            storeSlingerLabel = floorMenuStoorFont.render("SLINGER", 1, (0,0,0))
            storeArcherLabel = floorMenuStoorFont.render("ARCHER", 1, (0,0,0))
            storeCatapultLabel = floorMenuStoorFont.render("CATAPULT", 1, (0,0,0))
            storeCannonLabel = floorMenuStoorFont.render("CANNON", 1, (0,0,0))
            storeWizardLabel = floorMenuStoorFont.render("WIZARD", 1, (0,0,0))

            self.screen.blit(storeSpearmanLabel, (863, 648))
            self.screen.blit(storeSlingerLabel, (928, 648))
            self.screen.blit(storeArcherLabel, (989, 648))
            self.screen.blit(storeCatapultLabel, (1043, 648))
            self.screen.blit(storeCannonLabel, (1110, 648))
            self.screen.blit(storeWizardLabel, (1169, 648))

            #przyciski buy
            self.buttons[13] = Button(874, 680, "BUYDEFENDER")
            self.buttons[14] = Button(934, 680, "BUYDEFENDER")
            self.buttons[15] = Button(994, 680, "BUYDEFENDER")
            self.buttons[16] = Button(1054, 680, "BUYDEFENDER")
            self.buttons[17] = Button(1114, 680, "BUYDEFENDER")
            self.buttons[18] = Button(1174, 680, "BUYDEFENDER")

            #koszty defenderow
            storeSpearmanLabel = floorMenuStoorFont.render(str( COSTS.DEFENDER[ "SPEARMAN" ] ), 1, (0,50,0))
            storeSlingerLabel = floorMenuStoorFont.render(str( COSTS.DEFENDER[ "SLINGER" ] ), 1, (0,50,0))
            storeArcherLabel = floorMenuStoorFont.render(str( COSTS.DEFENDER[ "ARCHER" ] ), 1, (0,50,0))
            storeCatapultLabel = floorMenuStoorFont.render(str( COSTS.DEFENDER[ "CATAPULT" ] ), 1, (0,50,0))
            storeCannonLabel = floorMenuStoorFont.render(str( COSTS.DEFENDER[ "CANNON" ] ), 1, (0,50,0))
            storeWizardLabel = floorMenuStoorFont.render(str( COSTS.DEFENDER[ "WIZARD" ] ), 1, (0,50,0))

            self.screen.blit(storeSpearmanLabel, (879, 695))
            self.screen.blit(storeSlingerLabel, (938, 695))
            self.screen.blit(storeArcherLabel, (996, 695))
            self.screen.blit(storeCatapultLabel, (1055, 695))
            self.screen.blit(storeCannonLabel, (1116, 695))
            self.screen.blit(storeWizardLabel, (1176, 695))
        

