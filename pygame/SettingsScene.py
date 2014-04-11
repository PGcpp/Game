import pygame
import ConfigParser
from pygame.locals import *
from Button import *
from Enum import *
import time
import Scene
import DefenseScene
from sys import exit

class SettingsScene(Scene.Scene):

    screen = None
    buttons = [None, None, None, None]
    state = 0
    menuSound = None
    settings = None

    def SettingsScene(screen):
        self.screen = screen

    #nie jest to zbyt ladne ale to wyjatkowa sytuacja - nigdzie indziej w grze nie bedziemy 'podtrzymywac' dzwieku z poprzedniej
    #sceny wiec mozna sobie pozwolic na taki workarround :) //patrz nizej onExit()
    def setSound(self, menuSound):
        self.menuSound = menuSound
        

    def prepare(self):
        
        self.drawBackground()

        self.buttons[0] = Button(525, 220, "MUSICMINUS")
        self.buttons[1] = Button(725, 220, "MUSICPLUS")
        self.buttons[2] = Button(525, 300, "FXMINUS")
        self.buttons[3] = Button(725, 300, "FXPLUS")

        for button in self.buttons:
            button.displayImage(self.screen)

        self.settings = ConfigParser.ConfigParser()

    def readAndPrintSettings(self):
        #ta funkcja domyslnie bedzie podmieniala sprite'y
        #przy opcjach, ktore beda reprezentowaly skale
        #i aktualna wartosc [np 5 toporow - taki poziom glosnosci
        #ile z nich zakolorowanych na zielono]
        self.settings.read(['settings.cfg'])
        print "------------------------------"
        print self.settings.get("MUSIC", "PLAY")
        print self.settings.get("MUSIC", "LEVEL")
        print self.settings.get("EFFECTS", "PLAY")
        print self.settings.get("EFFECTS", "LEVEL")
        print "------------------------------"

    def step(self):
        for event in self.eventQueue:
            self.checkButton(event)

    def drawBackground(self):
        image = pygame.image.load("resources/settingsBackground.png")
        self.screen.blit(image, (0, 0))
        pygame.display.flip()

    def dispose(self):
        for button in self.buttons:
            button.dispose()
        self.buttons = [None]
        self.menuSound.stop()

    def checkButton(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                x, y = event.pos
                if button.isHit(x, y):
                    
                    print button.name

                    section = None
                    value = None

                    self.settings.readfp( open('settings.cfg', 'r') )
                    musicLevel = int(self.settings.get("MUSIC", "LEVEL"))
                    effectsLevel = int(self.settings.get("EFFECTS", "LEVEL"))

                    if button.name == "MUSICMINUS":
                        section = "MUSIC"
                        value = musicLevel - 1

                    if button.name == "MUSICPLUS":
                        section = "MUSIC"
                        value = musicLevel + 1

                    if button.name == "FXMINUS":
                        section = "EFFECTS"
                        value = effectsLevel - 1

                    if button.name == "FXPLUS":
                        section = "EFFECTS"
                        value = effectsLevel + 1
                        
                    self.settings.set(section, "LEVEL", value)
                    
                    with open('settings.cfg', 'wb') as configfile:
                        self.settings.write(configfile)

                    self.readAndPrintSettings()

    #zeby sie nie popsulo przy wylaczaniu krzyzykiem
    def onExit(self):
        self.menuSound.stop()
        

