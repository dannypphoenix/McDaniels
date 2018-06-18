import pygame, random
#t=0

class Entity(pygame.sprite.Sprite):
    def __init__(self,game,image,rect):
        pygame.sprite.Sprite.__init__(self)
        self.game=game
        self.game.LogicManager.entities.add(self)
        self.Time_Scale=1
        if image in game.imageLoader.imagedict:
            self.frames = game.imageLoader.imagedict[image]
        else:
            self.frames = {'idle0':game.imageLoader.missingasset}
        self.animationbase = 'idle'
        self.image=self.frames[self.animationbase+'0']
        self.internalFrameTimer = 0
        self.rect = rect
    def updateimg(self):
        newimg=self.animationbase+str(int(self.internalFrameTimer))
        if newimg in self.frames:
            self.image = self.frames[newimg]
        else:
            self.internalFrameTimer = 0
            self.image = self.frames[self.animationbase+'0']
        self.internalFrameTimer += 1/self.Time_Scale
        
    
    def collide(self,o):
        return

class ScreenEntity(pygame.sprite.Sprite):
    def __init__(self,image,rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = rect

class Character(Entity):
    def __init__(self, x, y, width, height, img, game):
        Entity.__init__(self, game,img,pygame.Rect(x, y, width, height))
        self.xvel = 0
        self.yvel = 0
        self.moveX = 0
        self.moveY = 0
        self.distancelimitx = self.distancelimity = 32*10**10
        self.onGround = False
        self.maxGroundTime = 1
        self.groundTime = self.maxGroundTime
##        self.image = pygame.image.load(img)
        ## DEBUG TEST EDIT LATER FIX
        #self.image.fill([random.randint(0,255) for i in range(3)])
        self.destroyed = False
        self.health = 100
        self.maxhealth = 100
        #self.healthbar = HealthBar(self)
        self.power = 1
        self.done = False
        self.speed = 4
        self.friction = .5
        self.gravity = .3
        self.regen = .1
        self.extraYvel = 0
        self.extraMoveY = 0
        self.extraXvel = 0
        self.extraMoveX = 0

    def update(self):
        Entity.updateimg(self)

        self.prevRect = self.rect.copy() 
        
        #platforms = self.game.LogicManager.platforms
    
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += self.gravity/self.Time_Scale
            # max falling speed
            #if self.yvel > 100: self.yvel = 100
            
##            if self.rect.top >= 100000:
##                self.rect.top = -100
##                self.yvel = 0
##                ##print('teleporting')
            
##        if not(left or right):
##            self.xvel = 0
            
        if abs(self.xvel) < .001:
            self.xvel = 0.0

        if self.xvel != 0.: # only slow down if moving
            self.xvel *= 1-((1-self.friction)/self.Time_Scale)
            ##print ('xvel',self.xvel)
            #self.xvel -= self.xvel*.4
            

        if self.health <= 0 or \
           abs(self.rect.left) >= self.distancelimitx or\
           abs(self.rect.top ) >= self.distancelimity:
            self.destroyed = True
            ##print('die!')


        #platforms = self.getCloseEntities(platforms)


        # remove decimals and store them
        self.xvel += self.extraXvel
        self.extraXvel = self.xvel - int(self.xvel)
        self.xvel = int(self.xvel)

        moveX = self.xvel/self.Time_Scale
        moveX += self.extraMoveX
        self.extraMoveX = moveX-int(moveX)
        moveX = int(moveX)
        
##        # do x-axis collisions
##        self.collide(self.xvel, 0, platforms)

        self.yvel += self.extraYvel
        self.extraYvel = self.yvel - int(self.yvel)
        self.yvel = int(self.yvel)

        moveY = self.yvel/self.Time_Scale
        moveY += self.extraMoveY
        self.extraMoveY = moveY-int(moveY)
        moveY = int(moveY)

        self.moveX=moveX;self.moveY=moveY


        # increment in x direction
        self.rect.left += moveX
        # increment in y direction
        self.rect.top += moveY      
        # assuming we're in the air
        if self.groundTime <= 0:
            self.onGround = False
        else:
            self.onGround = True
        self.groundTime -= 1/self.Time_Scale
        # do y-axis collisions
##        self.collide(0, self.yvel, platforms)


        if self.health < self.maxhealth and self.health != -1:
            self.health += self.regen

    def collide(self, p):
        


        if isinstance(p, Platform):
            ## figure out collision stuff
            
            rx = self.prevRect.copy()
            rx.left += self.moveX

##            if self.prevRect.colliderect(p.rect):
##                ##print('oops',self)
##                pass

            ry = self.prevRect.copy()
            ry.top  += self.moveY


            xcollide = rx.colliderect(p.rect)
            ycollide = ry.colliderect(p.rect)

            if xcollide and not ycollide:
                # x fault
                yvel = 0
                xvel = self.xvel
            elif ycollide and not xcollide:
                # y fault
                xvel = 0
                yvel = self.yvel
            elif xcollide and ycollide:
                ##print('huh',rx.left,p.rect.left,ry.top,p.rect.top)
                xvel = self.xvel
                yvel = 0#self.yvel
                # inside of p
            elif not xcollide and not ycollide:
                xdis = abs(p.rect.left-rx.left)
                ydis = abs(p.rect.top -rx.top)
                if xdis < ydis:
                    # x fault
                    yvel = 0
                    xvel = self.xvel
                elif ydis < xdis:
                    # y fault
                    xvel = 0
                    yvel = self.yvel
                else:
                    yvel = self.yvel
                    xvel = self.xvel
                    #print('huh')
            else:
                xvel = self.xvel
                yvel = self.yvel
                #print('should never get here')
                

        
            if isinstance(p, ExitBlock):
                self.done = True
                
            elif isinstance(p, BounceBlock):
                
                if yvel != 0:
                    self.yvel *= -1
                if xvel != 0:
                    self.xvel *= -1
                    
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel += 2
                elif yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.yvel -= 2
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel += 2
                    ##print('in Bounce')
                elif xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel -= 2
                    ##print('in Bounce')

                return

            elif isinstance(p, DeathBlock):
                if not self.health == -1:
                    self.destroyed = True
                    ##print('die0')

                    return

            elif isinstance(p, ZoomBlock):
                if   xvel == 0:
                    self.xvel *= p.zoominess
                if yvel == 0:
                    self.yvel *= p.zoominess
            if xvel > 0:
                self.rect.right = p.rect.left
                self.xvel = 0
                self.extraXvel = 0
                #self.extraMoveXvel = 0
                ##print("collide right")
            if xvel < 0:
                self.rect.left = p.rect.right
                self.xvel = 0
                self.extraXvel = 0
                #self.extraMoveXvel = 0
                ##print("collide left")
            if yvel > 0:
                self.rect.bottom = p.rect.top
                self.groundTime = self.maxGroundTime
                self.yvel = 0
                self.extraYvel = 0
                #self.extraMoveYvel = 0
            if yvel < 0:
                self.rect.top = p.rect.bottom
                self.yvel = 0
                self.extraYvel = 0
                #self.extraMoveYvel = 0


class Player(Character):
    def __init__(self, x, y, game):
        Character.__init__(self, x, y, 32, 32, 'player',
                           game)
        self.speed = 4
        self.jetpack = False
        self.friction = .7
        self.running_speed = 3.3#11#7.7
        self.walking_speed = 2.1#7#4.9
        self.sneaking_speed= .4#1#0.7
        self.continuousshoot = None
        self.shoottimer = 0
        self.shootrate = 5
        self.up=self.down=self.left=self.right=self.running=\
                 self.sneaking=False
        self.font = pygame.font.SysFont('monospace', 16)

    def updatebutton(self,key,value):
        if key == pygame.K_w:
            self.up = value
        elif key == pygame.K_s:
            self.down = value
        elif key == pygame.K_a:
            self.left = value
        elif key == pygame.K_d:
            self.right = value
        elif key == pygame.K_SPACE:
            self.running = value
        elif key == pygame.K_LSHIFT:
            self.sneaking = value
        elif key == pygame.K_UP:
            self.up = value
        elif key == pygame.K_DOWN:
            self.down = value
        elif key == pygame.K_LEFT:
            self.left = value
        elif key == pygame.K_RIGHT:
            self.right = value
        
    
    def update(self):
        # score stuff
        Xp=self.rect.left
        Yp=self.rect.top
        Xe=1824
        Ye=0




        
        entities = self.game.LogicManager.entities
        platforms = self.game.LogicManager.platforms

        
        if self.up:
            # only jump if on the ground
            if self.onGround and not self.jetpack:
                self.yvel -= 11/self.Time_Scale
            elif self.jetpack:
                self.yvel -= 1/self.Time_Scale
                laser = normal_laser(self.rect.left + 16,
                                     self.rect.bottom,
                                     entities,
                                     (0,1))
                laser.shooter = self
        if self.down:
            if self.jetpack:
                self.yvel += 1/self.Time_Scale
                laser = normal_laser(self.rect.left + 16,
                                     self.rect.top,
                                     entities,
                                     (0,-1))
                laser.shooter = self
        if self.running:
            self.speed = self.running_speed
            self.animationbase = 'running'
            self.internalFrameTimer = 0
        elif self.sneaking:
            self.speed = self.sneaking_speed
            self.animationbase = 'sneaking'
            self.internalFrameTimer = 0
        else:
            self.speed = self.walking_speed
            self.animationbase = 'walking'
            self.internalFrameTimer = 0

            
        if self.left:
            
            if not self.jetpack:
                self.xvel -= self.speed/self.Time_Scale
            else:
                self.xvel -= 2/self.Time_Scale
                laser = normal_laser(self.rect.right,
                                     self.rect.top + 16,
                                     self.game,
                                     (1,0))
                laser.shooter = self
        if self.right:
            if not self.jetpack:
                self.xvel += self.speed/self.Time_Scale
            else:
                self.xvel += 2/self.Time_Scale
                laser = normal_laser(self.rect.left,
                                     self.rect.top + 16,
                                     self.game,
                                     (-1,0))
                laser.shooter = self


        if self.continuousshoot != None:

            if self.shoottimer <= 0:
                self.shoottimer = self.shootrate
                
                laser = self.continuousshoot(self.rect.left+16,
                                             self.rect.top+16,self.game)
                laser.shooter = self

            elif self.shoottimer > 0:
                self.shoottimer -= 1

        Character.update(self)


        if self.health == -1:
            self.destroyed = False


class Enemy(Character):
    def __init__(self, x, y, game):
        Character.__init__(self, x, y, 32, 64, 'enemy',
                           game)
        self.game.LogicManager.enemies.add(self)
        self.spawn = (x, y)
        self.timer = 1000
        self.max_timer = 1000
        self.respawn = True
        self.target = game.LogicManager.player
        self.lasers = game.LogicManager.lasers
        
        
    def update(self):
        player = self.target
        
        if   player.rect.left > self.rect.right:
            self.xvel = self.speed

        elif player.rect.right < self.rect.left:
            self.xvel = -self.speed
        if player.rect.bottom < self.rect.top:
            if self.onGround: self.yvel -= 10



                
        shoot = random.randint(1, 20)
        if shoot == 1:
            Tx = player.rect.left + 16
            Ty = player.rect.top  + 16
            Sx = self.rect.left   + 16
            Sy = self.rect.top    + 16
            deltaX = Tx - Sx
            deltaY = Ty - Sy


            denom = (deltaX**2 + deltaY**2)**.5

            if denom == 0: denom = .1
            deltaX /= denom
            time = denom/16
            
            yvel_laser = (deltaY - \
                        1/2*self.game.LogicManager.globallaser.gravity *\
                          time**2)/time

            direction = (deltaX, yvel_laser/16)

            laser = normal_laser(Sx, Sy, self.game, direction)
            laser.shooter = self

        Character.update(self)

        if pygame.sprite.collide_rect(self, player):

            if not player.destroyed:
                if player.health != -1:
                    player.health -= self.power
                    player.health = max((player.health, 0))
                if player.health == 0: player.destroyed = True
            else:
                player.destroyed = True
##                #print('killed')


class HamburgurDrone(Character):
    def __init__(self, x, y, game,img='drone'):
        Character.__init__(self, x, y, 32, 32, img,
                           game)
        self.game.LogicManager.drones.add(self)
        self.spawn = (x, y)
        self.timer = 0
        self.max_timer = 0
        self.speed = .4
        self.friction = .9
        self.destroyed = False
        self.synchronisedShooting = False
        self.setupSynchronisedShooting = True
        self.targets = []
        self.Wifi = None
        self.cyclemax = 1
        self.cycles = 0
    def setupstuff(self, platforms):
        if self.synchronisedShooting and \
           self.setupSynchronisedShooting:
            for p in platforms:
                if isinstance(p, HamburgerWifiBlock):
                    self.Wifi = p
                    self.setupSynchronisedShooting = False
                    return
    def update(self):
        platforms = self.game.LogicManager.platforms
        self.setupstuff(platforms)
        if len(self.targets) > 0:
            target = self.targets[0]
            
            if target.destroyed == True:
                self.targets.remove(target)
                return
        else:
            target = None

        
        if target == None:
            if self.health >= 100:
                self.xvel += random.randint(-1,1)
                self.yvel += random.randint(-1,1)
            elif self.health < 100:
                self.xvel += random.randint(-1,1)*80/self.health
                self.yvel += random.randint(-1,1)
            Character.update(self)
            return

            
        if   target.rect.x > self.rect.x:
            self.xvel += self.speed

        elif target.rect.x < self.rect.x:
            self.xvel -= self.speed
            
        if target.rect.bottom <= self.rect.y:           
            self.yvel -= self.speed



        shoot = random.randint(1, 20)
        if self.synchronisedShooting:
            shoot = 2
            if self.Wifi.cycletimer == 0:
                self.cycles += 1
            if self.cycles >= self.cyclemax:
                shoot = 1
                self.cycles = 0
                
        if shoot == 1:
            Tx = target.rect.left + 16
            Ty = target.rect.top  + 16
            Sx = self.rect.left   + 16
            Sy = self.rect.top    + 16
            deltaX = Tx - Sx
            deltaY = Ty - Sy


            denom = (deltaX**2 + deltaY**2)**.5

            if denom == 0: denom = .1
            deltaX /= denom
            time = denom/16
            
            yvel_laser = (deltaY - 1/2*\
                          self.game.LogicManager.globallaser.gravity * \
                          time**2)/time

            direction = (deltaX, yvel_laser/16)

            laser = normal_laser(Sx, Sy, self.game, direction)
            laser.shooter = self

        Character.update(self)
        



class TomatobombDrone(HamburgurDrone):
    def __init__(self, x, y,game):
        HamburgurDrone.__init__(self, x, y, game)
        self.shoot = 0
        
    def update(self):
        platforms = self.game.LogicManager.platforms
        entities = self.game.LogicManager.entities
        self.setupstuff(platforms)
        if len(self.targets) > 0:
            target = self.targets[0]
            
            if target.destroyed == True:
                self.targets.remove(target)
                return
        else:
            target = None

        
        if target == None:
            if self.health >= 100:
                self.xvel += random.randint(-1,1)
                self.yvel += random.randint(-1,1)
            elif self.health < 100:
                self.xvel += random.randint(-1,1)*80/self.health
                self.yvel += random.randint(-2,1)
            Character.update(self)
            for e in entities:
                if pygame.sprite.collide_rect(self, e):
                    if isinstance(e, normal_laser):
                        if e.shooter not in self.targets:
                            self.targets.append(e.shooter)
            return
        
        if   target.rect.x > self.rect.x:
            self.xvel += self.speed

        elif target.rect.x < self.rect.x:
            self.xvel -= self.speed
            
        if target.rect.bottom-160 <= self.rect.y:
            self.yvel -= self.speed*3#/distanceY/2

        self.shoot += 1
        self.shoot %= 10
        if self.synchronisedShooting:
            self.shoot = 1
            if self.Wifi.cycletimer == 0:
                self.cycles += 1
            if self.cycles >= self.cyclemax:
                self.shoot = 0
                self.cycles = 0
                
        for t in self.targets:
            if abs(self.rect.x-t.rect.x)<32 and self.shoot == 0:
                laser = bomb_laser(self.rect.left, self.rect.top, self.game)
                laser.shooter = self

        Character.update(self)

        for e in entities:
            if pygame.sprite.collide_rect(self, e):
                if isinstance(e, normal_laser) and \
                   not isinstance(e, bomb_laser):
                    if e.shooter not in self.targets:
                        self.targets.append(e.shooter)

class SniperDrone(HamburgurDrone):
    def __init__(self, x, y, game):
        HamburgurDrone.__init__(self, x, y, game)
        self.distance = 320
        self.cyclemax = 6
        
    def update(self):
        platforms = self.game.LogicManager.platforms
        entities = self.game.LogicManager.entities
        
        self.setupstuff(platforms)
        if len(self.targets) > 0:
            target = self.targets[0]
            
            if target.destroyed == True:
                self.targets.remove(target)
                return
        else:
            target = None

        
        if target == None:
            if self.health >= 100:
                self.xvel += random.randint(-1,1)
                self.yvel += random.randint(-1,1)
            elif self.health < 100:
                self.xvel += random.randint(-1,1)*80/self.health
                self.yvel += random.randint(-1,1)
            Character.update(self)
            return

        shoot = random.randint(1, 100)
        if self.synchronisedShooting:
            shoot = 2
            if self.Wifi.cycletimer == 0:
                self.cycles += 1
            if self.cycles >= self.cyclemax:
                shoot = 1
                self.cycles = 0
        
        if shoot == 1:
            Tx = target.rect.left + 16
            Ty = target.rect.top  + 16
            Sx = self.rect.left   + 16
            Sy = self.rect.top    + 16
            deltaX = Tx - Sx
            deltaY = Ty - Sy


            denom = (deltaX**2 + deltaY**2)**.5

            if denom == 0: denom = .1
            deltaX /= denom
            time = denom/16
            
            yvel_laser = (deltaY - 1/2*self.game.LogicManager.globallaser.gravity * \
                          time**2)/time

            direction = (deltaX, yvel_laser/16)

            laser = normal_laser(Sx, Sy, self.game, direction)

            
            laser.shooter = self
            laser.dissipation = 0
            laser.damage = 100

        Character.update(self)


class MachineGunDrone(HamburgurDrone):
    def __init__(self, x, y, game):
        HamburgurDrone.__init__(self, x, y, game)
    def update(self):
        platforms = self.game.LogicManager.platforms
        self.setupstuff(platforms)
        if len(self.targets) > 0:
            target = self.targets[0]
            
            if target.destroyed == True:
                self.targets.remove(target)
                return
        else:
            target = None

        
        if target == None:
            if self.health >= 100:
                self.xvel += random.randint(-1,1)
                self.yvel += random.randint(-1,1)
            elif self.health < 100:
                self.xvel += random.randint(-1,1)*80/self.health
                self.yvel += random.randint(-1,1)
            Character.update(self)
            return
        
        if   target.rect.x > self.rect.x:
            self.xvel += self.speed

        elif target.rect.x < self.rect.x:
            self.xvel -= self.speed
            
        if target.rect.bottom <= self.rect.y:
            self.yvel -= self.speed*3

        Tx = target.rect.left + 16
        Ty = target.rect.top  + 16
        Sx = self.rect.left   + 16
        Sy = self.rect.top    + 16
        deltaX = Tx - Sx
        deltaY = Ty - Sy

        laser = normal_laser(Sx, Sy, self.game, direction)

        denom = (deltaX**2 + deltaY**2)**.5

        if denom == 0: denom = .1
        deltaX /= denom
        time = denom/16
        
        yvel_laser = (deltaY - 1/2*self.game.LogicManager.globallaser.gravity * \
                      time**2)/time

        direction = (deltaX, yvel_laser/16)

        
        laser = normal_laser(Sx, Sy, self.game, direction)
        laser.shooter = self

        Character.update(self)






class BlockHider(HamburgurDrone):
    def __init__(self, x, y, game):
        HamburgurDrone.__init__(self, x, y, game,'blockhider')
##        self.image = pygame.image.load('data/pictures/BlockTest0.gif')
        self.health = 100
    def update(self):
        ##print(self.destroyed)
        if len(self.targets) > 0:
            target = self.targets[0]
            
            if target.destroyed == True:
                self.targets.remove(target)
                return
        else:
            target = None

        
        if target == None:
            if self.health >= 100:
                self.xvel += random.randint(-1,1)
                self.yvel += random.randint(-1,1)
            elif self.health < 100:
                self.xvel += random.randint(-1,1)*80/self.health
                self.yvel += random.randint(-1,1)
            Character.update(self)
            return
        
        if   target.rect.x > self.rect.x:
            self.xvel += self.speed

        elif target.rect.x < self.rect.x:
            self.xvel -= self.speed
            
        if target.rect.bottom <= self.rect.y:
            self.yvel -= self.speed*3


        shoot = random.randint(1,2)
        if shoot==1:
            for i in range(1):

                

                Tx = target.rect.left + 16 + random.randint(-128,128)
                Ty = target.rect.top  + 16 + random.randint(-128,128)
                Sx = self.rect.left   + 16
                Sy = self.rect.top    + 16
                deltaX = Tx - Sx
                deltaY = Ty - Sy

                denom = (deltaX**2 + deltaY**2)**.5
                time = denom/16
                yvel_laser = (deltaY - 1/2*self.game.LogicManager.globallaser.gravity * \
                              time**2)
                if denom == 0: denom = 1
                deltaX /= denom
                if time == 0: time = 1
                yvel_laser /= time

                ##print(deltaX*100, deltaY)

                direction = (deltaX,
                             yvel_laser/16)
                #direction = (deltaX, yvel_laser/16)

                laser = WaterLazer(Sx, Sy, self.game,direction=direction)
                laser.shooter = self

                ##print(laser.xvel)

        ##print(self.destroyed)
        Character.update(self)
        ##print(self.destroyed)








class normal_laser(Entity):

    def __init__(self, x, y, game, direction=(1,0)):
        Entity.__init__(self, game,'laser',pygame.Rect(x, y, 5, 5))
        self.game.LogicManager.lasers.add(self)
        self.speed = 16
        self.damage = 10
        self.dissipation = .1
        width = height = 1
        if direction[0]!=0: width =5
        if direction[1]!=0: height=5
        #elif direction[1] == 0: direction = (direction[0], -1)
        self.xvel = direction[0]*self.speed
        self.yvel = direction[1]*self.speed
        self.shooter = None
        self.destroyed = False
        self.direction = direction
        self.prevRect = self.rect.copy()

    def update(self):
        Entity.updateimg(self)
        self.prevRect = self.rect.copy()
        
        if self.damage > 0: self.damage -= self.dissipation
        if self.damage < 0: self.damage = 0
        
        # accelerate with gravity
        self.yvel += self.game.LogicManager.globallaser.gravity/ \
                     self.Time_Scale
        # max falling speed
        if self.yvel > 100: self.yvel = 100

        # deaccelerate with friction
        self.xvel *= self.game.LogicManager.globallaser.friction/ \
                      self.Time_Scale
        self.yvel *= self.game.LogicManager.globallaser.friction/ \
                      self.Time_Scale

        self.rect.left += round(self.xvel/self.Time_Scale)
        self.rect.top += round(self.yvel/self.Time_Scale)


    def collide(self, e):

        if isinstance(e, Platform):
            ## figure out collision stuff
            
            rx = self.prevRect.copy()
            rx.left += self.xvel/self.Time_Scale

            ry = self.prevRect.copy()
            ry.top  += self.yvel/self.Time_Scale


            xcollide = rx.colliderect(e.rect)
            ycollide = ry.colliderect(e.rect)

            if xcollide and not ycollide:
                # x fault
                yvel = 0
                xvel = self.xvel
            elif ycollide and not xcollide:
                # y fault
                xvel = 0
                yvel = self.yvel
            elif xcollide and ycollide:
                ##print('huh',rx.left,p.rect.left,ry.top,p.rect.top)
                xvel = self.xvel
                yvel = 0#self.yvel
                # inside of p
            elif not xcollide and not ycollide:
                xdis = abs(e.rect.left-rx.left)
                ydis = abs(e.rect.top -rx.top)
                if xdis < ydis:
                    # x fault
                    yvel = 0
                    xvel = self.xvel
                elif ydis < xdis:
                    # y fault
                    xvel = 0
                    yvel = self.yvel
                else:
                    yvel = self.yvel
                    xvel = self.xvel
                    ##print('huh')
            else:
                xvel = self.xvel
                yvel = self.yvel
                #print('should never get here')

            if isinstance(e, BounceBlock):
                ##print('reflect')
                if xvel != 0:
                    self.xvel *= -1
                    if xvel < 0:
                        self.rect.left = e.rect.right
                    if xvel > 0:
                        self.rect.right = e.rect.left
                if yvel != 0:
                    self.yvel *= -1
                    if yvel < 0:
                        self.rect.top = e.rect.bottom
                    if yvel > 0:
                        self.rect.bottom = e.rect.top
                if random.randint(0,
                        self.game.LogicManager.globallaser.ReflectChance) == 0:
                    self.destroyed = True

            elif isinstance(e, DeathBlock):
                self.destroyed = True

        if e != self.shooter:
            ##print(e, self.shooter)
            if not (isinstance(e, ContainmentBlock) or \
                    isinstance(e, BounceBlock)):
                self.destroyed = True
##                    self.game.LogicManager.globallaser.List.remove(self)
##                    Entities.remove(self)

##                    for target in self.targets:
##
##                        if e == target:
            if isinstance(e, bomb_laser):
                self.destroyed = True
                e.exploding = True
                e.img_index += 1
            elif isinstance(e, super_laser):
                self.destroyed = True
            elif isinstance(e, normal_laser):
                self.destroyed = True
                e.destroyed = True
                
            if isinstance(e, Character):
                    if e.health == -1:
                        return

                    e. health -= self.damage
                    if e.health <= 0:
                        e.health = 0
                        #entities.remove(e)

            return


class heat_seaking_laser(normal_laser):
    def __init__(self, x, y,game, direction=(1,0)):
        normal_laser.__init__(self, x, y,game, direction)
        self.targets = []
        self.speed = 1
        self.damage = 10
        self.movetimer = 6
        self.moverate = 20
        self.dissipation = 0

    def update(self):

        normal_laser.update(self)
        if len(self.targets) == 0:
            ##print('sigh')
            return

        if self.targets[0].destroyed == True:
            self.targets.pop(0)
            return

        if self.movetimer > 0: self.movetimer -= 1

        if self.movetimer <= 0:
            self.movetimer = self.moverate

            Ex = self.targets[0].rect.centerx
            Ey = self.targets[0].rect.centery
            Sx = self.rect.centerx
            Sy = self.rect.centery
            deltaX = Ex - Sx
            deltaY = Ey - Sy
            
            denom = (deltaX**2 + deltaY**2)**.5
            if denom == 0: denom = 0.1
            deltaX /= denom
    ##                deltaY /= denom
            time = denom/16#laser.speed
            yvel = (deltaY - 1/2*self.game.LogicManager.globallaser.gravity * \
                    time**2)/time

            self.direction = (deltaX, yvel/16)#laser.speed)
            self.xvel = self.direction[0]*self.speed
            self.yvel = self.direction[1]*self.speed
            ##print(self.xvel)
            ##print(self.direction)



class super_laser(normal_laser):
    def __init__(self, x, y, game, direction=(1,0)):
        normal_laser.__init__(self, x, y,game, direction)
        self.damage = 50
        self.dissipation = 5

    def collide(self, e):


        if isinstance(e, DeathBlock) or \
            isinstance(e, IndestructibleBlock) or \
            isinstance(e, ExitBlock):
            self.destroyed = True
            return

        if e != self.shooter and not e == self:
            ##print(e, self.shooter)
            if not (isinstance(e, ContainmentBlock) or\
                    isinstance(e, normal_laser)):
                self.destroyed = True
            if isinstance(e, Platform):
                e.destroyed = True
                e.destroy()
##                    self.game.LogicManager.globallaser.List.remove(self)
##                    Entities.remove(self)

##                    for target in self.targets:
##
##                        if e == target:
            if isinstance(e, Character):
                    if e.health == -1:
                        return

                    e.health -= self.damage
##                        if e.health <= 0:
##                            e.health = 0
##                            e.destroyed = True

            return


class floor_destroying_laser(super_laser):
    def __init__(self, x, y,game):
        super_laser.__init__(self, x, y,game, (0, 1))

class bomb_laser(normal_laser):
    def __init__(self, x, y,game, direction=(0,0)):
        normal_laser.__init__(self, x, y,game, (1,1))
##        self.image = pygame.image.load('data/pictures/tomatoTest0.gif')
        self.rect = pygame.Rect(x, y, 32, 32)
        self.direction = (0, 0)
        self.xvel = self.yvel = 0
        self.damage = 40
        self.dissipation = 0
        self.img_index = 0
        self.exploding = False
        self.explosionradius = 32
        self.destroyblocks = False
    def update(self):
        ##print(self.shooter)
        if self.exploding:
            self.img_index += 1
##            self.xvel = 0
##            self.yvel = 0
            if self.img_index >= 21:
                self.destroyed = True
                self.img_index  %= 15
##        self.image = pygame.image.load('data/pictures/tomatoTest%s.gif'
##                                       % (str(self.img_index)))
        #self.damage = self.yvel + 40
        
        normal_laser.update(self)

    def collide(self, e):


        if isinstance(e, BounceBlock):
            if self.xvel != 0: self.xvel *= -1
            if self.yvel != 0: self.yvel *= -1
            if random.randint(0,
                self.game.LogicManager.globallaser.ReflectChance) == 0:
                self.destroyed = True

        elif isinstance(e, DeathBlock):
            self.destroyed = True

        elif isinstance(e, Platform) and not\
             isinstance(e, ContainmentBlock):
            if self.yvel > 0:
                self.rect.bottom = e.rect.top
                self.yvel = 0
            if self.yvel < 0:
                self.yvel = 0
                self.rect.top = e.rect.bottom
        
        elif e != self.shooter and e != self:
            if isinstance(e, bomb_laser):
                e.exploding = True
                self.destroyed = True
            elif isinstance(e, normal_laser):
                self.exploding = True
                e.destroyed = True
            elif not (isinstance(e, ContainmentBlock)):
                self.exploding = True
                
##    if self.exploding and \
##       ((self.rect.left-e.rect.left)**2+\
##        (self.rect.top-e.rect.top)**2)**.5\
##        < self.explosionradius:
##        
##        if isinstance(e, DeathBlock) or \
##           isinstance(e, IndestructibleBlock) or \
##           isinstance(e, ExitBlock):
##            
##            self.destroyed = True
##            continue
##        
##        elif isinstance(e, Character):
##            ##print(e, self.shooter, e == self.shooter)
##            if e.health == -1:
##                continue
##
##            e. health -= self.damage
##            if e.health <= 0:
##                e.health = 0
##                Entities.remove(e)
##                
##        elif isinstance(e, Platform):
##            if self.destroyblocks:
##                e.destroyed = True
##
##        elif isinstance(e, bomb_laser):
##            e.exploding = True
##            
##        elif isinstance(e, normal_laser):
##            e.destroyed = True




class WaterLazer(normal_laser):
    def __init__(self, x, y,game, direction=(1,0)):
        normal_laser.__init__(self, x, y,game, direction)
        width = 20; height = 20
##        self.image = pygame.Surface((width, height))
##        self.image.convert()
##        self.image.fill(pygame.Color("#ff000000"))
        self.speed = 1
        self.damage = 1
        self.dissipation = 0.05


    def collide(self, e):


        if isinstance(e, BounceBlock):
            self.xvel *= -1
            self.yvel *= -1
            if random.randint(0,
                self.game.LogicManager.globallaser.ReflectChance) == 0:
                self.destroyed = True

        elif isinstance(e, DeathBlock):
            self.destroyed = True

        elif e != self.shooter and not e == self:
            ##print(e, self.shooter)
            if not (isinstance(e, ContainmentBlock)):
                self.destroyed = True
##                    self.game.LogicManager.globallaser.List.remove(self)
##                    Entities.remove(self)

##                    for target in self.targets:
##
##                        if e == target:
            if isinstance(e, bomb_laser):
                self.destroyed = True
                e.exploding = True
                e.img_index += 1
            elif isinstance(e, super_laser):
                self.destroyed = True
            elif isinstance(e, normal_laser) and not \
                 isinstance(e, WaterLazer):
                self.destroyed = True
                e.destroyed = True
                
            if isinstance(e, Character):
                    if e.health == -1:
                        return
            return
    


class Platform(Entity):
    def __init__(self, x, y, game,img='platform'):
        Entity.__init__(self,game,img,pygame.Rect(x, y, 32, 32))
        self.game.LogicManager.platforms.add(self)
        self.platforms = self.game.LogicManager.platforms
        self.destroyed = False

    def update(self):
        Entity.updateimg(self)
    def destroy(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y, game):
        Platform.__init__(self, x, y, game,'exitblock')


class BounceBlock(Platform):
    def __init__(self, x, y, bounciness, game):
        Platform.__init__(self, x, y, game,'bounceblock')
        self.reflect = bounciness

class BigLogo(Platform):
    def __init__(self, x, y, game):
        Platform.__init__(self, x, y, game,'yellowblock')

class DeathBlock(Platform):
    def __init__(self, x, y, game):
        Platform.__init__(self, x, y, game,'missingasset')

class IndestructibleBlock(Platform):
    def __init__(self, x, y, game):
        Platform.__init__(self, x, y, game)

class ContainmentBlock(Platform):
    def __init__(self, x, y, game):
        Platform.__init__(self, x, y, game,'whiteblock')

class LetterBlock(Platform):
    def __init__(self, x, y, letter, game):
        Platform.__init__(self, x, y, game,'letter')
        font = pygame.font.SysFont('monospace', 20)
        self.animationbase = letter
        
class SpawnerBlock(Platform):
    def destroy(self):
        b=BlockHider(self.rect.left,self.rect.top,self.game)
        b.targets.append(self.game.LogicManager.player)

class DistanceSpawnerBlock(SpawnerBlock):
    def __init__(self, x, y,target, game):
        Platform.__init__(self,x,y,game)
        self.target = target
        self.range = 100
    def update(self):
        deltaX = self.target.rect.x - self.rect.x
        deltaY = self.target.rect.y - self.rect.y
            
        denom = (deltaX**2 + deltaY**2)**.5
        if denom <= self.range:
            self.destroyed = True
            b=BlockHider(self.rect.left,self.rect.top, self.game)
            b.targets.append(self.game.LogicManager.player)


class ZoomBlock(Platform):
    def __init__(self,x,y,game):
        Platform.__init__(self,x,y,game,'zoomblock')
        self.zoominess = 10
##        self.image = pygame.Surface((32, 32))
##        self.image.convert()
##        self.image.fill(pygame.Color("#1cfc11"))

class ShooterBlock(Platform):
    def __init__(self,x,y,game):
        Platform.__init__(self,x,y,game,'shooterblock')
    def update(self):
        shoot = random.randint(0,10)
        if shoot == 0:
            ##directions = ((1,0),(-1,0),(0,1),
            ##              (0,-1),(1,1),(0,0),
            ##              (-1,1),(1,-1))
            directions = ((0,-1),)
            laser = normal_laser(self.rect.left, self.rect.top,
                                 self.game,
                        directions[random.randint(0,len(directions)-1)],
                                 )
            laser.shooter = self



class BetterShooterBlock(Platform):
    def __init__(self,x,y,target, game):
        Platform.__init__(self,x,y,game,'shooterblock')
        self.target = target
        self.range = 200
    def update(self):
        shoot = random.randint(0,20)
        if shoot == 0:
        
            deltaX = self.target.rect.x - self.rect.x
            deltaY = self.target.rect.y - self.rect.y
                
            denom = (deltaX**2 + deltaY**2)**.5
            if denom >= self.range: return
            if denom == 0: denom = 0.1
            deltaX /= denom
##                deltaY /= denom
            time = denom/16#laser.speed
            yvel = (deltaY - 1/2*self.game.LogicManager.globallaser.gravity * time**2)/time

            direction = (deltaX, yvel/16)#laser.speed)
            
            laser = normal_laser(self.rect.left, self.rect.top, self.game,
                                 direction
                                 )
            laser.shooter = self
            laser.damage = 6
            laser.dissipation = 0.5


class HamburgerWifiBlock(Platform):
    def __init__(self,x,y, game):
        Platform.__init__(self,x,y,game,'wifiblock')
        self.cycletimermax = 20
        self.cycletimer = 0
    def update(self):
        self.cycletimer += 1
        if self.cycletimer >= self.cycletimermax:
            self.cycletimer = 0

