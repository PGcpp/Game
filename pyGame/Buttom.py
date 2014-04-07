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

	names = {
	#generic buttom
	"DEFAULT": "buttom.png",
	#main menu
	"NEW_GAME": "buttom.png",
	"OPTIONS": "buttom.png",
	"EXIT": "buttom.png"
	#actual game buttoms
	}