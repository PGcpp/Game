import pygame
from pygame.locals import *
import Box2D
from Box2D.b2 import *
from Enum import *
from Bullet import *

class Defender():

	world = None
	body = None

	B2HEIGTH = 1
	B2WIDTH = 1
	DENSITY = 1
	FRICTION = 0.3
	ANGLE = 0

        image = None
        interval = None #jak czesto moze strzelac
	bullets = [] #typy pociskow ktorymi moze strzelac
	xPos = None
	yPos = None

	chosenBulletType = 0 #aktualnie wybrany rodzaj pocisku
	bulletsAmount = 0 #aktualna ilosc dostepnych pociskow

	def __init__(self, world, xPos, yPos, interval):
		self.world = world
		self.xPos = xPos
		self.yPos = yPos
		self.interval = interval
		self.bullets = []

		self.body = self.world.CreateStaticBody(position=(self.xPos, self.yPos), angle=self.ANGLE)
		self.body.CreatePolygonFixture(box=(self.B2WIDTH, self.B2HEIGTH), density=self.DENSITY, friction=self.FRICTION) 

		self.image = pygame.image.load(PARAMS.IMAGEPATH + BUTTONS.names["VIKING"])
		self.image = self.image.convert()

		self.body.userData = ["defender", self.image]

        #jak dlugo chce zeby lecialo
        def getYVelocity(self, time, base):
                Vy = ( (5.0 * (time * time) ) - base ) / time
                return Vy

        #i jaki dystans osiagnelo
        def getXVelocity(self, time, distance):
                Vx = distance / time
                return Vx

        #potrzebujemy odleglosc na ktora mamy wystrzelic pocisk -> algorytm wykrywajacy punkt zderzenia z wikingiem w defenseScene
	def shoot(self, distance):

                i = self.chosenBulletType
                bullet = self.bullets[i]
                
                #bulletBody = self.world.CreateDynamicBody(position=(self.xPos - 1, self.yPos), angle=bullet.ANGLE) #chcemy utworzyc pocisk obok defendera a nie na nim stad self.xPos - 1
		##bulletBody.CreatePolygonFixture(box=(bullet.B2WIDTH, bullet.B2HEIGTH), density=bullet.DENSITY, friction=bullet.FRICTION) 
                #bulletBody.mass = 1  #bardzo wazne! zmiana masy totalnie wszystko zmienia - czasem lotu pocisku manipulujemy za pomoca speed
                #bulletBody.fixtures[0].sensor = True
		#bulletBody.userData = ["bullet", bullet.image]

                #pocisk stworzony teraz strzal
		print "LEN: " + str( len( self.bullets ) )
                print "SPEED:" + str(bullet.speed)
                print "BULLETS: " + str(self.bulletsAmount)
                time = distance / bullet.speed
                
                Vy = self.getYVelocity(time, self.yPos - 8 + 1) #bo na wysokosci 8 znajduje sie ziemia, a 1 bo chcemy trafic w srodek ciala wikinga [wiking ma wysokosc 2 stad chcemy trafic w punkt 1 nad ziemia]
                Vx = self.getXVelocity(time, distance)

                #BUM!
                #bulletBody.ApplyLinearImpulse( vec2( -Vx , Vy), (self.xPos - 1, self.yPos - 0.1), True ) # -Vx bo chcemy strzelac z prawej strony w lewa [wieze mamy po prawej przeciwnicy z lewej]
                                                                                                   # a self.xPos - 1 bo pocisk utworzony w self.xPos - 1, chcemy przylozyc sile w jego srodku
                #pocisk wystrzelony modyfikacja userData
		
                #bulletBody.userData[0] = "bulletShooted"

        def addBullet(self, width, height, speed, damage, image):
                self.bullets.append( Bullet(width, height, speed, damage, image) )
                self.bulletsAmount += 1

        
        
