import pygame
from pygame.locals import *
from Enum import *
import sys

try:
        import DefenseScene
        import MenuScene
except ImportError:
        print "\nUnable to import library class\n"
        sys.exit(2)

class Game():

    screenSize = (800, 600)
    bufferMode = DOUBLEBUF
    screen = None
    endOfGame = False
    
    def __init__(self):
        pygame.init()
                
        icon = pygame.image.load("resources/icon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Vikings Defense")
        self.screen = pygame.display.set_mode(self.screenSize, self.bufferMode)

        menuScene = MenuScene.MenuScene(self.screen)
        defenseScene = DefenseScene.DefenseScene(self.screen)
        menuScene.start()

        while not self.endOfGame:
                        
            if menuScene.state == MENU.PLAY:
                defenseScene.start()
                menuScene.start()
                     
            elif menuScene.state == MENU.OPTIONS:
                pass
                                    
            elif menuScene.state == STATE.EXIT:
                self.Exit()

    def Exit(self):                
        try:
            self.endOfGame = True
            self.screen = None
            pygame.quit()
            sys.exit()
        except SystemExit:
            print 'Vikings Defense game has stopped correctly.'


if __name__ == "__main__":
    Game()
