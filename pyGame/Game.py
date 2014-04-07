import pygame
from pygame.locals import *
from sys import exit

try:
	from DefenseScene import *
	from Buttom import *
except ImportError:
	print "\nUnable to import library class\n"
	sys.exit(2)

class Game():

	screenSize = (800, 600)
	bufferMode = DOUBLEBUF
	screen = None
	buttoms = []
	endOfGame = False
	
	def __init__(self):
		pygame.init()
		
		icon = pygame.image.load("resources/icon.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption("Vikings Defense")
		self.screen = pygame.display.set_mode(self.screenSize, self.bufferMode)
		self.drawBackground()
		self.buttoms.append(Buttom(300, 100, "NEW_GAME"))
		self.buttoms.append(Buttom(300, 250, "OPTIONS"))
		self.buttoms.append(Buttom(300, 400, "EXIT"))


		self.menuLoop()
		self.game_exit()
	
	def menu(self):
		pass
					
	def gameExit(self):
		self.endOfGame = True
		print("exit")
		exit()
		
	def menuLoop(self):		
		while not self.endOfGame:
			for event in pygame.event.get():
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					self.endOfGame = True
					self.gameExit()
				self.mouseEvents(event)
				self.drawMenu()
			
	def mouseEvents(self, event):
		if event.type == pygame.MOUSEBUTTONUP:
			for buttom in self.buttoms:
				x, y = event.pos
				if buttom.isHit(x, y):
					if buttom.name == "NEW_GAME":
						DefenseScene(self.screen)
						self.drawBackground()
					elif buttom.name == "OPTIONS":
						print "options!"
					elif buttom.name == "EXIT":
						self.gameExit()

	def drawMenu(self):
		for buttom in self.buttoms:
			buttom.displayImage(self.screen)

	def drawBackground(self):
		image = pygame.image.load("resources/background.png")
		self.screen.blit(image, (0, 0))
		pygame.display.flip()


	def scaleDisplayImage(self, sourcePath, xPos, yPos, xScale, yScale):
		image = pygame.image.load(sourcePath)
		imageScaled = pygame.transform.scale(image, (xScale, yScale))
		self.screen.blit(imageScaled, (xPos, yPos))
		pygame.display.flip()


if __name__ == "__main__":
	Game()