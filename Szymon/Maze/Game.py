import pygame
import time
import sys
from Maze import Maze
from  Player import Player
from MCP3008_class import MCP3008
import RPi.GPIO as GPIO
adc = MCP3008()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33,GPIO.IN,pull_up_down=GPIO.PUD_UP) #prawy
GPIO.setup(32,GPIO.IN,pull_up_down=GPIO.PUD_UP) #lewy
class Game():


    def sterowanie_oknem(self,player):
        if pygame.key.get_pressed()[pygame.K_q] or GPIO.input(33) == 0:
            pygame.quit()
            sys.exit()
        if pygame.key.get_pressed()[pygame.K_r] or GPIO.input(32) == 0:
            player.zycia = 3
            player.poziom = 1

    def __init__(self):
        pygame.init()

        clock = pygame.time.Clock()

        screen = pygame.display.set_mode([480, 320])
        player = Player(screen)
        maze = Maze(screen, width=2)
        fps = 10.0
        dx = 0
        dy = 0
        dt = 0
        tlo_menu = pygame.sprite.Sprite()
        tlo_menu.image = pygame.image.load("menu.png").convert()
        tlo_menu.rect = tlo_menu.image.get_rect()
        tlo_wygrana = pygame.sprite.Sprite()
        tlo_wygrana.image = pygame.image.load("tlo_wygrana.png").convert()
        tlo_wygrana.rect = tlo_wygrana.image.get_rect()
        tlo_porazka = pygame.sprite.Sprite()
        tlo_porazka.image = pygame.image.load("tlo_porazka.png").convert()
        tlo_porazka.rect = tlo_porazka.image.get_rect()

        font_style = pygame.font.SysFont("dejavuserif", 20)

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
                if pygame.key.get_pressed()[pygame.K_r] or GPIO.input(32) == 0 or player.counter_a==1:
                    player.counter_a=1
                    if player.zycia > 0:

                        if player.poziom == 1:
                            player.sterowanie(dx, dy)
                            player.color_ = (255, 69, 0)
                            screen.fill((0, 0, 0))
                            maze.set_color((255, 255, 0))
                            maze.draw_level_1()
                            player.kolizje(maze.linie)
                            player.win(screen)
                            player.napisy(screen, font_style)
                            player.draw()

                        if player.poziom == 2:
                            player.sterowanie(dx, dy)
                            player.color_ = (255, 69, 0)
                            screen.fill((0, 0, 0))
                            maze.set_color((0, 255, 255))
                            maze.draw_level_2()
                            player.kolizje(maze.linie2)
                            player.win(screen)
                            player.napisy(screen, font_style)
                            player.draw()
                        if player.poziom == 3:
                            player.sterowanie(dx, dy)
                            player.color_ = (255, 69, 0)
                            screen.fill((0, 0, 0))
                            maze.set_color((0, 255, 0))
                            maze.draw_level_3()
                            player.kolizje(maze.linie3)
                            player.win(screen)
                            player.napisy(screen, font_style)
                            player.draw()
                        if player.poziom == 4:
                            player.sterowanie(dx, dy)
                            screen.fill((0, 0, 0))
                            player.color_=	(0, 255, 255)
                            maze.set_color((255, 0, 0))
                            maze.draw_level_4()
                            player.kolizje(maze.linie4)
                            player.win(screen)
                            player.napisy(screen, font_style)
                            player.draw()
                        if player.poziom == 5:
                            player.sterowanie(dx, dy)
                            screen.fill((0, 0, 0))
                            player.color_=(0, 255, 255)
                            maze.set_color((255, 165, 0))
                            maze.draw_level_5()
                            maze.move()
                            player.kolizje(maze.linie51)
                            player.kolizje(maze.linie5)
                            player.win(screen)
                            player.napisy(screen, font_style)
                            player.draw()

                        if player.poziom > 5:
                            screen.blit(tlo_wygrana.image, tlo_wygrana.rect)
                            self.sterowanie_oknem(player)

                    if player.zycia <= 0:
                        screen.blit(tlo_porazka.image, tlo_porazka.rect)
                        self.sterowanie_oknem(player)

                    pygame.display.update()


        pygame.quit()