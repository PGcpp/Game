import pygame
import sys, time
from Enum import *
from pygame.locals import *

class Scene(object):

    isActive = False
    screen = None
    state = STATE.STOPPED
    eventQueue = []

    def __init__(self, screen):
        self.screen = screen

    def start(self):
        self.isActive = True
        self.state = STATE.RUNNING
        self.sceneLoop()

    def stop(self):
        if self.state == STATE.RUNNING:
            self.state = STATE.STOPPED
            
        self.isActive = False

    def sceneLoop(self):
        
        self.prepare()

        while(self.isActive):
            self.eventQueue = pygame.event.get()
            self.step()
            self.handleExit()

        self.dispose()

    def prepare(self):
        pass

    def step(self):
        pass

    def dispose(self):
        pass

    def onExit(self):
        self.isActive = False
        self.state = STATE.EXIT

    def handleExit(self):
        for event in self.eventQueue:
            if event.type == pygame.QUIT:
                self.onExit()
                
                try:
                    pygame.quit()
                    sys.exit()
                    
                except SystemExit:
                    print 'Vikings Defense scene has stopped correctly.'
