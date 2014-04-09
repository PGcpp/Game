import pygame
from pygame.locals import *
from Buttom import *
from Enum import *

import Scene
import DefenseScene
from sys import exit

class MenuScene(Scene.Scene):

    screen = None
    buttoms = []
    state = 0
    image = None

    def MenuScene(screen):
        super(screen)
        self.screen = screen
        

    def prepare(self):
        self.image = pygame.image.load("resources/background.png")
        self.buttoms.append(Buttom(300, 100, "MENU.PLAY"))
        self.buttoms.append(Buttom(300, 250, "MENU.OPTIONS"))
        self.buttoms.append(Buttom(300, 400, "STATE.EXIT"))

        self.drawBackground()

    def step(self):
        for event in self.eventQueue:
            self.checkButton(event)
        for buttom in self.buttoms:
            buttom.displayImage(self.screen)

    def drawBackground(self):
        self.screen.blit(self.image, (0, 0))
        pygame.display.flip()

    def dispose(self):
        for buttom in self.buttoms:
            buttom.dispose()

    def checkButton(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for buttom in self.buttoms:
                x, y = event.pos
                if buttom.isHit(x, y):
                    print buttom.name
                    if buttom.name == "MENU.PLAY":
                        self.state = MENU.PLAY
                        self.stop()

                    elif buttom.name == "MENU.OPTIONS":
                        self.state = MENU.OPTIONS

                    elif buttom.name == "STATE.EXIT":
                        self.state = STATE.EXIT
                        self.stop()

