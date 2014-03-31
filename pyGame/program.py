import pygame
from pygame.locals import *

class Game():

	endOfGame = False
	screenSize = (800, 600)
	bufferMode = DOUBLEBUF
	
	def __init__(self):
		pygame.init()
		
		icon = pygame.image.load("resources/icon.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption("Vikings Defense")
		
		screen = pygame.display.set_mode(self.screenSize, self.bufferMode)
		self.displayImage("resources/background.png", 0, 0, screen)
		
		self.mainLoop(screen)
					
					
	def gameExit(self):
		self.endOfGame = True
		print("game over")
		
	def mainLoop(self, screen):		
		while not self.endOfGame:
			for event in pygame.event.get():
				self.mouseEvents(event, screen)
				if event.type == pygame.QUIT:
					self.gameExit()
			
	def mouseEvents(self, event, screen):
		if event.type == pygame.MOUSEBUTTONUP:
			print event.pos
			x,y = event.pos
			xBoard, yBoard = self.computeBoardPosition(x,y)
			self.scaleDisplayImage("resources/cross.png", xBoard, yBoard, 120, 120, screen)
			
	def computeBoardPosition(self, x, y):
		if x < 250:
			return 120, 180
		elif x > 250 and x < 500:
			return 255, 180
		else:
			return 380, 180
			
	def displayImage(self, sourceName, x, y, screen):
			image = pygame.image.load(sourceName)
			screen.blit(image, (x, y))
			pygame.display.flip()
			
	def scaleDisplayImage(self, sourceName, xPos, yPos, xScale, yScale, screen):
			image = pygame.image.load(sourceName)
			imageScaled = pygame.transform.scale(image, (xScale, yScale))
			screen.blit(imageScaled, (xPos, yPos))
			pygame.display.flip()
		

if __name__ == "__main__":
	Game()