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
	damage = 10
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

                #tworzenie wikinga w zaleznosci od jego typu
		if self.name == VIKING.TYPE_1:
			self.attackInterval = VIKING.TYPE_1["ATTACKINTERVAL"]
			self.damage = VIKING.TYPE_1["DAMAGE"]
			self.health = VIKING.TYPE_1["HEALTH"]
			self.speed = VIKING.TYPE_1["SPEED"]
			self.money = VIKING.TYPE_1["MONEY"]
			self.image = pygame.image.load(PARAMS.IMAGEPATH + VIKING.TYPE_1["IMAGE"])

		if self.name == VIKING.TYPE_2:
			self.attackInterval = VIKING.TYPE_2["ATTACKINTERVAL"]
			self.damage = VIKING.TYPE_2["DAMAGE"]
			self.health = VIKING.TYPE_2["HEALTH"]
			self.speed = VIKING.TYPE_2["SPEED"]
			self.money = VIKING.TYPE_2["MONEY"]
			self.image = pygame.image.load(PARAMS.IMAGEPATH + VIKING.TYPE_2["IMAGE"])

		if self.name == VIKING.TYPE_3:
			self.attackInterval = VIKING.TYPE_3["ATTACKINTERVAL"]
			self.damage = VIKING.TYPE_3["DAMAGE"]
			self.health = VIKING.TYPE_3["HEALTH"]
			self.speed = VIKING.TYPE_3["SPEED"]
			self.money = VIKING.TYPE_3["MONEY"]
			self.image = pygame.image.load(PARAMS.IMAGEPATH + VIKING.TYPE_3["IMAGE"])

                #ruch wikinga
		self.body.linearVelocity = vec2(self.speed, 0)
		self.image = self.image.convert_alpha()

	def getPosition(self):
		return self.body.position[0]
