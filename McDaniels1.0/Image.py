import pygame


class ImageLoader:
    def __init__(self):
        self.missingasset = pygame.Surface((0,0))
        self.imagedict = {
            'missingasset':{'idle0':self.missingasset},
            
            'player':self.loadimage('data\pictures\player.frames'),
            
            'platform':self.loadimage('data\pictures\platform.frames'),
            
            'drone':self.loadimage('data\pictures\\bounceblock.frames'),
            
            'bounceblock':self.loadimage('data\pictures\\bounceblock.frames'),
            
            'enemy':self.loadimage('data\pictures\enemy.frames'),
            
            'blockhider':self.loadimage('data\pictures\\blockhider.frames'),
            
            'exitblock':self.loadimage('data\pictures\exitblock.frames'),

            'zoomblock':self.loadimage('data\pictures\zoomblock.frames'),
            
            'laser':{'idle0':self.makerect((255, 215, 0, 255),5,5)},

            'whiteblock':{'idle0':self.makerect((255, 255, 255, 255),5,5)},

            'redblock':{'idle0':self.makerect((255, 0, 0, 255),5,5)},

            'yellowblock':{'idle0':self.makerect((255, 255, 0, 255),5,5)},

            'greenblock':{'idle0':self.makerect((0, 255, 0, 255),5,5)},

            'cyanblock':{'idle0':self.makerect((0, 255, 255, 255),5,5)},

            'blueblock':{'idle0':self.makerect((0, 0, 255, 255),5,5)},

            'purpleblock':{'idle0':self.makerect((255, 0, 255, 255),5,5)},
            }

    def loadimage(self, framename):

        outdict = {}

        with open(framename,'r') as frame:
            
            base = pygame.image.load(frame.readline()[:-1])
            
            gridsize = [int(i) for i in frame.readline().split(' ')]
            dimension = [int(i) for i in frame.readline().split(' ')]
            #label = [frame.readline() for i in range(
            #    dimension[0]*dimension[1])]
            for y in range(dimension[1]):
                for x in range(dimension[0]):
                    aliases = [i for i in frame.readline()[:-1].split(' ')]
                    print(aliases)
                    img = pygame.Surface(gridsize, pygame.SRCALPHA, 32)
                    img = img.convert_alpha()
                    img.blit(base,(-x*gridsize[0],-y*gridsize[1]))

                    for a in aliases:
                        outdict[a] = img
        return outdict



    def makerect(self,color, w, h):
        surface = pygame.Surface((w,h))
        surface.fill(color)
        surface.convert()
        return surface
