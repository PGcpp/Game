import pygame
from pygame.locals import *
from Enum import *
import sys

try:
        import IntroScene
        import DefenseScene
        import MenuScene
        import SettingsScene
except ImportError:
        print "\nUnable to import library class\n"
        sys.exit(2)

class Game():

        screenSize = (800, 600)
        bufferMode = DOUBLEBUF
        screen = None
        endOfGame = False

        menuScene = None
        settingsScene = None
        defenseScene = None

        menuSound = None
        
        def __init__(self):
                pygame.init()
                pygame.mixer.init()
                
                icon = pygame.image.load("resources/icon.png")
                pygame.display.set_icon(icon)
                pygame.display.set_caption("Vikings Defense")
                self.screen = pygame.display.set_mode(self.screenSize, self.bufferMode)

                #wyswietlanie intra
                #introScene = IntroScene.IntroScene(self.screen)
                #introScene.start()
                
                #while introScene.state == STATE.RUNNING:
                #        pass

                #if introScene.state == STATE.EXIT:
                #        self.Exit()

                #jesli nie wylaczylismy w trakcie intra to gra idzie normalnie:
                while True:

                        self.menuSound = pygame.mixer.Sound("resources/menu.wav")
                        self.menuSound.play(-1)
                        
                        self.menuScene = MenuScene.MenuScene(self.screen)
                        self.settingsScene = SettingsScene.SettingsScene(self.screen)
                        self.settingsScene.setSound(self.menuSound)
                        self.defenseScene = DefenseScene.DefenseScene(self.screen)

                        self.menuScene.start()
                        while self.menuScene.state == STATE.RUNNING:
                                pass
      
                        if self.menuScene.state == MENU.PLAY:
                                self.menuSound.stop()
                                self.defenseScene.start()

                                while self.defenseScene.state == STATE.RUNNING:
                                        pass

                                if self.defenseScene.state == STATE.EXIT:
                                        self.Exit()
                                        break

                                elif self.defenseScene.state == STATE.STOPPED:
                                        continue
                                        
                        elif self.menuScene.state == MENU.OPTIONS:
                                self.settingsScene.start()

                                while self.settingsScene.state == STATE.RUNNING:
                                        pass

                                if self.settingsScene.state == STATE.EXIT:
                                        self.menuSound.stop()
                                        self.Exit()
                                        break

                                elif self.settingsScene.state == STATE.STOPPED:
                                        continue
                                        
                        elif self.menuScene.state == STATE.EXIT:
                                self.Exit()
                                break
                        
        def Exit(self):                
                try:
                    pygame.quit()
                    sys.exit()
                except SystemExit:
                    print 'Vikings Defense has stopped correctly.'


if __name__ == "__main__":
        Game()
