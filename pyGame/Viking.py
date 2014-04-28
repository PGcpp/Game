import pygame
from pygame.locals import *
import Box2D
from Box2D.b2 import *
from Enum import *

class Viking():

	world = None
	body = None
	image = None
	
	name = None
	attackInterval = 60
	damage = 100
	health = None
	speed = None
	vikingId = 0
	money = 100
	targeted = False

	B2HEIGTH = 2
	B2WIDTH = 1
	DENSITY = 1
	FRICTION = 0
	ANGLE = 0

	def __init__(self, world, name, vikingId, xPos, yPos):
		self.world = world

		self.body = self.world.CreateDynamicBody(position=(xPos, yPos), angle=self.ANGLE)
		self.body.CreatePolygonFixture(box=(self.B2WIDTH, self.B2HEIGTH), density=self.DENSITY, friction=self.FRICTION, categoryBits=CATEGORY.VIKING, maskBits=CATEGORY.GROUND)
		self.name = name
		self.vikingId = vikingId
		self.setInitParameters()

		self.body.userData = [VIKING.NOT_HIT, self.image, self.vikingId, 0]

	def setInitParameters(self):

		if self.name == VIKING.TYPE_1:
			self.attackInterval = 60
			self.damage = 100
			self.health = 100
			self.speed = 5
			self.money = 100
			self.image = pygame.image.load(PARAMS.IMAGEPATH + "viking1.png")

		if self.name == VIKING.TYPE_2:
			self.attackInterval = 60
			self.damage = 200
			self.health = 200
			self.speed = 7
			self.money = 200
			self.image = pygame.image.load(PARAMS.IMAGEPATH + "viking2.png")

		if self.name == VIKING.TYPE_3:
			self.attackInterval = 60
			self.damage = 400
			self.health = 400
			self.speed = 3
			self.money = 400
			self.image = pygame.image.load(PARAMS.IMAGEPATH + "viking3.png")

		self.body.linearVelocity = vec2(self.speed, 0)
		self.image = self.image.convert()

	def getPosition(self):
		return self.body.position[0]
