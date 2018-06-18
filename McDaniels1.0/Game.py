import pygame, os
from Entities import *
from Graphics import GraphicsManager
from Input import InputManager
from Logic import LogicManager
from Image import ImageLoader



class GameManager:
    def __init__(self):
        self.GraphicsManager = GraphicsManager(self)
        self.InputManager = InputManager(self)
        self.LogicManager = LogicManager(self)

        self.imageLoader = ImageLoader()
        self.timer = pygame.time.Clock()
    def initnewlevel(self):
        self.GraphicsManager.initnewlevel()
        self.InputManager.initnewlevel()
        self.LogicManager.initnewlevel()
        self.paused = False
        self.done = False

    def lateinit(self,tomove,w,h):
        self.GraphicsManager.lateinit(w,h)
        self.InputManager.lateinit(tomove)
        self.LogicManager.lateinit(None)

    def mainLoop(self):
        while 1:
            self.timer.tick(self.GraphicsManager.fps)
            self.GraphicsManager.update()
            self.InputManager.update()
            if not self.paused:
                self.LogicManager.update()

            #print(self.GraphicsManager.obsfpsconst)

            if self.LogicManager.player.destroyed:
                return False
            elif self.done:
                return True
