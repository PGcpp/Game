import pygame
import sys, time
from Enum import *
from pygame.locals import *

class Scene():

    isActive = False
    screen = None
    state = STATE.STOPPED
    eventQueue = []

    def __init__(self, screen):
        self.screen=screen

    def start(self):
        self.isActive = True
        self.state = STATE.RUNNING
        self.sceneLoop()

    def stop(self):
        self.isActive = False

    def sceneLoop(self):
        
        self.prepare()

        while(self.isActive):
            self.step()
            self.eventQueue = pygame.event.get()
            self.handleExit()

        self.dispose()

    def prepare(self):
        pass

    def step(self):
        pass

    def dispose(self):
        pass

    def onExit(self):
        pass

    def handleExit(self):
        for event in self.eventQueue:
            if event.type == pygame.QUIT:
                
                self.onExit()
                self.stop()
                self.state = STATE.EXIT
