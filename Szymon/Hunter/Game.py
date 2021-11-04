import pygame, sys
from  Shield import Shield
from random import randrange
from  Player import Player
from Heart import Heart
import RPi.GPIO as GPIO
from MCP3008_class import MCP3008
adc = MCP3008()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33,GPIO.IN,pull_up_down=GPIO.PUD_UP) #prawy
GPIO.setup(32,GPIO.IN,pull_up_down=GPIO.PUD_UP) #lewy
class Game():
    def zmiany_v(self,player,shield):
        if player.punkty_==1 or player.punkty_==2 or player.punkty_==0:
            shield.dx_=9
        else:
                if player.punkty_==3 or player.punkty_==4:
                    shield.dx_=11
                else:
                    if player.punkty_==5:
                        shield.dx_=13
                    else:
                        if player.punkty_==6:
                            shield.dx_=15
                        else:
                            if player.punkty_==7:
                                shield.dx_=16
                            else:
                                if player.punkty_==8 or player.punkty_==9:
                                    shield.dx_=17
                                else:
                                    shield.dx_=player.punkty_+8


    def sterowanie_oknem(self,player,shield):
        if pygame.key.get_pressed()[pygame.K_q]or GPIO.input(33) == 0:
            pygame.quit()
            sys.exit()
        if pygame.key.get_pressed()[pygame.K_r]or GPIO.input(32) == 0:
            player.counter_a = 1
            player.zycia_ = 3
            player.punkty_ = 0
            player.x_ = 240
            player.y_ = 160
            shield.dx_ = 11
            shield.dy_ = 0
            shield.x_ = -20
            shield.y_ = randrange(70, 270, 1)

    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()
        fps = 10.0
        dx = 0
        dy = 0
        dt = 0
        font_style = pygame.font.SysFont("dejavuserif", 20)
        font_style2 = pygame.font.SysFont("dejavuserif", 20)
        size_szerokosc = 480
        size_wysokosc=320
        size=[size_szerokosc,size_wysokosc]
        screen = pygame.display.set_mode(size)
        player = Player(screen)
        shield = Shield(screen)
        heart=Heart(screen)
        tlo_a= pygame.sprite.Sprite()
        tlo_a.image = pygame.image.load("tlo_a.png").convert()
        tlo_a.rect = tlo_a.image.get_rect()
        tlo_menu = pygame.sprite.Sprite()
        tlo_menu.image = pygame.image.load("menu.png").convert()
        tlo_menu.rect = tlo_menu.image.get_rect()
        tlo_porazka = pygame.sprite.Sprite()
        tlo_porazka.image = pygame.image.load("tlo_porazka.png").convert()
        tlo_porazka.rect = tlo_porazka.image.get_rect()
        running = True
        while running:
            dt += clock.tick() / 1000.0
            while dt > 1 / fps:
                dt -= 1 / fps

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                if player.counter_a==0:
                    screen.blit(tlo_menu.image, tlo_menu.rect)
                    pygame.display.flip()
                if pygame.key.get_pressed()[pygame.K_r]or GPIO.input(32) == 0 or player.counter_a==1:
                    player.counter_a=1
                    if player.zycia_ > 0:
                        screen.blit(tlo_a.image, tlo_a.rect)
                        player.sterowanie(dx, dy)
                        shield.draw()
                        player.draw()
                        self.zmiany_v(player, shield)
                        shield.move(player)
                        player.napisy(screen, font_style)
                        if player.punkty_>=6 and player.zycia_<2:
                            heart.kolizja(player)
                            heart.draw()
                            heart.move(player)
                        if shield.kolizja(player) == True:
                            shield.x_ = -20
                            shield.y_ = randrange(70, 270, 1)
                            shield.dy_ =0
                            player.punkty_ += 1
                    if player.zycia_ <= 0:
                        screen.blit(tlo_porazka.image, tlo_porazka.rect)
                        text_zycia = font_style2.render(str(player.punkty_), True, (255, 255, 0))
                        screen.blit(text_zycia, [230, 135])
                        self.sterowanie_oknem(player,shield)
                    pygame.display.update()
        pygame.quit()