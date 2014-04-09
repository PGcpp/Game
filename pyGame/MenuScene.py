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

    def MenuScene(screen):
        super(screen)
        self.screen = screen
        

    def prepare(self):
        self.buttoms.append(Buttom(300, 100, "NEW_GAME"))
        self.buttoms.append(Buttom(300, 250, "OPTIONS"))
        self.buttoms.append(Buttom(300, 400, "EXIT"))

        self.drawBackground()

    def step(self):
        for event in self.eventQueue:
            self.checkButton(event)
        for buttom in self.buttoms:
            buttom.displayImage(self.screen)

    def drawBackground(self):
        image = pygame.image.load("resources/background.png")
        self.screen.blit(image, (0, 0))
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
                    if buttom.name == "NEW_GAME":
                        self.state = MENU.PLAY
                        self.stop()

                    elif buttom.name == "OPTIONS":
                        self.state = MENU.OPTIONS
                        self.stop()

                    elif buttom.name == "EXIT":
                        self.state = STATE.EXIT
                        self.stop()

