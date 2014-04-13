import pygame
from pygame.locals import *
from Enum import *
import sys

try:
        import IntroScene
        import DefenseScene
        import MenuScene
        import SettingsScene
        import Settings
except ImportError:
        print "\nUnable to import library class\n"
        sys.exit(2)

class Game():

        SCREEN_SIZE = (800, 600)
        BUFFER_MODE = DOUBLEBUF
        screen = None

        menuScene = None
        settingsScene = None
        defenseScene = None

        menuSound = None
        startMenuSound = True
        
        def __init__(self):
                pygame.init()
                pygame.mixer.init()
                
                icon = pygame.image.load("resources/icon.png")
                pygame.display.set_icon(icon)
                pygame.display.set_caption("Vikings Defense")
                self.screen = pygame.display.set_mode(self.SCREEN_SIZE, self.BUFFER_MODE)

                self.menuSound = pygame.mixer.Sound("resources/menu.wav")
                
                introScene = IntroScene.IntroScene(self.screen)
                introScene.start()
                
                while introScene.state == STATE.RUNNING:
                        pass

                if introScene.state == STATE.EXIT:
                        self.Exit()

                while True:

                        self.menuSound.set_volume( Settings.getMusicLevel() )
                        if self.startMenuSound:
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
                                        self.startMenuSound = True
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
                                        self.menuSound.set_volume( Settings.getMusicLevel() )
                                        self.startMenuSound = False
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
