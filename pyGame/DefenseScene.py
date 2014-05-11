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
    INTERVAL1 = 12
    INTERVAL2 = 20
    INTERVAL3 = 25

    gameOver = False

    world = None
    ground = None
    groundTexture = None
    groundTextureLeft = None
    groundTextureRight = None
    count = 0

    hpTexture = None

    showFloorMenu = False
    refreshFloorMenu = True #czy nalezy odswiezyc FloorMenu (oraz grounda!)
    activeFloorMenu = None

    gameOverTexture = None

    floorMenuStoreTexture = None
    
    showFloorMenuStore = False
    refreshFloorMenuStore = True #czy nalezy odswiezyc FloorMenuStore (oraz grounda!)

    chosenFloorTexture = None

    backgroundTexture = None

    towerFloors = [None, None, None, None]
    targetFloor = 0

    buttons = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

    clock = None

    money = None

    vikingId = 0
    vikings = {}
    vikingWave = 0

    def DefenseScene(screen):
        self.screen = screen

    def prepare(self):
        self.world = world(gravity=(0,-10), doSleep=True, contactListener=CollisionListener())
        
        self.ground = self.world.CreateStaticBody(position=(0,-2), shapes=polygonShape(box=(64,4)))
        self.groundTexture = pygame.image.load("resources/ground.png")
        self.groundTexture = self.groundTexture.convert()
        self.groundTextureLeft = pygame.image.load("resources/ground_left.png")
        self.groundTextureLeft = self.groundTextureLeft.convert()
        self.groundTextureRight = pygame.image.load("resources/ground_right.png")
        self.groundTextureRight = self.groundTextureRight.convert()
        self.ground.userData = ["ground"]

        self.hpTexture = pygame.image.load("resources/hpBackground.png").convert_alpha()

        self.gameOverTexture = pygame.image.load("resources/gameOver.png").convert_alpha()
        
        self.backgroundTexture = pygame.image.load("resources/gameBackground.png").convert()

        self.floorMenuTexture = pygame.image.load("resources/floorMenu.png").convert_alpha()

        self.floorMenuStoreTexture = pygame.image.load("resources/floorMenuStore.png").convert_alpha()

        self.chosenFloorTexture = pygame.image.load('resources/chosenFloor.png').convert_alpha()

        self.drawTower()

        self.clock = pygame.time.Clock()

        self.money = 1500

        self.initialDraw()

    def step(self):      
        self.screen.blit( self.backgroundTexture, (0,0) )

        #rysowanie tekstury wiezy
        for tF in self.towerFloors[self.targetFloor:4]:
            self.screen.blit( tF.image[tF.level], (tF.xPos * 20, tF.yPos * 20) )

        #rysowanie defenderow
        self.drawDefenders()
        
        #rysowanie floorMenu
        if self.showFloorMenu:

            #rysowanie markera zaznaczonego defendera
            self.drawChosenFloorMenu()

            #rysowanie menu    
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
        
        for t in self.towerFloors[self.targetFloor:4]:
            if t.defender.interval > 0:
                if self.count % t.defender.interval == 0:

                    distanceToShoot = 0
                  
                    for v in self.vikings.keys():
                        
                        vikingX = self.vikings[v].body.position.x
                        
                        if distanceToShoot < vikingX:
                            distanceToShoot = vikingX

                    if distanceToShoot > 0:  
                        distanceToShoot = 55.0 - distanceToShoot 
                    t.defender.shoot( float(distanceToShoot) )

                    distanceToShoot = 0

        for event in self.eventQueue:
            if event.type==KEYDOWN and event.key==K_ESCAPE:
                self.inGameMenuLoop()
            self.handleFloorMenu(event)

        if self.gameOver:
            self.gameOverLoop()

    def deployVikings(self):
        if self.count % (self.TARGET_FPS * self.INTERVAL1) == 0:
            if self.vikingWave <= 8: 
                for i in range(2 + self.vikingWave):
                    self.vikings[self.vikingId] = Viking(self.world, VIKING.TYPE_1, self.vikingId, uniform(-20, 0), 5)
                    self.vikingId += 1
            else:
                for i in range(8):
                    self.vikings[self.vikingId] = Viking(self.world, VIKING.TYPE_1, self.vikingId, uniform(-20, 0), 5)
                    self.vikingId += 1
            self.vikingWave += 1
        if self.vikingWave >= 8:
            if self.count % (self.TARGET_FPS * self.INTERVAL2) == 0:
                if self.vikingWave <= 16:
                    for i in range(self.vikingWave - 8):
                        self.vikings[self.vikingId] = Viking(self.world, VIKING.TYPE_2, self.vikingId, uniform(-20, 0), 5)
                        self.vikingId += 1
                else:
                    for i in range(8):
                        self.vikings[self.vikingId] = Viking(self.world, VIKING.TYPE_2, self.vikingId, uniform(-20, 0), 5)
                        self.vikingId += 1                    
        if self.vikingWave >= 16:
            if self.count % (self.TARGET_FPS * self.INTERVAL3) == 0:
                if self.vikingWave <= 24:
                    for i in range(self.vikingWave - 16):
                        self.vikings[self.vikingId] = Viking(self.world, VIKING.TYPE_3, self.vikingId, uniform(-20, 0), 5)
                        self.vikingId += 1
                else:
                    for i in range(8):
                        self.vikings[self.vikingId] = Viking(self.world, VIKING.TYPE_3, self.vikingId, uniform(-20, 0), 5)
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
            if body.position[1] < 3.2:
                self.world.DestroyBody(body)

        elif body.userData != None and body.userData[0] == VIKING.ATTACK:
            viking = self.vikings[body.userData[2]]
            viking.attackInterval -= 1
            if viking.attackInterval == 0:
                self.attackTower(viking)
                viking.attackInterval = 60

    def attackTower(self, viking):
        floor = self.towerFloors[self.targetFloor]
        floor.hp = floor.hp - viking.damage

        #wypisywanie hp:
        if self.showFloorMenu and (not self.showFloorMenuStore):
            self.printTowerFloorHP()
        
        print "Viking " + str(viking.vikingId) + " deal " + str(viking.damage) + " dmg to floor " + str(self.targetFloor)
        print "Floor " + str(self.targetFloor) + " left " + str(floor.hp) + " hp"
        if floor.hp <= 0:

            if self.showFloorMenu or self.showFloorMenuStore:
                self.showFloorMenu = False
                self.refreshFloorMenu = True
                self.showFloorMenuStore = False
                self.refreshFloorMenuStore = True

                self.screen.blit( self.groundTextureRight, (768, 559) )
            
            print "Tower floor " + str(self.targetFloor) + " destroyed!"
            self.targetFloor += 1
            self.drawTower()
            self.drawButtoms()
            if self.targetFloor >= 4:
                self.targetFloor = 3
                self.gameOver = True

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

    def initialDraw(self):

        self.screen.blit(self.backgroundTexture, ( 1034, 0 ) )

        #rysowanie tekstury ground
        self.screen.blit( self.groundTexture, (0, 559) )

        #rysowanie przyciskow
        self.drawButtoms()

        self.showMoney()

    def showMoney(self):
        print "rysuje"
        self.screen.blit( self.groundTextureLeft, (0, 559) )
        moneyFont = pygame.font.SysFont("monospace", 25, True)
        moneyLabel = moneyFont.render("Money:", 1, (255,255,0))
        self.screen.blit(moneyLabel, (15, 600))

        amountLabel = moneyFont.render(str(self.money), 1, (255,255,0))
        self.screen.blit(amountLabel, (110, 600))

    def tryPay(self, amount):
        if self.money < amount:
            return False
        else:
            self.money -= amount
            self.showMoney()
            return True

    #funkcje liczace wartosci skillow
    def calculateDamageCost(self, defender):
        print " DD: "+str(int( ( defender.getDamage() - SKILLS.DAMAGE[ defender.name ] ) / SKILLS.STEP ))
        cost = COSTS.DEFENDERUPGRADE.DAMAGE + ( COSTS.DEFENDER[ defender.name ] / 4 )
        for i in range( int( ( defender.getDamage() - SKILLS.DAMAGE[ defender.name ] ) / SKILLS.STEP ) ):
            cost += COSTS.DEFENDERUPGRADE.STEP

        return int( cost )

    def calculateIntervalCost(self, defender):
        cost = COSTS.DEFENDERUPGRADE.RELOAD + ( COSTS.DEFENDER[ defender.name ] / 4 )
        for i in range( int( ( SKILLS.INTERVAL[ defender.name ] - defender.getInterval() ) / SKILLS.STEP ) ):     #tu odejmuje na odwrot bo ten parametr maleje a nie narasta
            cost += COSTS.DEFENDERUPGRADE.STEP

        return int( cost )

    def calculateSpeedCost(self, defender):
        cost = COSTS.DEFENDERUPGRADE.SPEED + ( COSTS.DEFENDER[ defender.name ] / 4 )
        for i in range( int( ( defender.getSpeed() - SKILLS.SPEED[ defender.name ] ) / SKILLS.STEP ) ):
            cost += COSTS.DEFENDERUPGRADE.STEP

        return int( cost )
        
            
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
                                    self.showFloorMenuStore = False
                                    self.refreshFloorMenuStore = True
                                    self.activeFloorMenu = 0

                                if button.name == "FLOOR2":
                                    self.showFloorMenu = True
                                    self.refreshFloorMenu = True
                                    self.showFloorMenuStore = False
                                    self.refreshFloorMenuStore = True
                                    self.activeFloorMenu = 1

                                if button.name == "FLOOR3":
                                    self.showFloorMenu = True
                                    self.refreshFloorMenu = True
                                    self.showFloorMenuStore = False
                                    self.refreshFloorMenuStore = True
                                    self.activeFloorMenu = 2

                                if button.name == "FLOOR4":
                                    self.showFloorMenu = True
                                    self.refreshFloorMenu = True
                                    self.showFloorMenuStore = False
                                    self.refreshFloorMenuStore = True
                                    self.activeFloorMenu = 3
                                    
                                if button.name == "CLOSEFLOORMENU":
                                    self.showFloorMenu = False
                                    self.refreshFloorMenu = True

                                    self.screen.blit( self.groundTextureRight, (768, 559) ) #to nam od razu czysci stare menu
                                    
                                if button.name == "UPGRADEFLOORLEVEL":
                                    if self.towerFloors[self.activeFloorMenu].level < SKILLS.FLOOR.MAXLEVEL:
                                        
                                        if self.tryPay( COSTS.FLOOR.UPGRADE ):
                                            self.towerFloors[self.activeFloorMenu].upgrade()
                                            
                                            self.refreshFloorMenu = True


                                if button.name == "UPGRADEDEFENDERDAMAGE":

                                    if self.towerFloors[self.activeFloorMenu].defender.name != "NONE":
                                                
                                        if self.tryPay( self.calculateDamageCost( self.towerFloors[self.activeFloorMenu].defender ) ):
                                            self.towerFloors[self.activeFloorMenu].defender.upgradeDamage()
                                            self.refreshFloorMenu = True

                                if button.name == "UPGRADEDEFENDERINTERVAL":

                                    if self.towerFloors[self.activeFloorMenu].defender.name != "NONE" and self.towerFloors[self.activeFloorMenu].defender.interval >= ( SKILLS.MINVALUE ):  #bardzo brzydki workaround ale w tym przypadku potrzebny - ten skill ma jasno wytyczona granice i nie chcemy zeby nie dalo sie juz upgradeowac a zeby kasa sie odliczala

                                        if self.tryPay( self.calculateIntervalCost( self.towerFloors[self.activeFloorMenu].defender ) ):
                                            self.towerFloors[self.activeFloorMenu].defender.upgradeInterval()
                                            self.refreshFloorMenu = True

                                if button.name == "UPGRADEDEFENDERSPEED":

                                    if self.towerFloors[self.activeFloorMenu].defender.name != "NONE":
                                    
                                        if self.tryPay( self.calculateSpeedCost( self.towerFloors[self.activeFloorMenu].defender ) ):
                                            self.towerFloors[self.activeFloorMenu].defender.upgradeSpeed()
                                            self.refreshFloorMenu = True


                                if button.name == "FIXTOWERFLOOR":
                                    cost = (100 - self.towerFloors[self.activeFloorMenu].hp) * 5

                                    if self.towerFloors[self.activeFloorMenu].hp < (100 * (self.towerFloors[self.activeFloorMenu].level + 1) ):

                                        if self.tryPay(cost):

                                            self.towerFloors[self.activeFloorMenu].hp = (100 * (self.towerFloors[self.activeFloorMenu].level + 1) )

                                            self.refreshFloorMenu = True

                                if button.name == "BUYDEFENDER":
                                    self.showFloorMenu = False
                                    self.refreshFloorMenu = True
                                    self.showFloorMenuStore = True
                                    self.refreshFloorMenuStore = True

                                if button.name == "SELLDEFENDER":
                                    defender = self.towerFloors[self.activeFloorMenu].defender

                                    self.money += COSTS.DEFENDER[ defender.name ]
                                    self.showMoney()
                                    
                                    self.towerFloors[self.activeFloorMenu].setDefender("NONE")
                                    self.refreshFloorMenu = True

                                if button.name == "BUYSPEARMAN":
                                    if self.tryPay( COSTS.DEFENDER[ "SPEARMAN" ] ):
                                        self.towerFloors[self.activeFloorMenu].setDefender("SPEARMAN")

                                        self.showFloorMenu = True
                                        self.refreshFloorMenu = True
                                        self.showFloorMenuStore = False
                                        self.refreshFloorMenuStore = True

                                if button.name == "BUYSLINGER":
                                    if self.tryPay( COSTS.DEFENDER[ "SLINGER" ] ):
                                        self.towerFloors[self.activeFloorMenu].setDefender("SLINGER")
                                        
                                        self.showFloorMenu = True
                                        self.refreshFloorMenu = True
                                        self.showFloorMenuStore = False
                                        self.refreshFloorMenuStore = True

                                if button.name == "BUYARCHER":
                                    if self.tryPay( COSTS.DEFENDER[ "ARCHER" ] ):
                                        self.towerFloors[self.activeFloorMenu].setDefender("ARCHER")
                                        
                                        self.showFloorMenu = True
                                        self.refreshFloorMenu = True
                                        self.showFloorMenuStore = False
                                        self.refreshFloorMenuStore = True

                                if button.name == "BUYCATAPULT":
                                    if self.tryPay( COSTS.DEFENDER[ "CATAPULT" ] ):
                                        self.towerFloors[self.activeFloorMenu].setDefender("CATAPULT")
                                        
                                        self.showFloorMenu = True
                                        self.refreshFloorMenu = True
                                        self.showFloorMenuStore = False
                                        self.refreshFloorMenuStore = True

                                if button.name == "BUYCANNON":
                                    if self.tryPay( COSTS.DEFENDER[ "CANNON" ] ):
                                        self.towerFloors[self.activeFloorMenu].setDefender("CANNON")
                                        
                                        self.showFloorMenu = True
                                        self.refreshFloorMenu = True
                                        self.showFloorMenuStore = False
                                        self.refreshFloorMenuStore = True

                                if button.name == "BUYWIZARD":
                                    if self.tryPay( COSTS.DEFENDER[ "WIZARD" ] ):
                                        self.towerFloors[self.activeFloorMenu].setDefender("WIZARD")
        
                                        self.showFloorMenu = True
                                        self.refreshFloorMenu = True
                                        self.showFloorMenuStore = False
                                        self.refreshFloorMenuStore = True

                                if button.name == "CLOSEFLOORMENUSTORE":
                                    self.showFloorMenu = True
                                    self.refreshFloorMenu = True
                                    self.showFloorMenuStore = False
                                    self.refreshFloorMenuStore = True

    def doShowFloorMenu(self):

        if self.refreshFloorMenu:
            print "PIK"
            self.screen.blit( self.groundTextureRight, (768, 559) )

            self.refreshFloorMenu = False

            defender = self.towerFloors[self.activeFloorMenu].defender
            
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
            UpgradeLevelValue = floorMenuFont.render(str( COSTS.FLOOR.UPGRADE ), 1, (100,100,0))
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

            AttackUpgradeValue = floorMenuFont.render(str( self.calculateDamageCost( defender ) ), 1, (100,100,0))
            ReloadUpgradeValue = floorMenuFont.render(str( self.calculateIntervalCost( defender ) ), 1, (100,100,0))
            SpeedUpgradeValue = floorMenuFont.render(str( self.calculateSpeedCost( defender ) ), 1, (100,100,0))

            AttackValue = floorMenuFont.render(str( int( defender.getDamage() ) ), 1, (0,0,0))
            ReloadValue = floorMenuFont.render(str( int( defender.getInterval() ) ), 1, (0,0,0))
            SpeedValue = floorMenuFont.render(str( int( defender.getSpeed() ) ), 1, (0,0,0))

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

            self.screen.blit(AttackValue, (1160, 650))
            self.screen.blit(ReloadValue, (1160, 670))
            self.screen.blit(SpeedValue,  (1160, 690))

            self.screen.blit(AttackUpgradeValue, (1210, 650))
            self.screen.blit(ReloadUpgradeValue, (1210, 670))
            self.screen.blit(SpeedUpgradeValue,  (1210, 690))

            #unit
            self.screen.blit(self.towerFloors[self.activeFloorMenu].defender.icon, (1045, 640) )

            #wypisywanie zawartosci menu - przyciski/grafiki
            self.buttons[6] = Button(995, 628, "UPGRADEFLOORLEVEL")

            self.buttons[7] = Button(950, 685, "FIXTOWERFLOOR")

            self.buttons[8] = Button(1190, 647, "UPGRADEDEFENDERDAMAGE")
            self.buttons[9] = Button(1190, 667, "UPGRADEDEFENDERINTERVAL")
            self.buttons[10] = Button(1190, 687, "UPGRADEDEFENDERSPEED")

            if self.towerFloors[self.activeFloorMenu].defender.name == "NONE":
                self.buttons[11] = Button(1049, 690 ,"BUYDEFENDER")
            else:
                DefenderCostLabel = floorMenuFont.render( str( COSTS.DEFENDER[ self.towerFloors[self.activeFloorMenu].defender.name ] ), 1, (100,100,0))
                self.screen.blit(DefenderCostLabel,  (1062, 690))
                self.buttons[11] = Button(1028, 690 ,"SELLDEFENDER")

    def doShowFloorMenuStore(self):

        if self.refreshFloorMenuStore:

            self.screen.blit( self.groundTextureRight, (768, 559) )
            
            self.refreshFloorMenuStore = False
            
            #tlo menu
            self.screen.blit(self.floorMenuStoreTexture, (855, 590))

            #przycisk do wylaczania sklepu
            self.buttons[12] = Button(1200, 590, "CLOSEFLOORMENUSTORE")

            #ikony defenderow
            self.screen.blit(pygame.image.load("resources/defenderIco_spearman.png").convert_alpha(), (870, 595) )
            self.screen.blit(pygame.image.load("resources/defenderIco_slinger.png").convert_alpha(),  (930, 595) )
            self.screen.blit(pygame.image.load("resources/defenderIco_archer.png").convert_alpha(),   (990, 595) )
            self.screen.blit(pygame.image.load("resources/defenderIco_catapult.png").convert_alpha(), (1050, 595) )
            self.screen.blit(pygame.image.load("resources/defenderIco_cannon.png").convert_alpha(),   (1110, 595) )
            self.screen.blit(pygame.image.load("resources/defenderIco_wizard.png").convert_alpha(),   (1170, 595) )

            #podpisy defenderow
            floorMenuStoorFont = pygame.font.SysFont("monospace", 10, True)
            storeSpearmanLabel = floorMenuStoorFont.render("SPEARMAN", 1, (0,0,0))
            storeSlingerLabel = floorMenuStoorFont.render("SLINGER", 1, (0,0,0))
            storeArcherLabel = floorMenuStoorFont.render("ARCHER", 1, (0,0,0))
            storeCatapultLabel = floorMenuStoorFont.render("CATAPULT", 1, (0,0,0))
            storeCannonLabel = floorMenuStoorFont.render("CANNON", 1, (0,0,0))
            storeWizardLabel = floorMenuStoorFont.render("WIZARD", 1, (0,0,0))

            self.screen.blit(storeSpearmanLabel, (863, 643))
            self.screen.blit(storeSlingerLabel, (928, 643))
            self.screen.blit(storeArcherLabel, (989, 643))
            self.screen.blit(storeCatapultLabel, (1043, 643))
            self.screen.blit(storeCannonLabel, (1110, 643))
            self.screen.blit(storeWizardLabel, (1169, 643))

            #przyciski buy
            self.buttons[13] = Button(874, 683, "BUYSPEARMAN")
            self.buttons[14] = Button(934, 683, "BUYSLINGER")
            self.buttons[15] = Button(994, 683, "BUYARCHER")
            self.buttons[16] = Button(1054, 683, "BUYCATAPULT")
            self.buttons[17] = Button(1114, 683, "BUYCANNON")
            self.buttons[18] = Button(1174, 683, "BUYWIZARD")

            #koszty defenderow
            storeSpearmanLabel = floorMenuStoorFont.render(str( COSTS.DEFENDER[ "SPEARMAN" ] ), 1, (0,50,0))
            storeSlingerLabel = floorMenuStoorFont.render(str( COSTS.DEFENDER[ "SLINGER" ] ), 1, (0,50,0))
            storeArcherLabel = floorMenuStoorFont.render(str( COSTS.DEFENDER[ "ARCHER" ] ), 1, (0,50,0))
            storeCatapultLabel = floorMenuStoorFont.render(str( COSTS.DEFENDER[ "CATAPULT" ] ), 1, (0,50,0))
            storeCannonLabel = floorMenuStoorFont.render(str( COSTS.DEFENDER[ "CANNON" ] ), 1, (0,50,0))
            storeWizardLabel = floorMenuStoorFont.render(str( COSTS.DEFENDER[ "WIZARD" ] ), 1, (0,50,0))

            self.screen.blit(storeSpearmanLabel, (879, 698))
            self.screen.blit(storeSlingerLabel, (938, 698))
            self.screen.blit(storeArcherLabel, (996, 698))
            self.screen.blit(storeCatapultLabel, (1055, 698))
            self.screen.blit(storeCannonLabel, (1116, 698))
            self.screen.blit(storeWizardLabel, (1176, 698))

            #statsy defenderow
            floorMenuStoorFontSmall = pygame.font.SysFont("monospace", 8, True)
            
            storeSpearmanAttackValue = floorMenuStoorFontSmall.render("A: " + str( int( SKILLS.DAMAGE[ "SPEARMAN" ] ) ), 1, (0,0,0))
            storeSpearmanReloadValue = floorMenuStoorFontSmall.render("R: " + str( int( SKILLS.INTERVAL[ "SPEARMAN" ] ) ), 1, (0,0,0))
            storeSpearmanSpeedValue = floorMenuStoorFontSmall.render("S: " + str( int( SKILLS.SPEED[ "SPEARMAN" ] ) ), 1, (0,0,0))
            
            storeSlingerAttackValue = floorMenuStoorFontSmall.render("A: " + str( int( SKILLS.DAMAGE[ "SLINGER" ] ) ), 1, (0,0,0))
            storeSlingerReloadValue = floorMenuStoorFontSmall.render("R: " + str( int( SKILLS.INTERVAL[ "SLINGER" ] ) ), 1, (0,0,0))
            storeSlingerSpeedValue = floorMenuStoorFontSmall.render("S: " + str( int( SKILLS.SPEED[ "SLINGER" ] ) ), 1, (0,0,0))
            
            storeArcherAttackValue = floorMenuStoorFontSmall.render("A: " + str( int( SKILLS.DAMAGE[ "ARCHER" ] ) ), 1, (0,0,0))
            storeArcherReloadValue = floorMenuStoorFontSmall.render("R: " + str( int( SKILLS.INTERVAL[ "ARCHER" ] ) ), 1, (0,0,0))
            storeArcherSpeedValue = floorMenuStoorFontSmall.render("S: " + str( int( SKILLS.SPEED[ "ARCHER" ] ) ), 1, (0,0,0))
            
            storeCatapultAttackValue = floorMenuStoorFontSmall.render("A: " + str( int( SKILLS.DAMAGE[ "CATAPULT" ] ) ), 1, (0,0,0))
            storeCatapultReloadValue = floorMenuStoorFontSmall.render("R: " + str( int( SKILLS.INTERVAL[ "CATAPULT" ] ) ), 1, (0,0,0))
            storeCatapultSpeedValue = floorMenuStoorFontSmall.render("S: " + str( int( SKILLS.SPEED[ "CATAPULT" ] ) ), 1, (0,0,0))
            
            storeCannonAttackValue = floorMenuStoorFontSmall.render("A: " + str( int( SKILLS.DAMAGE[ "CANNON" ] ) ), 1, (0,0,0))
            storeCannonReloadValue = floorMenuStoorFontSmall.render("R: " + str( int( SKILLS.INTERVAL[ "CANNON" ] ) ), 1, (0,0,0))
            storeCannonSpeedValue = floorMenuStoorFontSmall.render("S: " + str( int( SKILLS.SPEED[ "CANNON" ] ) ), 1, (0,0,0))
            
            storeWizardAttackValue = floorMenuStoorFontSmall.render("A: " + str( int( SKILLS.DAMAGE[ "WIZARD" ] ) ), 1, (0,0,0))
            storeWizardReloadValue = floorMenuStoorFontSmall.render("R: " + str( int( SKILLS.INTERVAL[ "WIZARD" ] ) ), 1, (0,0,0))
            storeWizardSpeedValue = floorMenuStoorFontSmall.render("S: " + str( int( SKILLS.SPEED[ "WIZARD" ] ) ), 1, (0,0,0))

            self.screen.blit(storeSpearmanAttackValue, (870, 656))
            self.screen.blit(storeSpearmanReloadValue, (870, 664))
            self.screen.blit(storeSpearmanSpeedValue, (870, 672))

            self.screen.blit(storeSlingerAttackValue, (930, 656))
            self.screen.blit(storeSlingerReloadValue, (930, 664))
            self.screen.blit(storeSlingerSpeedValue, (930, 672))

            self.screen.blit(storeArcherAttackValue, (990, 656))
            self.screen.blit(storeArcherReloadValue, (990, 664))
            self.screen.blit(storeArcherSpeedValue, (990, 672))

            self.screen.blit(storeCatapultAttackValue, (1050, 656))
            self.screen.blit(storeCatapultReloadValue, (1050, 664))
            self.screen.blit(storeCatapultSpeedValue, (1050, 672))

            self.screen.blit(storeCannonAttackValue, (1110, 656))
            self.screen.blit(storeCannonReloadValue, (1110, 664))
            self.screen.blit(storeCannonSpeedValue, (1110, 672))

            self.screen.blit(storeWizardAttackValue, (1170, 656))
            self.screen.blit(storeWizardReloadValue, (1170, 664))
            self.screen.blit(storeWizardSpeedValue, (1170, 672))

    def printTowerFloorHP(self):
        if self.towerFloors[self.activeFloorMenu] != None:
            floorMenuFont = pygame.font.SysFont("monospace", 12, True)

            HPLabel = floorMenuFont.render("HP:", 1, (0,0,0))
            HPValue = floorMenuFont.render(str( self.towerFloors[self.activeFloorMenu].hp ), 1, (0,0,0))

            self.screen.blit(self.hpTexture, (950, 668))
            self.screen.blit(self.hpTexture, (950, 685))
            self.screen.blit(HPLabel, (950, 668))
            self.screen.blit(HPValue, (970, 668))

            FixTowerFloorValue = floorMenuFont.render(str( ((100 * (self.towerFloors[self.activeFloorMenu].level + 1) ) - self.towerFloors[self.activeFloorMenu].hp) * 5 ) + "$", 1, (0,100,0))
            self.screen.blit(FixTowerFloorValue, (980, 685))

    def gameOverLoop(self):
        
        self.screen.blit( self.gameOverTexture, (0, 0) )
        
        buttons = [None]
        buttons[0] = Button(200, 580, "BACKTOMENU")

        for button in buttons:
            button.displayImage(self.screen)

        floorMenuFont = pygame.font.SysFont("monospace", 40, True)
        
        timeLabel = floorMenuFont.render("YOUR TIME:", 1, (200,200,200))
        timeValue = floorMenuFont.render(str( datetime.timedelta( seconds = ( self.count / 60 ) ) ), 1, (250,250,250))

        self.screen.blit( timeLabel, (430, 440) )
        self.screen.blit( timeValue, (680, 440) )

        pygame.display.flip()

        continueLoop = True 

        while continueLoop:

            eventQueue = pygame.event.get()
            for event in eventQueue:
                
                if event.type == pygame.QUIT:
                    self.onExit()
                    self.state = STATE.EXIT
                    self.stop()
                    continueLoop = False
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    for button in buttons:
                        x, y = event.pos
                        if button.isHit(x, y):

                            print button.name
                
                            if button.name == "BACKTOMENU":
                                self.state = STATE.STOPPED
                                self.stop()
                                continueLoop = False

    def drawTower(self):
        if self.targetFloor == 0:
            self.towerFloors[0] = TowerFloor( self.world, 1,  999/self.PPM, 476/self.PPM ,["resources/brick1.png", "resources/stone1.png"], 100 )
            self.towerFloors[1] = TowerFloor( self.world, 2, 1012/self.PPM, 392/self.PPM ,["resources/brick2.png", "resources/stone2.png"], 100 )
            self.towerFloors[2] = TowerFloor( self.world, 3, 1023/self.PPM, 308/self.PPM ,["resources/brick3.png", "resources/stone3.png"], 100 )
            self.towerFloors[3] = TowerFloor( self.world, 4, 1016/self.PPM, 140/self.PPM ,["resources/brick4.png", "resources/stone4.png"], 100 )
            self.towerFloors[0].setDefender("NONE")
            self.towerFloors[1].setDefender("NONE")
            self.towerFloors[2].setDefender("NONE")
            self.towerFloors[3].setDefender("NONE")
        elif self.targetFloor == 1:
            floor1 = self.towerFloors[1]
            floor2 = self.towerFloors[2]
            floor3 = self.towerFloors[3]
            self.towerFloors[0] = None
            self.towerFloors[1] = TowerFloor( self.world, 2,  1012/self.PPM, 476/self.PPM ,["resources/brick2.png", "resources/stone2.png"], floor1.hp )
            self.towerFloors[2] = TowerFloor( self.world, 3, 1023/self.PPM, 392/self.PPM ,["resources/brick3.png", "resources/stone3.png"], floor2.hp )
            self.towerFloors[3] = TowerFloor( self.world, 4, 1016/self.PPM, 224/self.PPM ,["resources/brick4.png", "resources/stone4.png"], floor3.hp )
            self.towerFloors[1].defender = floor1.defender
            self.towerFloors[2].defender = floor2.defender
            self.towerFloors[3].defender = floor3.defender
            self.towerFloors[1].level = floor1.level
            self.towerFloors[2].level = floor2.level
            self.towerFloors[3].level = floor3.level
        elif self.targetFloor == 2:
            floor2 = self.towerFloors[2]
            floor3 = self.towerFloors[3]
            self.towerFloors[0] = None
            self.towerFloors[1] = None
            self.towerFloors[2] = TowerFloor( self.world, 3,  1023/self.PPM, 476/self.PPM ,["resources/brick3.png", "resources/stone3.png"], floor2.hp )
            self.towerFloors[3] = TowerFloor( self.world, 4, 1016/self.PPM, 308/self.PPM ,["resources/brick4.png", "resources/stone4.png"], floor3.hp )
            self.towerFloors[2].defender = floor2.defender
            self.towerFloors[3].defender = floor3.defender
            self.towerFloors[2].level = floor2.level
            self.towerFloors[3].level = floor3.level
        elif self.targetFloor == 3:
            floor3 = self.towerFloors[3]
            self.towerFloors[0] = None
            self.towerFloors[1] = None
            self.towerFloors[2] = None
            self.towerFloors[3] = TowerFloor( self.world, 4,  1016/self.PPM, 392/self.PPM ,["resources/brick4.png", "resources/stone4.png"], floor3.hp )
            self.towerFloors[3].defender = floor3.defender
            self.towerFloors[3].level = floor3.level

    def drawDefenders(self):
        if self.targetFloor == 0:
            self.screen.blit( self.towerFloors[0].defender.image, ( 1069, 486 ) )
            self.screen.blit( self.towerFloors[1].defender.image, ( 1069, 406 ) )
            self.screen.blit( self.towerFloors[2].defender.image, ( 1069, 322 ) )
            self.screen.blit( self.towerFloors[3].defender.image, ( 1069, 238 ) )
        elif self.targetFloor == 1:
            self.screen.blit( self.towerFloors[1].defender.image, ( 1069, 486 ) )
            self.screen.blit( self.towerFloors[2].defender.image, ( 1069, 406 ) )
            self.screen.blit( self.towerFloors[3].defender.image, ( 1069, 322 ) )
        elif self.targetFloor == 2:
            self.screen.blit( self.towerFloors[2].defender.image, ( 1069, 486 ) )
            self.screen.blit( self.towerFloors[3].defender.image, ( 1069, 406 ) )
        elif self.targetFloor == 3:
            self.screen.blit( self.towerFloors[3].defender.image, ( 1069, 486 ) )
        
    def drawButtoms(self):
        if self.targetFloor == 0:
            self.buttons[0] = Button(1049, 486, "FLOOR1")
            self.buttons[1] = Button(1049, 406, "FLOOR2")
            self.buttons[2] = Button(1049, 322, "FLOOR3")
            self.buttons[3] = Button(1049, 238, "FLOOR4")
            self.buttons[4] = Button(1230, 20, "SHOWMENU")
        elif self.targetFloor == 1:
            self.buttons[0] = None
            self.buttons[1] = Button(1049, 486, "FLOOR2")
            self.buttons[2] = Button(1049, 406, "FLOOR3")
            self.buttons[3] = Button(1049, 322, "FLOOR4")
        elif self.targetFloor == 2:
            self.buttons[1] = None
            self.buttons[2] = Button(1049, 486, "FLOOR3")
            self.buttons[3] = Button(1049, 406, "FLOOR4")
        elif self.targetFloor == 3:
            self.buttons[2] = None
            self.buttons[3] = Button(1049, 486, "FLOOR4")

    def drawChosenFloorMenu(self):
        if self.targetFloor == 0:
            if self.activeFloorMenu == 0:
                self.screen.blit( self.chosenFloorTexture, ( 1069, 486 ) )
            if self.activeFloorMenu == 1:
                self.screen.blit( self.chosenFloorTexture, ( 1069, 406 ) )
            if self.activeFloorMenu == 2:
                self.screen.blit( self.chosenFloorTexture, ( 1069, 322 ) )
            if self.activeFloorMenu == 3:
                self.screen.blit( self.chosenFloorTexture, ( 1069, 238 ) )
        elif self.targetFloor == 1:
            if self.activeFloorMenu == 1:
                self.screen.blit( self.chosenFloorTexture, ( 1069, 486 ) )
            if self.activeFloorMenu == 2:
                self.screen.blit( self.chosenFloorTexture, ( 1069, 406 ) )
            if self.activeFloorMenu == 3:
                self.screen.blit( self.chosenFloorTexture, ( 1069, 322 ) )
        elif self.targetFloor == 2:
            if self.activeFloorMenu == 2:
                self.screen.blit( self.chosenFloorTexture, ( 1069, 486 ) )
            if self.activeFloorMenu == 3:
                self.screen.blit( self.chosenFloorTexture, ( 1069, 406 ) )
        elif self.targetFloor == 3:
            if self.activeFloorMenu == 3:
                self.screen.blit( self.chosenFloorTexture, ( 1069, 486 ) )

