import pygame
from pygame.locals import *
import Box2D
from Box2D.b2 import *
from Enum import *

class VikingFactory():

	world = None
	body = None
	image = None

	B2HEIGTH = 2
	B2WIDTH = 1
	DENSITY = 1
	FRICTION = 0
	ANGLE = 0
	LINEAR_VELOCITY = vec2(5, 0)

	def __init__(self, world, xPos, yPos):
		self.world = world

		self.body = self.world.CreateDynamicBody(position=(xPos, yPos), angle=self.ANGLE)
		self.body.CreatePolygonFixture(box=(self.B2WIDTH, self.B2HEIGTH), density=self.DENSITY, friction=self.FRICTION)
		self.body.linearVelocity = self.LINEAR_VELOCITY

		self.image = pygame.image.load(PARAMS.IMAGEPATH + BUTTONS.names["VIKING"])
		self.image = self.image.convert()

		self.body.userData = ["viking", self.image]