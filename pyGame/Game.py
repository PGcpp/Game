import pygame
from pygame.locals import *
from sys import exit

try:
	from Warrior import *
except ImportError:
	print "\nUnable to import Warrior class\n"
	sys.exit(2)

class Game():

	screenSize = (800, 600)
	bufferMode = DOUBLEBUF
	screen = None
	
	player = None
	endOfGame = False
	
	def __init__(self):
		pygame.init()
		
		icon = pygame.image.load("resources/icon.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption("Vikings Defense")
		
		self.screen = pygame.display.set_mode(self.screenSize, self.bufferMode)
		self.displayImage("resources/background.png", 0, 0)
		
		#warrior1 = Warrior(self.screen)
		self.player = Warrior(self.screen, 200, 300)
		
		self.mainLoop()
		self.game_exit()
					
					
	def gameExit(self):
		self.endOfGame = True
		print("game over")
		exit()
		
	def mainLoop(self):		
		while not self.endOfGame:
			for event in pygame.event.get():
				self.mouseEvents(event)
				if event.type == pygame.QUIT:
					self.gameExit()
			
	def mouseEvents(self, event):
		if event.type == pygame.MOUSEBUTTONUP:
			print event.pos
			x,y = event.pos
		
		keys = pygame.key.get_pressed()

		if keys[K_s]:
			self.player.move(0,1)

		if keys[K_w]:
			self.player.move(0,-1)
		
		if keys[K_d]:
			self.player.move(1,0)

		if keys[K_a]:
			self.player.move(-1,0)
		
		self.screen.fill((0,0,0))
		self.displayImage("resources/background.png", 0, 0)
		self.screen.blit(self.player.image, (self.player.xPos, self.player.yPos))
		pygame.display.flip()
			
		#xBoard, yBoard = self.computeBoardPosition(x,y)
		#self.scaleDisplayImage("resources/cross.png", xBoard, yBoard, 120, 120)
			
	def computeBoardPosition(self, x, y):
		if x < 250:
			return 120, 180
		elif x > 250 and x < 500:
			return 255, 180
		else:
			return 380, 180
			
	def displayImage(self, sourcePath, x, y):
			image = pygame.image.load(sourcePath)
			self.screen.blit(image, (x, y))
			pygame.display.flip()
			
	def scaleDisplayImage(self, sourcePath, xPos, yPos, xScale, yScale):
			image = pygame.image.load(sourcePath)
			imageScaled = pygame.transform.scale(image, (xScale, yScale))
			self.screen.blit(imageScaled, (xPos, yPos))
			pygame.display.flip()
		

if __name__ == "__main__":
	Game()