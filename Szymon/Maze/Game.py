import pygame
import time
import sys
from Maze import Maze
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
                        screen.fill((0, 255, 127))
                        text_win = font_style2.render("Wygrana!", True, (0, 0, 0))
                        self.napisy_sterowanie(screen, font_style)
                        screen.blit(text_win, [screen.get_width() / 2 - 120, screen.get_height() / 2 - 50])
                        self.sterowanie_oknem(player)

                if player.zycia <= 0:
                    screen.fill((255, 0, 0))
                    text_koniec = font_style2.render("Porażka!", True, (0, 0, 0))
                    screen.blit(text_koniec, [screen.get_width() / 2 - 120, screen.get_height() / 2 - 50])
                    self.napisy_sterowanie(screen, font_style)
                    self.sterowanie_oknem(player)

                pygame.display.update()


        pygame.quit()