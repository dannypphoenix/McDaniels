import pygame, random
from Entities import *
from Game import GameManager


def main(leveltoplay=0):
    

    game.initnewlevel()
    

    #player.health = -1; #player.jetpack = True
    playerstartL = playerstartT = 32
    up = down = left = right = running = sneaking = False
    
    x = y = 0

    number_of_levels = 8

##    cl = 1
##    while cl <= 5:
##        l = open('levels/level%s.txt' %(str(cl)))
##        linfo = l.read()
##        l.close()
##        levels += eval(linfo)
##        print(eval(linfo))
##        cl += 1

    leveltoplay %= number_of_levels
    l = open('data/levels/level%s.txt' %(str(leveltoplay+1))); mode = 0
    #l = open('data/super_hard_levels/level%s.txt' %(str(leveltoplay+1))); mode = 1
    level = eval(l.read())
    l.close()
    #level = levels[leveltoplay]
    # build the level
    enemyspeed = 3
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y, game)
            if col == "E":
                e = ExitBlock(x, y, game)
            if col == 'T':
                t = BounceBlock(x, y, .5, game)
            if col == 'M':
                m = BigLogo(x, y, game)
                if mode == 0 and leveltoplay == 4:
                    game.LogicManager.mustdestroy.append(m)
            if col == 'D':
                d = DeathBlock(x, y, game)
            if col == 'C':
                c = ContainmentBlock(x, y, game)
                if mode == 1 and leveltoplay == 6:
                    game.LogicManager.mustdestroy.append(c)
            if col == 'W':
                b = SpawnerBlock(x, y, game)
            if col == 'Z':
                z = ZoomBlock(x, y, game)
            if col == 'O':
                s = ShooterBlock(x, y, game)
            if col == 'V':
                s = BetterShooterBlock(x, y, game.LogicManager.player, game)
            if col == 'I':
                s = DistanceSpawnerBlock(x, y, game.LogicManager.player, game)
            if col == 'h':
                h = HamburgerWifiBlock(160,160,game)
            if col == 'S':
                s = Enemy(x, y, game)
                s.speed = enemyspeed; enemyspeed += 1
            if col == 'H':
                h = HamburgurDrone(x, y, game)
                h.targets.append(game.LogicManager.player)
            if col == 'B':
                b = TomatobombDrone(x, y, game)
                b.targets.add(game.LogicManager.player)
            if col == 'N':
                n = SniperDrone(x, y, game)
                n.targets.append(game.LogicManager.player)
            if col == 'G':
                g = MachineGunDrone(x, y,game)
                g.targets.append(game.LogicManager.player)
            if col == '*':
                playerstartL = x
                playerstartT = y
                
            x += 32
        y += 32
        x = 0



    level_width = len(level[0])*32
    level_height = len(level)*32

    laser_types = (heat_seaking_laser,
                   normal_laser, normal_laser, normal_laser, normal_laser,
                   normal_laser,
                   )


    game.LogicManager.player.rect.left = playerstartL
    game.LogicManager.player.rect.top  = playerstartT
    #camera_to_use = game.GraphicsManager.complex_camera
    borderlimit   = False


    # aUTO
    moveindex = 0
    tomove = []
##    with open('data/moves/hard_levels_%s.txt' % (str(leveltoplay))) as m:
##                tomove=eval(m.readlines()[-1])
##                m.close()

    if mode == 0:

        if leveltoplay == 0:
            game.LogicManager.player.distancelimity = 1000

        elif leveltoplay == 1:
            game.LogicManager.player.distancelimity = 1000

        elif leveltoplay == 2:
            pass#camera_to_use = simple_camera

        elif leveltoplay == 3:
            pass

        elif leveltoplay == 4:
            
            laser_types = (super_laser,)
        
        elif leveltoplay == 5:
            pass
        
        elif leveltoplay == 6:
            l#azer_types = (super_laser, )
            bombers = []
            gunners = []
            
##            for i in range(10):
##                b = TomatobombDrone((i+9)*32, 32*6)
##                #b.targets.append(player)
##                #b.health = 1000
##                entities.add(b)
##                drones.append(b)
##                healthbars.append(b.healthbar)
##                b.targets = gunners
##                bombers.append(b)
##
##            for i in range(10):
##                g = MachineGunDrone((i+9)*32, 32*5)
##                #g.targets.append(player)
##                #g.health = 1000
##                entities.add(g)
##                drones.append(g)
##                healthbars.append(g.healthbar)
##                g.targets = bombers
##                gunners.append(g)

            

        
        elif leveltoplay == 7:
            game.LogicManager.player.jetpack = True
            for e in game.live_enemies:
                e.respawn = False
            #laser_types = (super_laser,)


    elif mode == 1:

        

        if leveltoplay == 0:
            for e in game.LogicManager.entities:
                if isinstance(e, HamburgurDrone):
                    e.synchronisedShooting = True
            
        if leveltoplay == 1:
            game.LogicManager.player.distancelimity = 1000
            #camera_to_use = 'simple camera'
            p = ExitBlock(14400,224,game)
            z = ZoomBlock(32,32,game)
            z.zoominess = 1000
            level_width = 16000
            
            

        if leveltoplay == 2:
            game.LogicManager.player.distancelimity = 10000

        if leveltoplay == 3:
            game.LogicManager.globallaser.ReflectChance = 100

        if leveltoplay == 4:
            game.LogicManager.player.distancelimity = 96
            #camera_to_use = game.simple_camera

        if leveltoplay == 5:
            #laser_types = (super_laser,)
            game.LogicManager.player.distancelimity = 2170
            game.LogicManager.player.continuousshoot = floor_destroying_laser
            borderlimit = True

        if leveltoplay == 6:
            laser_types = (super_laser,)
            game.LogicManager.player.jetpack = False#True
            game.LogicManager.player.distancelimitx = 2816
            game.LogicManager.player.distancelimity = 2976

            bomb_positions = ((2528,32),(1280,64),(384,160),(2432,320),
                              (1024,352),(1472,416),(1504,416),(320,512),
                              (1984,608),(64,800),(2048,864),(832,992),
                              (11568,1248),(2432,1344),(192,1376),(960,1440),
                              (1568,1248))

            for i in range(len(bomb_positions)):
                b = bomb_laser(bomb_positions[i][0], bomb_positions[i][1],
                               game)
                #entities.add(b)
                b.shooter = game.LogicManager.player
                b.explosionradius = 500
                b.destroyblocks = True
                b.damage = 0
            

        if leveltoplay == 7:
            pass

        if leveltoplay == 8:
            pass

        if leveltoplay == 9:
            pass

    #total_level_height = len(level)*32
    current_laser = laser_types[random.randint(0, len(laser_types)-1)]

    
    game.lateinit(tomove,level_width,level_height)
    game.GraphicsManager.camera.borderlimit = borderlimit
    total_frame_count = 0

    
    return game.mainLoop()



if __name__ == '__main__':
    ## start sound
    pygame.init()
    game = GameManager()
    pygame.mixer.init()
    pygame.mixer.music.load('data/Sounds/McdonaldsTest_5.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0)#.51)
    currentnum = 0
    while 1:
        won = main(currentnum)
        if won:
            currentnum += 1
            print(game.InputManager.buttonlog)
