import pygame
import sys, time
from Enum import *
from pygame.locals import *

class Scene():

    is_active = False
    screen = None
    state = STATE.STOPPED

    #uwaga to dodane po to zeby mozna bylo przegladac eventy
    #w kilku miejscach (funkcja event.get() w handleExit
    #'blokowala' kolejne wywolania tej funkcji
    #teraz eventy przegladamy w tej liscie a nie w tej z get() !!!
    # -> patrz MenuScene
    eventQueue = []

    def __init__(self, screen):
        self.screen=screen

    def start(self):
        self.is_active = True
        self.state = STATE.RUNNING
        self.sceneLoop()

    def stop(self):
        if self.state == STATE.RUNNING:
            self.state = STATE.STOPPED
            
        self.is_active = False

    def sceneLoop(self):
        
        self.prepare()

        while(self.is_active):
            self.eventQueue = pygame.event.get()
            self.step()
            self.handleExit()

        self.dispose()

    def prepare(self):
        pass
        #tu przygotowujemy sobie wszystko - to mozna zrobic tez w konstruktorze ale moze akurat taka logika okaze sie sensowna :)

    def step(self):
        pass
        #tu wrzucamy wszystkie akcje

    def dispose(self):
        pass
        # a tu sprzatamy

    def onExit(self):
        pass
        #tu mozemy np zawrzec pytanie czy zapisac

    #to jest po to, zeby w kazdej scenie krzyzyk dzialal
    def handleExit(self):
        for event in self.eventQueue:
            if event.type == pygame.QUIT:
                
                self.onExit()
                self.stop()
                
                try:
                    pygame.quit()
                    sys.exit()
                    
                except SystemExit:
                    print 'Vikings Defense has stopped correctly.'
