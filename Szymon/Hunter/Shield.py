import pygame
from random import randrange
import time

class Shield(pygame.sprite.Sprite):

    def __init__(self,screen):

        self.image_= pygame.image.load("a.png")
        self.screen_=screen
        self.rect_=self.image_.get_rect()
        self.x_ =randrange(200, 300, 1)
        self.y_ =randrange(120, 200, 1)
        self.dx_=3 * randrange(-1, 1, 2)
        self.dy_=3 * randrange(-1, 1, 2)



    def draw(self):
        self.screen_.blit(self.image_, self.rect_)
        self.rect_.center = [self.x_, self.y_]

    def move(self,player):
        if self.x_ + self.dx_ - 3 > -16 and self.x_ + self.dx_ + 3 < 496 and self.y_ + self.dy_ > -16 and self.y_ + self.dy_ < 336:
            self.x_ += self.dx_
            self.y_ += self.dy_
        else:
            self.x_ = randrange(200, 300, 1)
            self.y_ =randrange(120, 200, 1)
            player.zycia_-=1


    def kolizja(self,player):
        if pygame.Rect(player.x_,player.y_,6,6).colliderect(
                pygame.Rect(self.x_-16,self.y_-16,32,32)) == True and  pygame.key.get_pressed()[pygame.K_SPACE]:
            return True