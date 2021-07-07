import pygame
import time
import pygame, sys
from  Shield import Shield
from random import randrange
from  Player import Player
class Game():
    def napisy_sterowanie(self,screen, font_style):
        text_wylacz = font_style.render("Wciśnij q żeby zamknąć gre", True, (0, 0, 0))
        text_wlacz = font_style.render("Wciśnij r żeby zagrac jeszcze raz", True, (0, 0, 0))
        screen.blit(text_wylacz, [screen.get_width() / 2 - 140, screen.get_height() / 2 + 10])
        screen.blit(text_wlacz, [screen.get_width() / 2 - 150, screen.get_height() / 2 + 30])

    def sterowanie_oknem(self,player):
        if pygame.key.get_pressed()[pygame.K_q]:
            pygame.quit()
            sys.exit()
        if pygame.key.get_pressed()[pygame.K_r]:
            player.zycia_ = 3
            player.punkty_ = 0
            player.x_ = 240
            player.y_ = 160

    def __init__(self):
        pygame.init()

        clock = pygame.time.Clock()

        fps = 10.0
        dx = 0
        dy = 0
        dt = 0
        size = [480, 320]
        screen = pygame.display.set_mode(size)
        player = Player(screen)
        shield = Shield(screen)

        font_style = pygame.font.SysFont("dejavuserif", 20)
        font_style2 = pygame.font.SysFont("dejavuserif", 60)
        running = True
        while running:
            dt += clock.tick() / 1000.0
            while dt > 1 / fps:
                dt -= 1 / fps

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                if player.zycia_ > 0:
                    vx = 3 * randrange(-1, 1, 2)
                    vy = 3 * randrange(-1, 1, 2)

                    screen.fill((0, 0, 0))
                    player.sterowanie(dx, dy)

                    shield.draw()
                    player.draw()
                    shield.move(vx, vy, player)
                    player.napisy(screen, font_style)
                    if shield.kolizja(player) == True:
                        shield.x_ = randrange(20, 460, 1)
                        shield.y_ = randrange(20, 300, 1)
                        player.punkty_ += 1
                    if player.punkty_ >= 8:
                        vx = 0
                        vy = 0
                        screen.fill((0, 255, 127))
                        text_win = font_style2.render("Wygrana!", True, (0, 0, 0))
                        self.napisy_sterowanie(screen, font_style)
                        screen.blit(text_win, [screen.get_width() / 2 - 120, screen.get_height() / 2 - 50])
                        self.sterowanie_oknem(player)
                if player.zycia_ <= 0:
                    screen.fill((255, 0, 0))
                    text_koniec = font_style2.render("Porażka!", True, (0, 0, 0))
                    screen.blit(text_koniec, [screen.get_width() / 2 - 120, screen.get_height() / 2 - 50])
                    self.napisy_sterowanie(screen, font_style)
                    self.sterowanie_oknem(player)

                pygame.display.update()
                pygame.display.flip()

        pygame.quit()