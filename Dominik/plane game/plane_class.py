import pygame, os
from pygame.math import Vector2

class Plane(pygame.Rect):

    def __init__(self,screen):
        os.chdir('/home/pi/Desktop/main/menu/Plane')
        
        #plane consist of blocks
        self._blocks = (Vector2(6 * 22 + 8,screen.get_height()-26), Vector2(7 * 22 + 8,screen.get_height()-47), Vector2(7 * 22 + 8, screen.get_height() - 26),Vector2(8 * 22 + 8, screen.get_height() - 26))
        
        #information about screen location
        self._screen = screen
        middle = screen.get_width() / 2*15/22

    def draw(self):
        for block in self._blocks:
            pygame.draw.rect(self._screen, (255,255, 255), pygame.Rect(block.x,block.y,20,20))


    def move(self, dx):
        #_blocks[0] - the middle block of plane
        if self._blocks[0].x + dx >= 0 * 22 + 8 and self._blocks[0].x + dx < 14 * 22 + 8:
            for block in self._blocks:
                block.x += dx

    def get_position(self):
        return self._blocks[1]


        