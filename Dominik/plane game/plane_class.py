import pygame
from pygame.math import Vector2

class Plane(pygame.Rect):

    def __init__(self,screen):
        #plane consist of blocks
        middle=screen.get_width() / 2*15/22
        self._blocks = (Vector2(middle,screen.get_height()-26), Vector2(middle,screen.get_height()-47), Vector2(middle+ 21, screen.get_height() - 26),Vector2(middle - 21, screen.get_height() - 26))
        
        #information about screen location
        self._screen=screen
        middle=screen.get_width() / 2*15/22

    def draw(self):
        for block in self._blocks:
            pygame.draw.rect(self._screen, (255,255, 255), pygame.Rect(block.x,block.y,20,20))


    def move(self,dx):
        #_blocks[0] - the middle block of plane
        if self._blocks[0].x+dx>28 and self._blocks[0].x + dx < 14/22*self._screen.get_width()+13:
            for block in self._blocks:
                block.x+=dx

    def get_position(self):
        return self._blocks[1]

        
    def update(self,dx):
        if dx>0:
            pygame.display.update(pygame.Rect(self._blocks[3].x-dx,self._blocks[1].y,63+dx,42))
        elif dx<0:
            pygame.display.update(pygame.Rect(self._blocks[3].x,self._blocks[1].y,63+abs(dx),42))
        