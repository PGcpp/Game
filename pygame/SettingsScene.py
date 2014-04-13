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
    buttons = [None, None, None, None, None, None, None, None, None]
    state = 0
    menuSound = None
    settings = None

    musicLevel = 0
    effectsLevel = 0
    difficulty = 1

    def SettingsScene(screen):
        self.screen = screen

    def setSound(self, menuSound):
        self.menuSound = menuSound
        

    def prepare(self):
        
        self.drawBackground()
        self.buttons[0] = Button(525, 220, "MUSICMINUS")
        self.buttons[1] = Button(725, 220, "MUSICPLUS")
        self.buttons[2] = Button(525, 320, "FXMINUS")
        self.buttons[3] = Button(725, 320, "FXPLUS")
        self.buttons[4] = Button(487, 420, "DIFFICULTYEASY")
        self.buttons[5] = Button(580, 420, "DIFFICULTYMEDIUM")
        self.buttons[6] = Button(697, 420, "DIFFICULTYHARD")
        self.buttons[7] = Button(475, 525, "EXITSETTINGS")
        self.buttons[8] = Button(625,525, "SAVESETTINGS")

        for button in self.buttons:
            button.displayImage(self.screen)

        self.settings = ConfigParser.ConfigParser()
        self.settings.readfp(open('settings.cfg'))
        self.musicLevel = int(self.settings.get("MUSIC", "LEVEL"))
        self.effectsLevel = int(self.settings.get("EFFECTS", "LEVEL"))
        self.difficulty = int(self.settings.get("DIFFICULTY", "LEVEL"))

        if self.musicLevel < 0:
            self.musicLevel = 0
        elif self.musicLevel > 5:
            self.musicLevel = 5
        elif self.effectsLevel < 0:
            self.effectsLevel = 0
        elif self.effectsLevel > 5:
            self.effectsLevel = 5
        elif self.difficulty < 1:
            self.difficulty = 1
        elif self.difficulty > 3:
            self.difficulty = 3

        self.PrintSettings()

    def PrintSettings(self):
        musicLevelImage = pygame.image.load("resources/value"+str(self.musicLevel)+".png")
        effectsLevelImage = pygame.image.load("resources/value"+str(self.effectsLevel)+".png")
        difficultyImage = pygame.image.load("resources/difficulty"+str(self.difficulty)+".png")
        self.screen.blit(musicLevelImage, (562, 195))
        self.screen.blit(effectsLevelImage, (562, 295))
        self.screen.blit(difficultyImage, (480, 420))
        pygame.display.flip()
        
        self.menuSound.set_volume( self.musicLevel * 0.2 )

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

    def checkButton(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                x, y = event.pos
                if button.isHit(x, y):
                    
                    print button.name

                    if button.name == "MUSICMINUS":
                        if self.musicLevel <= 0:
                            self.musicLevel = 0
                        else:
                            self.musicLevel = self.musicLevel - 1
                        self.PrintSettings()

                    if button.name == "MUSICPLUS":
                        if self.musicLevel >= 5:
                            self.musicLevel = 5
                        else:
                            self.musicLevel = self.musicLevel + 1
                        self.PrintSettings()

                    if button.name == "FXMINUS":
                        if self.effectsLevel <= 0:
                            self.effectsLevel = 0
                        else :
                            self.effectsLevel = self.effectsLevel - 1
                        self.PrintSettings()

                    if button.name == "FXPLUS":
                        if self.effectsLevel >= 5:
                            self.effectsLevel = 5
                        else :
                            self.effectsLevel = self.effectsLevel + 1
                        self.PrintSettings()

                    if button.name == "DIFFICULTYEASY":
                        self.difficulty = 1
                        self.PrintSettings()

                    if button.name == "DIFFICULTYMEDIUM":
                        self.difficulty = 2
                        self.PrintSettings()

                    if button.name == "DIFFICULTYHARD":
                        self.difficulty = 3
                        self.PrintSettings()
                        
                    if button.name == "EXITSETTINGS":
                        self.state = STATE.STOPPED
                        self.stop()

                    if button.name == "SAVESETTINGS":
                        self.saveSettings()
                    

    def saveSettings(self):
        self.settings.set("MUSIC", "LEVEL", self.musicLevel)
        self.settings.set("EFFECTS", "LEVEL", self.effectsLevel)
        self.settings.set("DIFFICULTY", "LEVEL", self.difficulty)
        
        settingsFile = open('settings.cfg' , 'w')
        self.settings.write(settingsFile)
        settingsFile.close()

    def onExit(self):
        self.menuSound.stop()
        

