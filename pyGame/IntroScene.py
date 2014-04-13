import pygame
from pygame.locals import *
from Enum import *

import Settings
import Scene
import time
import math
from sys import exit

class IntroScene(Scene.Scene):

    screen = None
    state = 0
    introImage = None
    fadeLevel = 0
    fadeIn = True
    
    def IntroScene(screen):
        self.screen = screen

    def prepare(self):
        self.screen.fill((0,0,0));

        self.introImage = pygame.image.load('resources/intro.png')
        self.introImage = self.introImage.convert()

        self.introImage.set_alpha(0)

        introSound = pygame.mixer.Sound("resources/intro.wav")
        introSound.set_volume( Settings.getMusicLevel() )
        introSound.play()

    def step(self):
        
        if self.fadeIn == True:

            self.fadeLevel += 5
            
            if self.fadeLevel == 255:
                time.sleep(1)
                self.fadeIn = False
        else:

            self.fadeLevel -= 25

            if self.fadeLevel == 5:
                self.state = STATE.STOPPED
                self.stop()

        time.sleep(0.05)

        self.screen.fill((0,0,0));
        self.introImage.set_alpha( self.fadeLevel )
        self.screen.blit(self.introImage, (200, 100))
        pygame.display.flip()
 
        

