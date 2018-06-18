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
                print(self.buttonlog)
                pygame.quit()
                raise SystemExit("QUIT")

            if e.type == pygame.KEYDOWN:
                if e.key in self.keymap:
                    self.keymap[e.key](e.key,True)
            elif e.type == pygame.KEYUP:
                if e.key in self.keymap:
                    self.keymap[e.key](e.key,False)




##            if e.type == pygame.MOUSEBUTTONDOWN:
##                Mx, My = pygame.mouse.get_pos()
##                Mx -= camera.state.left
##                My -= camera.state.top
##                Px = player.rect.left + 2
##                Py = player.rect.top  + 2
##                deltaX = Mx - Px
##                deltaY = My - Py
##                
##                denom = (deltaX**2 + deltaY**2)**.5
##                deltaX /= denom
####                deltaY /= denom
##                time = denom/16#laser.speed
##                yvel = (deltaY - 1/2*self.globallaser.gravity * \
##                        time**2)/time
##
##                direction = (deltaX, yvel/16)#laser.speed)
##
##                laser = current_laser(Px,Py,
##                                      self, 
##                                      direction)
##                laser.shooter = player



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
##                if m[1]=='up':
##                    self.playerbuttons(pygame.K_w,m[2])
##                if m[1]=='down':
##                    self.playerbuttons(pygame.K_s,m[2])
##                if m[1]=='left':
##                    self.playerbuttons(pygame.K_a,m[2])
##                if m[1]=='right':
##                    self.playerbuttons(pygame.K_d,m[2])
##                if m[1]=='running':
##                    self.playerbuttons(pygame.K_SPACE,m[2])
##                if m[1]=='sneaking':
##                    self.playerbuttons(pygame.K_LSHIFT,m[2])

        if not self.GameManager.paused:
            self.total_frame_count += 1


    def playerbuttons(self,key,value):
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
    
    def slowtime(self,key,value):
##        return
        if value:
            self.GameManager.GraphicsManager.fps = 0
            #self.GameManager.GraphicsManager.fps -= 5
        
    def speedtime(self,key,value):
##        return
        if value:
           self.GameManager.GraphicsManager.fps += 5

