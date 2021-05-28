import pygame

class Plane(pygame.Rect):

    def __init__(self,screen):
        #plane consist of blocks
        self._blocks = []
        #information about screen location
        self._screen=screen
        middle=screen.get_width() / 2*15/22
        self._blocks.append([middle, screen.get_height() - 20 - 1-5])
        self._blocks.append([middle, screen.get_height() - 20 - 1 - 21-5])
        self._blocks.append([middle+ 21, screen.get_height() - 20 - 1-5])
        self._blocks.append([middle - 21, screen.get_height() - 20 - 1-5])

    def draw(self):
        for block in self._blocks:
            pygame.draw.rect(self._screen, (255,255, 255), pygame.Rect(block[0],block[1],20,20))

    def move(self,dx):
        #_blocks[0] - the middle block of plane
        if self._blocks[0][0]+dx>22 and self._blocks[0][0] + dx < 14/22*self._screen.get_width()+20:
            for block in self._blocks:
                block[0]+=dx

    def get_position(self):
        return [self._blocks[1][0],self._blocks[1][1]]