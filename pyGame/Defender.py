import pygame
from pygame.locals import *
import Box2D
from Box2D.b2 import *
import datetime
from Enum import *
from Bullet import *
import Settings

class Defender():

	world = None
	body = None

	B2HEIGTH = 1
	B2WIDTH = 1
	DENSITY = 1
	FRICTION = 0.3
	ANGLE = 0

        image = None
        icon = None
        interval = None

        maxDistance = None
        
	bullets = []
	xPos = None
	yPos = None

	name = None
	sound = None

	chosenBulletType = 0
	bulletsAmount = 0

	def __init__(self, world, xPos, yPos, interval, maxDistance, image, name):
		self.world = world
		self.xPos = xPos
		self.yPos = yPos
		self.interval = interval
		self.maxDistance = maxDistance
		self.bullets = []

		self.body = self.world.CreateStaticBody(position=(self.xPos, self.yPos), angle=self.ANGLE)
		self.body.CreatePolygonFixture(box=(self.B2WIDTH, self.B2HEIGTH), density=self.DENSITY, friction=self.FRICTION) 

                self.name = name

		self.image = pygame.image.load(image)
		self.image = self.image.convert_alpha()

		self.icon = pygame.image.load('resources/defenderIco_'+self.name.lower()+'.png')
                self.icon = self.icon.convert_alpha()

                self.sound = pygame.mixer.Sound( BULLETMUSIC.name[ self.name ])
                self.sound.set_volume( Settings.getEffectsLevel() )

		self.body.userData = ["defender", self.image]

        def getYVelocity(self, time, base):
                Vy = ( (5.0 * (time * time) ) - base ) / time
                return Vy

        def getXVelocity(self, time, distance):
                Vx = distance / time
                return Vx

	def shoot(self, distance):
                if distance <= self.maxDistance and distance > 0: 
                        
                        if self.bulletsAmount > 0 :
                                
                                i = self.chosenBulletType

                                print "##",str(i),"   ",str(len(self.bullets))
                                
                                bullet = self.bullets[i]
                                
                                bulletBody = self.world.CreateDynamicBody(position=(self.xPos - 1, self.yPos), angle=bullet.ANGLE) 
                                bulletBody.CreatePolygonFixture(box=(bullet.B2WIDTH, bullet.B2HEIGTH), density=bullet.DENSITY, friction=bullet.FRICTION) 
                                bulletBody.mass = 1  
                                bulletBody.fixtures[0].sensor = True
                                bulletBody.userData = [BULLET.NOT_HIT, bullet.image, bullet.damage]

                                time = distance / bullet.speed
                                
                                Vy = self.getYVelocity(time, self.yPos - 4 + 1) 
                                Vx = self.getXVelocity(time, distance)

                                self.sound.play() 
                                bulletBody.ApplyLinearImpulse( vec2( -Vx , Vy), (self.xPos - 1, self.yPos), True ) 


        def addBullet(self, width, height, speed, damage, image):
                self.bullets.append( Bullet(width, height, speed, damage, image) )
                self.bulletsAmount += 1

        def upgradeDamage(self):
                if self.name != "NONE":
                        self.bullets[ self.chosenBulletType ].damage += SKILLS.STEP

        def upgradeSpeed(self):
                if self.name != "NONE":
                        self.bullets[ self.chosenBulletType ].speed += SKILLS.STEP

        def upgradeInterval(self):
                if self.name != "NONE" and self.interval >= ( SKILLS.MINVALUE ):   
                        self.interval -= SKILLS.STEP

        def getDamage(self):
                return self.bullets[ self.chosenBulletType ].damage

        def getInterval(self):
                return self.interval

        def getSpeed(self):
                return self.bullets[ self.chosenBulletType ].speed

        def dispose(self):
                self.bullets = []

        
        
