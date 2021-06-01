import pygame
import time

class Maze(pygame.Rect):
    def __init__(self, screen,width,color):
        self.screen_ = screen
        self.linie=[]
        self.linie2=[]
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

        self.linie2.append((10, 50, 10, 320))
        self.linie2.append((30, 70, 30, 320))
        self.linie2.append((10,50,60,50))
        self.linie2.append((30, 70, 40, 70))
        self.linie2.append((40, 70, 40, 290))
        self.linie2.append((60, 50, 60, 270))
        self.linie2.append((60, 270, 100, 270))
        self.linie2.append((40, 290, 120, 290))
        self.linie2.append((120, 270, 120, 290))
        self.linie2.append((100, 250, 100, 270))
        self.linie2.append((120, 270, 300, 270))
        self.linie2.append((100, 250, 280, 250))
        self.linie2.append((300, 250, 300, 270))
        self.linie2.append((280, 230, 280, 250))
        self.linie2.append((300, 250, 350, 250))
        self.linie2.append((280, 230, 370, 230))
        self.linie2.append((370, 230, 370, 290))
        self.linie2.append((350, 250, 350, 310))
        self.linie2.append((350, 310, 430, 310))
        self.linie2.append((370, 290, 410, 290))
        self.linie2.append((410, 60, 410, 290))
        self.linie2.append((430, 40, 430, 310))
        self.linie2.append((330, 60, 410, 60))
        self.linie2.append((350, 40, 430, 40))
        self.linie2.append((350, 0, 350, 40))
        self.linie2.append((330, 0, 330, 60))
        #self.blocks.append((10,200))

    def set_color(self,new_color):
        self.color_=new_color
    def draw_level_1(self):
     for block in self.linie:
         pygame.draw.line(self.screen_,self.color_,(block[0],block[1]),(block[2],block[3]),self.width_)
    def draw_level_2(self):
     for block in self.linie2:
         pygame.draw.line(self.screen_,self.color_,(block[0],block[1]),(block[2],block[3]),self.width_)











