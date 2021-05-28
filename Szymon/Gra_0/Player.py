import pygame
import time
class Player(pygame.Rect):

    def __init__(self,screen):
        self.blocks = []
        self.screen_=screen
        self.x_start_=15.5
        self.y_start_=310
        self.blocks.append([self.x_start_, self.y_start_])


    def draw(self):
        for block in self.blocks:
            pygame.draw.rect(self.screen_, (255, 69, 0), pygame.Rect(block[0],block[1],6,6))

    def move(self,dx,dy):
        #_blocks[0] - the middle block of plane
        if self.blocks[0][0]+dx-3>0 and self.blocks[0][0] + dx+3 < 475 and self.blocks[0][1]+dy>0 and self.blocks[0][1]+dy<320:
            for block in self.blocks:
                block[0]+=dx
                block[1]+=dy

    def get_position(self):
        return [self.blocks[1][0],self.blocks[1][1]]
