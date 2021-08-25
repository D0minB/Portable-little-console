import pygame
from random import randrange
class Shield(pygame.sprite.Sprite):
    def __init__(self,screen):
        self.image_= pygame.image.load("bird.png")
        self.screen_=screen
        self.rect_=self.image_.get_rect()
        self.x_ =-20
        self.y_ =randrange(70, 270, 1)
        self.dx_=11
        self.dy_=0
        self.szerokosc_=self.image_.get_width()
        self.wysokosc_=self.image_.get_height()

    def draw(self):
        self.screen_.blit(self.image_, self.rect_)
        self.rect_.center = [self.x_, self.y_]

    def move(self,player):
        if  self.x_ + self.dx_ + 3 < self.screen_.get_width()+self.szerokosc_/2:# and self.y_ + self.dy_ < 336:
            self.x_ += self.dx_
            self.y_ += self.dy_
        else:
            self.x_ = -20
            self.y_ =randrange(70, 270, 1)
            player.zycia_-=1

    def kolizja(self,player):
        if pygame.Rect(player.x_,player.y_,player.szerokosc_,player.wysokosc_).colliderect(
                pygame.Rect(self.x_-self.szerokosc_/2,self.y_-self.wysokosc_/2,self.szerokosc_,self.wysokosc_)) == True and  pygame.key.get_pressed()[pygame.K_SPACE]:
            return True