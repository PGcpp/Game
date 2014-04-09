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

                #w zasadzie wszystko ponizej bedzie w jednej zajebiscie wielkiej glownej petli gry

                menuScene = MenuScene.MenuScene(self.screen)
                defenseScene = DefenseScene.DefenseScene(self.screen)

                menuScene.start()
                while menuScene.state == STATE.RUNNING:
                        pass
                
                if menuScene.state == MENU.PLAY:
                        defenseScene.start()
                        #i tu znow bedzie jakis while na tym defenseScene
                        #i sprawdzanie state'a itp -> bo np chcemy wrocic do menu
                        #albo zamknac gre :)
                        #btw powrot do menu bd wymagal pomyslunku :)
                        
                elif menuScene.state == MENU.OPTIONS:
                        print "tu beda opcje ale jeszcze nie ma wiec exit"
                        self.Exit()
                        #tu beda cuda i same piekne rzeczy
                        
                elif menuScene.state == STATE.EXIT:
                        self.Exit()
                        #a tu juz nic nie bedzie bo jest wszystko

        def Exit(self):                
                try:
                    pygame.quit()
                    sys.exit()
                except SystemExit:
                    print 'Vikings Defense has stopped correctly.'


if __name__ == "__main__":
        Game()
