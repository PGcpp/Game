import pygame
from Enum import *

class Button():
	
	width = None
	height = None
	image = None
	xPos = 0
	yPos = 0
	name = ""
		
	def __init__(self, xPos=0, yPos=0, buttonName="DEFAULT"):
		self.xPos = xPos
		self.yPos = yPos		
		self.name = buttonName
		
		self.image = pygame.image.load(PARAMS.IMAGEPATH + BUTTONS.names[buttonName]).convert_alpha()
		self.width, self.height = self.image.get_size()
		
	def displayImage(self, screen, doFlip = True):
                screen.blit(self.image, (self.xPos, self.yPos))
                if doFlip:
                        pygame.display.flip()

	def isHit(self, xPos, yPos):
		if xPos > self.xPos and xPos < (self.xPos + self.width) and yPos > self.yPos and yPos < (self.yPos + self.height):
			return True
		else:
			return False

	def dispose(self):
                pass
