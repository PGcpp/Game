import pygame
from pygame.locals import *
import Box2D
from Box2D.b2 import *
from Enum import *

class Bullet():

	body = None
	
	B2HEIGTH = None
	B2WIDTH = None
	DENSITY = 1
	FRICTION = 0.3
	ANGLE = 0

	image = None
	speed = None 
	damage = None

	def __init__(self, width, height, speed, damage, image):
                self.B2WIDTH = width
                self.B2HEIGTH = height
                self.speed = speed
                self.damage = damage
                self.image = pygame.image.load( image )
                self.image = self.image.convert_alpha()
