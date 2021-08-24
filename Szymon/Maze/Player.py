import pygame
import time
class Player(pygame.Rect):

    def __init__(self,screen):
        self.x_=16
        self.y_=310
        self.screen_=screen
        self.zycia=3
        self.poziom=1
        self.width_=6
        self.height_=6





    def draw(self):
            pygame.draw.rect(self.screen_, (255, 69, 0), pygame.Rect(self.x_,self.y_,self.width_,self.height_))

    def move(self,dx,dy):
        if self.x_+dx-self.width_/2>0 and self.x_+ dx+self.width_/2 < 475 and self.y_+dy>0 and self.y_+dy<320-self.height_/2:
                self.x_+=dx
                self.y_+=dy

    def sterowanie(self,dx,dy):
        dx = 0
        dy = 0
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            dx -= 4
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            dx += 4
        if pygame.key.get_pressed()[pygame.K_UP]:
            dy -= 4
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            dy += 4
        self.move(dx, dy)

    def kolizje(self, linie):
        for linia in linie:
            if linia[0] == linia[2]:
                dlugosc = abs(linia[3] - linia[1])
                szerokosc = 2
            if linia[1] == linia[3]:
                szerokosc = abs(linia[2] - linia[0])
                dlugosc = 2
            if pygame.Rect(self.x_, self.y_, self.width_, self.height_).colliderect(
                    pygame.Rect(linia[0], linia[1], szerokosc, dlugosc)) == True:
                self.x_ = 16
                self.y_ = 310
                self.zycia -= 1

    def win(self,screen):
        pygame.draw.rect(screen, (255, 255, 255), [332, 0, 18, 10])
        if pygame.Rect(self.x_, self.y_, self.width_, self.height_).colliderect(pygame.Rect(332, 0, 18, 10)) == True:
            self.x_ = 16
            self.y_ = 310
            self.poziom += 1

    def napisy(self,screen,font_style):
        text_zycia = font_style.render("Życia: " + str(self.zycia), True, (255, 0, 0))
        screen.blit(text_zycia, [0, 0])
        text_zycia = font_style.render("Poziom: " + str(self.poziom), True, (255, 0, 0))
        screen.blit(text_zycia, [0, 20])