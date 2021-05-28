import pygame
import time
class Player(pygame.Rect):

    def __init__(self,screen):
        self.x_=16
        self.y_=310
        self.screen_=screen



    def draw(self):
        #for block in self.blocks:
            pygame.draw.rect(self.screen_, (255, 69, 0), pygame.Rect(self.x_,self.y_,6,6))

    def move(self,dx,dy):
        #_blocks[0] - the middle block of plane
        if self.x_+dx-3>0 and self.x_+ dx+3 < 475 and self.y_+dy>0 and self.y_+dy<320:
                self.x_+=dx
                self.y_+=dy

