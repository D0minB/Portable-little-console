import pygame
import time

class Maze(pygame.Rect):
    def __init__(self, screen,width,color):
        self.screen_ = screen
        self.linie=[]
        self.color_=color
        self.width_=width
        self.linie.append((10, 200,10,320))
        self.linie.append((30, 220, 30, 320))

        self.linie.append((30, 220, 150, 220))
        self.linie.append((10, 200, 130, 200))
        self.linie.append((130, 150, 130, 200))

        self.linie.append((150, 170, 150, 220))
        self.linie.append((150, 170, 180, 170))
        self.linie.append((130, 150, 200, 150))

        self.linie.append((180, 240, 180, 170))
        self.linie.append((200, 150, 200, 220))
        self.linie.append((180, 240, 350, 240))

        self.linie.append((200, 220, 330, 220))
        self.linie.append((350, 100, 350, 240))
        self.linie.append((330, 100, 330, 220))

        self.linie.append((350, 100, 420, 100))
        self.linie.append((260, 100, 330, 100))
        self.linie.append((260, 30, 260, 100))

        self.linie.append((420, 30, 420, 100))
        self.linie.append((350, 30, 420, 30))
        self.linie.append((260, 30, 330, 30))

        self.linie.append((330, 0, 330, 30))
        self.linie.append((350, 0, 350, 30))
        self.linie.append((280, 80, 400, 80))

        self.linie.append((280, 50, 400, 50))
        self.linie.append((280, 50, 280, 80))
        self.linie.append((400, 50, 400, 80))



        #self.blocks.append((10,200))
    def set_color(self,new_color):
        self.color_=new_color
    def draw_level_1(self):


     for block in self.linie:
         pygame.draw.line(self.screen_,self.color_,(block[0],block[1]),(block[2],block[3]),self.width_)












