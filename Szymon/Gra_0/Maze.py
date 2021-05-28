import pygame
import time

class Maze(pygame.Rect):
    def __init__(self, screen,width,color):
        self.screen_ = screen
        self.color_=color
        self.width_=width
    def set_color(self,new_color):
        self.color_=new_color
    def draw_level_1(self):
        pygame.draw.line(self.screen_, self.color_,
                         (10, 320), (10, 200), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (30, 320), (30, 220), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (30, 220), (150, 220), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (10, 200), (130, 200), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (130, 200), (130, 150), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (150, 220), (150, 170), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (150, 170), (180, 170), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (130, 150), (200, 150), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (180, 170), (180, 240), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (200, 150), (200, 220), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (180, 240), (350, 240), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (200, 220), (330, 220), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (350, 240), (350, 100), self.width_)
        pygame.draw.line(self.screen_,self.color_,
                         (330, 220), (330, 100), self.width_)
        pygame.draw.line(self.screen_,self.color_,
                         (350, 100), (420, 100), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (330, 100), (260, 100), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (260, 100), (260, 30), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (420, 100), (420, 30), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (420, 30), (350, 30), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (260, 30), (330, 30), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (330, 30), (330, 0), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (350, 30), (350, 0), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (280, 80), (400, 80), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (280, 50), (400, 50), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (280, 80), (280, 50), self.width_)
        pygame.draw.line(self.screen_, self.color_,
                         (400, 80), (400, 50), self.width_)
        pygame.draw.rect(self.screen_, (255, 255, 255), [330, 0, 20, 10])






