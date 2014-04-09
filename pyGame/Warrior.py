import pygame
import Box2D
from Box2D.b2 import *


class Warrior():

	xPos = 0
	yPos = 0
	speed = 1.2
	imagePath = "resources/warrior.png"
	image = None
		
	def __init__(self, screen, xPos=0, yPos=0):
		self.xPos = xPos
		self.yPos = yPos
		self.displayImage(self.xPos, self.yPos, screen)
		
	def move(self, x, y):
		   self.xPos = self.xPos + (x * self.speed)
		   self.yPos = self.yPos + (y * self.speed)
				
		
	def displayImage(self, xPos, yPos, screen):
			self.image = pygame.image.load(self.imagePath)
			screen.blit(self.image, (xPos, yPos))
			pygame.display.flip()