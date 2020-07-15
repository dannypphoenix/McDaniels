import pygame

class InputManager:
    def __init__(self,GameManager):
        self.GameManager = GameManager

        self.keymap = {
            pygame.K_ESCAPE:self.pause,
            pygame.K_w:self.playerbuttons,
            pygame.K_s:self.playerbuttons,
            pygame.K_a:self.playerbuttons,
            pygame.K_d:self.playerbuttons,
            pygame.K_SPACE:self.playerbuttons,
            pygame.K_LSHIFT:self.playerbuttons,
            pygame.K_UP:self.playerbuttons,
            pygame.K_DOWN:self.playerbuttons,
            pygame.K_LEFT:self.playerbuttons,
            pygame.K_RIGHT:self.playerbuttons,
            pygame.MOUSEBUTTONDOWN:self.playerbuttons,
            pygame.K_l:self.slowtime,
            pygame.K_k:self.speedtime,
            pygame.K_p:self.print,
            
            }


    def initnewlevel(self):
        self.moveindex = 0
        self.total_frame_count = 0

        
    def lateinit(self,tomove):
        # global
        self.buttonlog = []

        self.tomove = tomove

    def update(self):
        # EVENTS
        for e in pygame.event.get():
            
            if e.type == pygame.QUIT:
                #print(self.buttonlog)
                pygame.quit()
                raise SystemExit("QUIT")

            if e.type == pygame.KEYDOWN:
                if e.key in self.keymap:
                    self.keymap[e.key](e.key,True)
            elif e.type == pygame.KEYUP:
                if e.key in self.keymap:
                    self.keymap[e.key](e.key,False)




            if e.type == pygame.MOUSEBUTTONDOWN:
                self.keymap[pygame.MOUSEBUTTONDOWN](
                    pygame.MOUSEBUTTONDOWN,
                    pygame.mouse.get_pos()
                    )



        ## AUTO MOVEMENT
        if self.moveindex < len(self.tomove):
            m=self.tomove[self.moveindex]
            while self.total_frame_count >= m[0]:
                self.moveindex += 1
                self.playerbuttons(m[1],m[2])
                if self.moveindex < len(self.tomove):
                    m=self.tomove[self.moveindex]
                else:
                    break

        if not self.GameManager.paused:
            self.total_frame_count += 1


    def playerbuttons(self,key,value):
        if self.GameManager.paused: return
        self.GameManager.LogicManager.player.updatebutton(key,value)
        self.buttonlog.append((self.total_frame_count,key,value))

    def pause(self,key,value):
        if value == 1:
            if self.GameManager.paused:
                self.GameManager.paused = False
                pygame.mixer.music.unpause()
            else:
                self.GameManager.paused = True
                pygame.mixer.music.pause()
        print(self.total_frame_count)

    def print(self,key,value):
##        return
        if value:
            print('xvel:',self.GameManager.LogicManager.player.xvel,'yvel:',
                  self.GameManager.LogicManager.player.yvel)
            print('x:',self.GameManager.LogicManager.player.rect.left,
                  'y:',self.GameManager.LogicManager.player.rect.top)
            print('number of entities:',
                  len(self.GameManager.LogicManager.entities))
            print(self.GameManager.GraphicsManager.obsfpsconst,
                  self.GameManager.GraphicsManager.observedfps)
    
    def slowtime(self,key,value):
##        return
        if value:
            self.GameManager.GraphicsManager.fps = 100
            self.GameManager.LogicManager.player.Time_Scale = 1
            #self.GameManager.GraphicsManager.fps -= 5
        
    def speedtime(self,key,value):
##        return
        if value:
           self.GameManager.GraphicsManager.fps = 100
           self.GameManager.LogicManager.player.Time_Scale = .5        
        

