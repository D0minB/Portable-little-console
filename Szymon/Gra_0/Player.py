import pygame
import time
# class Player(pygame.Rect):
#     def __init__(self,screen,color):
#         self.screen_ = screen
#         self.color_ = color
#         self.pos_x_start_=20
#         self.pos_y_start_=255
#         self.pos_x_
#         self.pos_y_
#         self.fps=10
#
#     def set_color(self,new_color):
#         self.color_=new_color
#     def move(self,sreen,):
#         if pygame.key.get_pressed()[pygame.K_LEFT]:
#             self.pos_x_ -= int(150 / self.fps)
#         if pygame.key.get_pressed()[pygame.K_RIGHT]:
#             self.pos_x_ += int(150 / self.fps)
#         self.move(self.pos_x_)
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
