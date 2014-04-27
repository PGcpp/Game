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
	attack = None
	health = None
	speed = None
	vikingId = 0

	B2HEIGTH = 2
	B2WIDTH = 1
	DENSITY = 1
	FRICTION = 0
	ANGLE = 0

	def __init__(self, world, name, vikingId, xPos, yPos):
		self.world = world

		self.body = self.world.CreateDynamicBody(position=(xPos, yPos), angle=self.ANGLE)
		self.body.CreatePolygonFixture(box=(self.B2WIDTH, self.B2HEIGTH), density=self.DENSITY, friction=self.FRICTION)
		self.name = name
		self.vikingId = vikingId
		self.setInitParameters()

		self.body.userData = [VIKING.NOT_HIT, self.image, self.vikingId]

	def setInitParameters(self):

		if self.name == VIKING.TYPE_1:
			self.attack = 100
			self.health = 100
			self.speed = 5
			self.image = pygame.image.load(PARAMS.IMAGEPATH + "viking1.png")

		if self.name == VIKING.TYPE_2:
			self.attack = 200
			self.health = 200
			self.speed = 7
			self.image = pygame.image.load(PARAMS.IMAGEPATH + "viking2.png")

		if self.name == VIKING.TYPE_3:
			self.attack = 400
			self.health = 400
			self.speed = 3
			self.image = pygame.image.load(PARAMS.IMAGEPATH + "viking3.png")

		self.body.linearVelocity = vec2(self.speed, 0)
		self.image = self.image.convert()
