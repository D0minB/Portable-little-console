import pygame

class Plane(pygame.Rect):

    def __init__(self,screen):
        #plane consist of blocks
        self._blocks = []
        #information about screen location
        self._screen=screen
        middle=screen.get_width() / 2*15/22
        self._blocks.append([middle, screen.get_height() - 20 - 1])
        self._blocks.append([middle, screen.get_height() - 20 - 1 - 21])
        self._blocks.append([middle+ 21, screen.get_height() - 20 - 1])
        self._blocks.append([middle - 21, screen.get_height() - 20 - 1])

    def draw(self):
        for block in self._blocks:
            pygame.draw.rect(self._screen, (19, 56, 207), pygame.Rect(block[0],block[1],20,20))

    def move(self,dx):
        #_blocks[0] - the middle block of plane
        if self._blocks[0][0]+dx-10>0 and self._blocks[0][0] + dx < 15/22*self._screen.get_width()+20:
            for block in self._blocks:
                block[0]+=dx

    def get_position(self):
        return [self._blocks[1][0],self._blocks[1][1]]