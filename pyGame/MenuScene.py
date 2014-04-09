import pygame
from pygame.locals import *
from Buttom import *
from Enum import *
import time
import Scene
import DefenseScene
from sys import exit

class MenuScene(Scene.Scene):

    screen = None
    buttoms = [None, None, None]
    state = 0
    menuSound = None

    def MenuScene(screen):
        self.screen = screen
        

    def prepare(self):
        self.menuSound = pygame.mixer.Sound("resources/menu.wav")
        self.menuSound.play(-1)
        
        self.drawBackground()

        self.buttoms[0] = Buttom(300, 100, "NEW_GAME")
        self.buttoms[1] = Buttom(300, 250, "OPTIONS")
        self.buttoms[2] = Buttom(300, 400, "EXIT")

        for buttom in self.buttoms:
            buttom.displayImage(self.screen)

    def step(self):
        for event in self.eventQueue:
            self.checkButton(event)

    def drawBackground(self):
        image = pygame.image.load("resources/background.png")
        self.screen.blit(image, (0, 0))
        pygame.display.flip()

    def dispose(self):
        for buttom in self.buttoms:
            buttom.dispose()
        self.buttoms = [None]
        self.menuSound.stop()

    def checkButton(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for buttom in self.buttoms:
                x, y = event.pos
                if buttom.isHit(x, y):
                    print buttom.name
                    if buttom.name == "NEW_GAME":
                        self.stop()
                        self.state = MENU.PLAY

                    elif buttom.name == "OPTIONS":
                        self.state = MENU.OPTIONS
                        self.stop()

                    elif buttom.name == "EXIT":
                        self.state = STATE.EXIT
                        self.stop()
        

