import pygame
import time

class Maze(pygame.Rect):
    def __init__(self, screen,width):
        self.screen_ = screen
        self.linie=[]
        self.linie2=[]
        self.linie3=[]
        self.linie4=[]
        self.linie5=[]
        self.linie51=[]
        self.color_=(0,0,0)
        self.width_=width
        self.yg_ = -40
        self.yd_ = 0
        self.vy_ = 35

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

        self.linie3.append((10,210,10,320))
        self.linie3.append((30, 230, 30, 320))
        self.linie3.append((30, 230, 60, 230))
        self.linie3.append((10, 210, 100, 210))
        self.linie3.append((60, 230, 60, 315))
        self.linie3.append((80, 230, 80, 300))
        self.linie3.append((80, 230, 120, 230))
        self.linie3.append((100, 140, 100, 210))
        self.linie3.append((120, 160, 120, 230))
        self.linie3.append((120, 160, 200, 160))
        self.linie3.append((100, 140,220, 140))
        self.linie3.append((200, 160, 200, 250))
        self.linie3.append((220, 140, 220, 230))
        self.linie3.append((220, 230, 270, 230))
        self.linie3.append((200, 250, 290, 250))
        self.linie3.append((270, 120, 270, 230))
        self.linie3.append((290, 140, 290, 250))
        self.linie3.append((270, 120, 330, 120))
        self.linie3.append((290, 140, 350, 140))
        self.linie3.append((330, 0, 330, 120))
        self.linie3.append((350, 110, 350, 140))
        self.linie3.append((350, 0, 350, 95))
        self.linie3.append((80, 300, 430, 300))
        self.linie3.append((60, 315, 445, 315))
        self.linie3.append((430, 110, 430, 300))
        self.linie3.append((445, 95, 445, 315))
        self.linie3.append((350, 110, 430, 110))
        self.linie3.append((350, 95, 445, 95))

        self.linie4.append((10,270,10,320))
        self.linie4.append((30,300,30,320))
        self.linie4.append((30, 300, 70, 300))
        self.linie4.append((10, 270, 70, 270))
        self.linie4.append((70, 290, 70, 300))
        self.linie4.append((70, 270, 70, 280))
        self.linie4.append((70, 280, 100, 280))
        self.linie4.append((70, 290, 100, 290))
        self.linie4.append((100, 270, 100, 280))
        self.linie4.append((100, 290, 100, 300))
        self.linie4.append((100, 270, 130, 270))
        self.linie4.append((100, 300, 160, 300))
        self.linie4.append((160, 160, 160, 300))
        self.linie4.append((130, 210, 130, 270))
        self.linie4.append((130, 210, 140, 210))
        self.linie4.append((140, 180, 140, 210))
        self.linie4.append((50, 180, 140, 180))
        self.linie4.append((65, 160, 160, 160))
        self.linie4.append((65, 100, 65, 160))
        self.linie4.append((50, 80, 50, 180))
        self.linie4.append((50, 80, 220, 80))
        self.linie4.append((65, 100, 205, 100))
        self.linie4.append((220, 80, 220, 260))
        self.linie4.append((205, 100, 205, 280))
        self.linie4.append((220, 260, 300, 260))
        self.linie4.append((205, 280, 280, 280))
        self.linie4.append((280, 280, 280, 300))
        self.linie4.append((300, 260, 300, 285))
        self.linie4.append((300, 285, 350, 285))
        self.linie4.append((280, 300, 365, 300))
        self.linie4.append((365, 160, 365, 300))
        self.linie4.append((350, 150, 350, 285))
        self.linie4.append((10, 270, 10, 320))
        self.linie4.append((365, 160, 440, 160))
        self.linie4.append((350, 150, 430, 150))
        self.linie4.append((430, 70, 430, 150))
        self.linie4.append((440, 50, 440, 160))
        self.linie4.append((390, 50, 440, 50))
        self.linie4.append((410, 70, 430, 70))
        self.linie4.append((410, 70, 410, 120))
        self.linie4.append((390, 50, 390, 105))
        self.linie4.append((330, 120, 410, 120))
        self.linie4.append((345, 105, 390, 105))
        self.linie4.append((330, 0, 330, 120))
        self.linie4.append((345, 40, 345, 105))
        self.linie4.append((345, 40, 350, 40))
        self.linie4.append((350, 0, 350, 40))

        self.linie5.append((10, 260, 10, 320))
        self.linie5.append((30, 280, 30, 320))
        self.linie5.append((30, 280, 70, 280))
        self.linie5.append((10, 260, 90, 260))
        self.linie5.append((90, 260, 90, 290))
        self.linie5.append((70, 280, 70, 310))
        self.linie5.append((90, 290, 105, 290))
        self.linie5.append((70, 310, 120, 310))
        self.linie5.append((105, 150, 105, 290))
        self.linie5.append((120, 170, 120, 310))
        self.linie5.append((105, 150, 150, 150))
        self.linie5.append((120, 170, 150, 170))
        self.linie5.append((155, 150, 220, 150))
        self.linie5.append((155, 170, 205, 170))
        self.linie5.append((205, 170, 205, 260))
        self.linie5.append((220, 150, 220, 245))
        self.linie5.append((220, 245, 270, 245))
        self.linie5.append((205, 260, 290, 260))
        self.linie5.append((270, 190, 270, 245))
        self.linie5.append((290, 210, 290, 260))
        self.linie5.append((270, 190, 380, 190))
        self.linie5.append((290, 210, 360, 210))
        self.linie5.append((360, 210, 360, 300))
        self.linie5.append((380, 190, 380, 280))
        self.linie5.append((380, 280, 435, 280))
        self.linie5.append((360, 300, 450, 300))
        self.linie5.append((435, 160, 435, 280))
        self.linie5.append((450, 140, 450, 300))
        self.linie5.append((320, 140, 450, 140))
        self.linie5.append((300, 160, 435, 160))
        self.linie5.append((300, 55, 300, 160))
        self.linie5.append((320, 70, 320, 140))
        self.linie5.append((300, 55, 420, 55))
        self.linie5.append((320, 70, 440, 70))
        self.linie5.append((420, 30, 420, 55))
        self.linie5.append((440, 10, 440, 70))
        self.linie5.append((350, 10, 440, 10))
        self.linie5.append((330, 30, 420, 30))
        self.linie5.append((330, 0, 330, 30))
        self.linie5.append((350, 0, 350, 10))

        self.linie51.append((152, 140, 152, 180))


    def set_color(self,new_color):
        self.color_=new_color
    def draw_level_1(self):
     for block in self.linie:
         pygame.draw.line(self.screen_,self.color_,(block[0],block[1]),(block[2],block[3]),self.width_)
    def draw_level_2(self):
     for block in self.linie2:
         pygame.draw.line(self.screen_,self.color_,(block[0],block[1]),(block[2],block[3]),self.width_)
    def draw_level_3(self):
     for block in self.linie3:
         pygame.draw.line(self.screen_,self.color_,(block[0],block[1]),(block[2],block[3]),self.width_)
    def draw_level_4(self):
     for block in self.linie4:
         pygame.draw.line(self.screen_,self.color_,(block[0],block[1]),(block[2],block[3]),self.width_)
    def draw_level_5(self):
     for block in self.linie5:
         pygame.draw.line(self.screen_,self.color_,(block[0],block[1]),(block[2],block[3]),self.width_)


    def move(self):
        if self.yg_<320:
            self.yg_ = self.yg_ + self.vy_
            self.yd_ = self.yd_ + self.vy_
            self.linie51=[]
            self.linie51.append((152,self.yg_,152,self.yd_))
            pygame.draw.line(self.screen_, self.color_, (152, self.yg_), (152, self.yd_), self.width_)
        else:
            self.yg_=-41
            self.yd_=0





