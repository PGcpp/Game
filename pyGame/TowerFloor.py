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

                self.defender = Defender( self.world, x, y, SKILLS.INTERVAL[ defenderName ], SKILLS.DAMAGE[ defenderName ], 'resources/defender_'+defenderName.lower()+'.png', defenderName )
                self.defender.addBullet(1, 1, SKILLS.SPEED[ defenderName ], SKILLS.MAXDISTANCE[ defenderName ], BULLETSPRITE.name[ defenderName ] )

        def upgrade(self):
                self.level += 1
                self.hp = 100 * ( self.level + 1 )

                
                

