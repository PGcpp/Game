import pygame
from pygame.locals import *
import Box2D
from Box2D.b2 import *
from Enum import *

class Bullet():

	body = None
	
	#parametry body:
	B2HEIGTH = None
	B2WIDTH = None
	DENSITY = 1
	FRICTION = 0.3
	ANGLE = 0

        #pozostale parametry:
        image = None
	speed = None #ile metrow w ciagu sekundy pokonuje
	damage = None #ile procent zycia zabiera bez uwzglednienia zbroi

	def __init__(self, width, height, speed, damage, image):
                self.B2WIDTH = width
                self.B2HEIGTH = height
                self.speed = speed
                self.damage = damage
                self.image = pygame.image.load( image )
                self.image = self.image.convert()
