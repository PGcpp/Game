import pygame
from pygame.locals import *
import Box2D
from Box2D.b2 import *
from Enum import *
from Defender import *
import math

class TowerFloor():

	xPos = None
	yPos = None

	defender = None

        #pozostale parametry:
	floorNumber = None
        image = []
        level = None
        hp = None

        defender = None

	def __init__(self, world, floorNumber, xPos, yPos, images, hp):
                self.world = world
                self.floorNumber = floorNumber
                self.xPos = xPos
                self.yPos = yPos
                
                self.image = images
                for i in range( len(self.image) ):
                        self.image[i] = pygame.image.load( self.image[i] ).convert_alpha()

                self.hp = hp

                self.level = 0

        def setDefender(self, defenderName):

                x = 55.0
                y = 36.0 - self.yPos - self.image[self.level].get_size()[1]/20.0 - 4.2 #4.2 dobrane na pale zeby pasowalo

                print "X: ",x,"   Y: ",y
                
                if defenderName == "NONE":
                        self.defender = Defender( self.world, x, y, -1, 'resources/defender_none.png', "NONE")
                        self.defender.addBullet(1, 1, 5, 10, 'resources/bullet1.png')
                elif defenderName == "SPEARMAN":
                        self.defender = Defender( self.world, x, y, -1, 'resources/defender_spearman.png', "SPEARMAN")
                        self.defender.addBullet(1, 1, 30, 10, 'resources/bullet1.png')
                elif defenderName == "SLINGER":
                        self.defender = Defender( self.world, x, y, -1, 'resources/defender_slinger.png', "SLINGER")
                        self.defender.addBullet(1, 1, 30, 10, 'resources/bullet1.png')
                elif defenderName == "ARCHER":
                        self.defender = Defender( self.world, x, y, -1, 'resources/defender_archer.png', "ARCHER")
                        self.defender.addBullet(1, 1, 30, 10, 'resources/bullet1.png')
                elif defenderName == "CATAPULT":
                        self.defender = Defender( self.world, x, y, -1, 'resources/defender_catapult.png', "CATAPULT")
                        self.defender.addBullet(1, 1, 30, 10, 'resources/bullet1.png')
                elif defenderName == "CANNON":
                        self.defender = Defender( self.world, x, y, -1, 'resources/defender_cannon.png', "CANNON")
                        self.defender.addBullet(1, 1, 30, 10, 'resources/bullet1.png')
                elif defenderName == "WIZARD":
                        self.defender = Defender( self.world, x, y, -1, 'resources/defender_wizard.png', "WIZARD")
                        self.defender.addBullet(1, 1, 30, 10, 'resources/bullet1.png')


                
                

