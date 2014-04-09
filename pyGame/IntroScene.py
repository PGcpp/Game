import pygame
from pygame.locals import *
from Enum import *

import Scene
import time
import math
from sys import exit

class IntroScene(Scene.Scene):

    screen = None
    state = 0
    introImage = None
    a = 0
    fadeIn = True
    
    def IntroScene(screen):
        self.screen = screen

    def prepare(self):
        self.screen.fill((0,0,0));

        self.introImage = pygame.image.load('resources/intro.png')
        self.introImage = self.introImage.convert()

        self.introImage.set_alpha(0)

        introSound = pygame.mixer.Sound("resources/intro.wav")
        introSound.play()

    def step(self):
        
        if self.fadeIn == True:

            self.a += 5
            
            if self.a == 255:
                time.sleep(1)
                self.fadeIn = False
        else:

            self.a -= 25

            if self.a == 5:
                self.state = STATE.STOPPED
                self.stop()

        time.sleep(0.05)

        self.screen.fill((0,0,0));
        self.introImage.set_alpha( self.a )
        self.screen.blit(self.introImage, (200, 100))
        pygame.display.flip()
 
        

