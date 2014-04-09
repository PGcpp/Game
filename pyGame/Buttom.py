import pygame

class Buttom():

	WIDTH = 200
	HEIGTH = 100
	IMAGEPATH = "resources/"
	
	xPos = 0
	yPos = 0
	image = None
	name = ""
		
	def __init__(self, xPos=0, yPos=0, buttomName="buttom.png"):
		self.xPos = xPos
		self.yPos = yPos		
		self.name = buttomName
		self.image = pygame.image.load(self.IMAGEPATH + self.names[buttomName])
		
	def displayImage(self, screen):
                screen.blit(self.image, (self.xPos, self.yPos))
                pygame.display.flip()

	def isHit(self, xPos, yPos):
		if xPos > self.xPos and xPos < (self.xPos + self.WIDTH) and yPos > self.yPos and yPos < (self.yPos + self.HEIGTH):
			return True
		else:
			return False

	def dispose(self):
                pass
                #self.screen = None
                #self.image = None

	names = {
	#generic buttom
	"DEFAULT": "playButton.png",
	#main menu
	"NEW_GAME": "playButton.png",
	"OPTIONS": "settingsButton.png",
	"EXIT": "exitButton.png"
	#actual game buttoms
	}
