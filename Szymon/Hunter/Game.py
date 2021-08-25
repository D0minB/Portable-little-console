import pygame, sys
from  Shield import Shield
from random import randrange
from  Player import Player
from Heart import Heart
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

    def napisy_sterowanie(self,screen, text_wylacz,text_wlacz):
        screen.blit(text_wylacz, [screen.get_width() / 2 - 140, screen.get_height() / 2 + 10])
        screen.blit(text_wlacz, [screen.get_width() / 2 - 150, screen.get_height() / 2 + 30])
    def napisy_sterowanie_2(self,screen, text_a,text_b):
        screen.blit(text_a, [screen.get_width() / 2 - 140, screen.get_height() / 2 + 10])
        screen.blit(text_b, [screen.get_width() / 2 - 150, screen.get_height() / 2 + 30])

    def sterowanie_oknem(self,player,shield):
        if pygame.key.get_pressed()[pygame.K_q]:
            pygame.quit()
            sys.exit()
        if pygame.key.get_pressed()[pygame.K_r]:
            player.counter_a = 0
            player.zycia_ = 3
            player.punkty_ = 0
            player.x_ = 240
            player.y_ = 160
            shield.dx_ = 11
            shield.dy_ = 0

    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()
        fps = 10.0
        dx = 0
        dy = 0
        dt = 0
        font_style = pygame.font.SysFont("dejavuserif", 20)
        font_style2 = pygame.font.SysFont("dejavuserif", 60)
        text_wylacz = font_style.render("Wciśnij q żeby zamknąć gre", True, (0, 0, 0))
        text_wlacz = font_style.render("Wciśnij r żeby zagrac jeszcze raz", True, (0, 0, 0))
        text_a = font_style.render("Wciśnij a żeby grać o rekord", True, (0, 0, 0))
        text_b = font_style.render("Wciśnij b żeby grać do 13 punktów", True, (0, 0, 0))
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
        tlo_b = pygame.sprite.Sprite()
        tlo_b.image = pygame.image.load("tlo_b.png").convert()
        tlo_b.rect = tlo_b.image.get_rect()
        running = True
        while running:
            dt += clock.tick() / 1000.0
            while dt > 1 / fps:
                dt -= 1 / fps

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                if player.counter_a==0:
                    screen.fill((186, 85, 211))
                    self.napisy_sterowanie_2(screen, text_a,text_b)
                    pygame.display.update()
                    pygame.display.flip()
                if pygame.key.get_pressed()[pygame.K_a] or player.counter_a==1:
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
                        screen.fill((255, 0, 0))
                        text_koniec = font_style2.render("Porażka!", True, (0, 0, 0))
                        screen.blit(text_koniec, [screen.get_width() / 2 - 120, screen.get_height() / 2 - 50])
                        self.napisy_sterowanie(screen, text_wylacz,text_wlacz)
                        self.sterowanie_oknem(player,shield)
                    pygame.display.update()
                    print([shield.dx_, player.punkty_])
                if pygame.key.get_pressed()[pygame.K_b] or player.counter_a==2:
                    player.counter_a=2
                    if player.zycia_ > 0:
                        screen.blit(tlo_b.image, tlo_b.rect)
                        player.sterowanie(dx, dy)
                        shield.draw()
                        player.draw()
                        self.zmiany_v(player, shield)
                        shield.move(player)
                        player.napisy(screen, font_style)
                        if shield.kolizja(player) == True:
                            shield.x_ = -20
                            shield.y_ = randrange(70, 270, 1)
                            shield.dy_ = 0
                            player.punkty_ += 1
                        if player.punkty_>=6 and player.zycia_<2:
                            heart.kolizja(player)
                            heart.draw()
                            heart.move(player)
                        if player.punkty_ >= 13:
                             shield.dx_ = 0
                             shield.dy_ = 0
                             screen.fill((0, 255, 127))
                             text_win = font_style2.render("Wygrana!", True, (0, 0, 0))
                             self.napisy_sterowanie(screen, text_wylacz,text_wlacz)
                             screen.blit(text_win, [screen.get_width() / 2 - 120, screen.get_height() / 2 - 50])
                             self.sterowanie_oknem(player,shield)
                    if player.zycia_ <= 0:
                        screen.fill((255, 0, 0))
                        text_koniec = font_style2.render("Porażka!", True, (0, 0, 0))
                        screen.blit(text_koniec, [screen.get_width() / 2 - 120, screen.get_height() / 2 - 50])
                        self.napisy_sterowanie(screen, text_wylacz,text_wlacz)
                        self.sterowanie_oknem(player,shield)
                    pygame.display.update()
                    print([shield.dx_,player.punkty_])
        pygame.quit()