import pygame
from Entities import *


class LogicManager:
    
    def __init__(self,GameManager):
        self.GameManager = GameManager

        # lists
        self.entities = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.live_enemies = pygame.sprite.Group()
        self.destroyed_enemies = pygame.sprite.Group()
        self.drones = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()

        # constants
        self.GRIDSIZE = 32

    def initnewlevel(self):
        # lists
        self.entities.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.live_enemies.empty()
        self.destroyed_enemies.empty()
        self.drones.empty()
        self.lasers.empty()
        self.mustdestroy = []

        # global
        self.globallaser = GlobalLaser()

        # game
        Time_Scale = 1
        self.total_frame_count = 0

        # player
        self.player = Player(32, 32, self.GameManager)

    def lateinit(self,current_laser):
        

        self.current_laser = current_laser

        if len(self.mustdestroy)==0:
            mustdestroy = [0]

    def update(self):
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
                for name in e1.groups:
                    for e2 in groups[name]:
                        if e1==e2:continue
                        if pygame.sprite.collide_rect(e1,e2):
                            e1.collide(e2)
                            #e2.collide(e1)

        if self.player.done:
            self.GameManager.done = True
            

##        ## UPDATING DIFFERENT ENTITIES
##            
##        ### LASERS
##        self.lasers.remove(filter(lambda e: e.destroyed, self.lasers))
##        self.lasers.update()
##        
##
##        ### ENEMIES
##        
##
##        # reset live/destroyed enemies
##        self.live_enemies.empty()
##        self.live_enemies.add(filter(lambda e: not e.destroyed, self.enemies))
##        self.destroyed_enemies.empty()
##        self.destroyed_enemies.add(filter(lambda e: e.destroyed, self.enemies))
##
##        # update
##        self.live_enemies.update()
##            
##        
##        ### DRONES
##        self.drones.remove(filter(lambda e: e.destroyed, self.drones))
##        #self.drones.update()
##
##        ### PLATFORMS
##        self.platforms.remove(filter(lambda e: e.destroyed, self.platforms))
##        #self.platforms.update()

        current_must = 0
        while current_must < len(self.mustdestroy):
            p = self.mustdestroy[current_must]
            if p==0: break
            if p.destroyed:
                self.mustdestroy.remove(p)
            else:
                current_must += 1


        self.total_frame_count += 1

class GlobalLaser(object):
    def __init__(self):
        self.ReflectChance=1
        self.friction = 1.0
        self.gravity = 1
