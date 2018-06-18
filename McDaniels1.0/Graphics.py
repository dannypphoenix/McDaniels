import pygame
from Entities import *

class Camera(object):
    def __init__(self, width, height,GraphicsManager):
        self.state = pygame.Rect(0, 0, width, height)
        self.borderlimit = False
        self.GraphicsManager = GraphicsManager
        self.width = width
        self.height = height


    def camera_func(self, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = self.state
        l, t, _, _ = -l+self.GraphicsManager.HALF_WIDTH, \
                     -t+self.GraphicsManager.HALF_HEIGHT, w, h

        l = min(0, l)
        # stop scrolling at the left edge
        l = max(-(self.width-self.GraphicsManager.WIN_WIDTH), l)
        # stop scrolling at the right edge
        t = max(-(self.height-self.GraphicsManager.WIN_HEIGHT), t)
        # stop scrolling at the bottom
        t = min(0, t)
        # stop scrolling at the top
        return pygame.Rect(l, t, w, h)

    def apply(self, target):
        if self.borderlimit and isinstance(target, Character):
            if not self.onscreen(target):
                target.destroyed = True
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(target.rect)

    def onscreen(self, target):
        sl = self.state.left
        st = self.state.top
        sw = self.state.width
        sh = self.state.height
        self.rect = pygame.Rect(-sl, -st, sw, sh)
        if pygame.sprite.collide_rect(self, target):
            return True
        else:
            return False

        


class GraphicsManager:
    
    def __init__(self,GameManager):
        self.GameManager = GameManager
        # setup variables
        self.WIN_WIDTH = 800
        self.WIN_HEIGHT = 640
        self.HALF_WIDTH = int(self.WIN_WIDTH / 2)
        self.HALF_HEIGHT = int(self.WIN_HEIGHT / 2)

        self.DISPLAY = (self.WIN_WIDTH, self.WIN_HEIGHT)
        self.DEPTH = 32 
        self.FLAGS = 0

        self.screen = pygame.display.set_mode(
            self.DISPLAY, self.FLAGS, self.DEPTH)
        pygame.display.set_caption("Mcdaniels")


        self.bg = pygame.Surface((32,32))
        self.bg.convert()
        self.bg.fill((0,0,0,10))

        
        self.fps = 60
        self.observedfps = [0,0,0,0,0,0,0,0,0,0]
        self.fpscounter = 0
        self.obsfpsconst = 0
        self.fpschecktimermax = 100
        self.fpschecktimer = 0

        

        
        self.draw_entities = pygame.sprite.Group()

    def initnewlevel(self):
        pass

    def lateinit(self,w,h):
        # camera
        self.camera=Camera(w,h,self)
        self.focus = self.GameManager.LogicManager.player

    def update(self):

##        self.fpschecktimer -= 1
##        if self.fpschecktimer <= 0:
##            self.fpschecktimer = self.fpschecktimermax
##            self.observedfps[self.fpscounter]=self.GameManager.timer.get_fps()
##            self.fpscounter+=1;self.fpscounter%=len(self.observedfps)
##            self.obsfpsconst = sum(self.observedfps)/len(self.observedfps)

        ## DRAW BACKGROUND
        for y in range(32):
            for x in range(32):
                self.screen.blit(self.bg, (x * 32, y * 32))
        
        self.draw_entities.empty()
        self.draw_entities.add(map(lambda e: \
                              ScreenEntity(e.image, self.camera.apply(e)),
                            self.GameManager.LogicManager.entities))
        self.draw_entities.draw(self.screen)


        self.camera.update(self.focus)

        pygame.display.flip()
