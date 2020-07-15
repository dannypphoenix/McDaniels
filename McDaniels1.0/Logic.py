import pygame, time
from Entities import *


class LogicManager:
    
    def __init__(self,GameManager):
        self.t = 0
        self.GameManager = GameManager

        # lists
        self.entities = pygame.sprite.Group()
        self.mustdestroy = pygame.sprite.Group()

        # constants
        self.GRIDSIZE = 32

    def initnewlevel(self):
        # lists
        self.entities.empty()
        self.mustdestroy.empty()

        # global
        self.globallaser = GlobalLaser()

        # game
        Time_Scale = 1
        self.total_frame_count = 0

        # player
        self.player = Player(32, 32, self.GameManager)

    def lateinit(self,current_laser):
        

        self.current_laser = current_laser

        self.mustdestroythresh = len(self.mustdestroy)
        if self.mustdestroythresh==0: self.mustdestroythresh = -1

    def update(self):
        t1 = time.time()
        ## SCREEN UPDATING

        self.entities.remove(filter(lambda e: e.destroyed, self.entities))
        self.entities.update()

        
        ## COLLISION
        groups = {}

        GRIDSIZE=self.GRIDSIZE
        
        for e in self.entities:
            l=e.rect.left//GRIDSIZE
            t=e.rect.top//GRIDSIZE
            r=(e.rect.right-1)//GRIDSIZE
            b=(e.rect.bottom-1)//GRIDSIZE
            names = [str(x)+' '+str(y) \
                      for x in range(l,r+1) for y in range(t,b+1)]
            for name in names:
                if name in groups:
                    groups[name].append(e)
                else:
                    groups[name]=[e]
            e.groups = names


        for e1 in self.entities:
            if isinstance(e1, Platform): continue
            for name in e1.groups:
                for e2 in groups[name]:
                    if e1==e2:continue
                    if pygame.sprite.collide_rect(e1,e2):
                        e1.collide(e2)
        #print(len(groups))
        if self.player.done:
            self.GameManager.done = True
            
        self.mustdestroy.remove(filter(lambda e: e.destroyed, self.entities))
        if len(self.mustdestroy)-self.mustdestroythresh <= 0:
            self.GameManager.done = True

        


        self.total_frame_count += 1
        self.t += time.time() - t1

class GlobalLaser(object):
    def __init__(self):
        self.ReflectChance=1
        self.friction = 1.0
        self.gravity = 1
