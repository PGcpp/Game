import pygame
from pygame.locals import *
from Button import *
from Enum import *
import time
import Scene
import DefenseScene
from sys import exit

class MenuScene(Scene.Scene):

    screen = None
    buttons = [None, None, None]
    state = 0
    menuSound = None

    def MenuScene(screen):
        self.screen = screen
        

    def prepare(self):
        
        self.drawBackground()

        self.buttons[0] = Button(800, 160, "NEW_GAME")
        self.buttons[1] = Button(800, 260, "OPTIONS")
        self.buttons[2] = Button(800, 360, "EXIT")

        for button in self.buttons:
            button.displayImage(self.screen)

    def step(self):
        for event in self.eventQueue:
            self.checkButton(event)

    def drawBackground(self):
        self.screen.fill((0,0,0,0))
        image = pygame.image.load("resources/menuBackground.png")
        menuLabel = pygame.image.load("resources/mainMenuMenuLabel.png")
        self.screen.blit(image, (0, 0))
        self.screen.blit(menuLabel, (800, 30))
        pygame.display.flip()

    def dispose(self):
        for button in self.buttons:
            button.dispose()
        self.buttons = [None]

    def checkButton(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                x, y = event.pos
                if button.isHit(x, y):
                    print button.name
                    if button.name == "NEW_GAME":
                        self.stop()
                        self.state = MENU.PLAY

                    elif button.name == "OPTIONS":
                        self.state = MENU.OPTIONS
                        self.stop()

                    elif button.name == "EXIT":
                        self.state = STATE.EXIT
                        self.stop()
