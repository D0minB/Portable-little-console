import pygame
from random import randrange
import time
class Shield(pygame.sprite.Sprite):

    def __init__(self,screen):

        self.image_= pygame.image.load("shield.png").convert()
        self.screen_=screen
        self.rect_=self.image_.get_rect()
        self.x_ =randrange(230, 250, 1)
        self.y_ =randrange(150, 170, 1)

    def draw(self):
        self.screen_.blit(self.image_, self.rect_)
        self.rect_.center = [self.x_, self.y_]

    def move(self, dx, dy,player):
        if self.x_ + dx - 3 > -16 and self.x_ + dx + 3 < 496 and self.y_ + dy > -16 and self.y_ + dy < 336:
            self.x_ += dx
            self.y_ += dy
        else:
            # self.x_ += dx
            # self.y_ += dy
            self.x_ = randrange(20, 460, 1)
            self.y_ = randrange(20, 300, 1)
            player.zycia_-=1


    def kolizja(self,player):
        if pygame.Rect(player.x_,player.y_,6,6).colliderect(
                pygame.Rect(self.x_-16,self.y_-16,32,32)) == True and  pygame.key.get_pressed()[pygame.K_SPACE]:
            return True