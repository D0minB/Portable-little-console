import pygame
import time
import sys
from Maze import Maze
from  Player import Player

def napisy_sterowanie(screen,font_style):
    text_wylacz = font_style.render("Wciśnij q żeby zamknąć gre", True, (0, 0, 0))
    text_wlacz = font_style.render("Wciśnij r żeby zagrac jeszcze raz", True, (0, 0, 0))
    screen.blit(text_wylacz, [screen.get_width() / 2 - 140, screen.get_height() / 2 + 10])
    screen.blit(text_wlacz, [screen.get_width() / 2 - 150, screen.get_height() / 2 + 30])
def sterowanie_oknem(player):
    if pygame.key.get_pressed()[pygame.K_q]:
        pygame.quit()
        sys.exit()
    if pygame.key.get_pressed()[pygame.K_r]:
        player.zycia = 3
        player.poziom = 1

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode([480, 320])
player=Player(screen)
maze=Maze(screen,width=2)
fps = 10.0
dx=0
dy=0
dt=0

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


    if player.zycia>0:

        if player.poziom==1:
            player.sterowanie(dx, dy)
            screen.fill((0, 0, 0))
            maze.set_color((255, 255, 0))
            maze.draw_level_1()
            player.kolizje(maze.linie)
            player.win(screen)
            player.napisy(screen, font_style)
            player.draw()

        if player.poziom == 2:
                player.sterowanie(dx,dy)
                screen.fill((0, 0, 0))
                maze.set_color((0 ,255, 255))
                maze.draw_level_2()
                player.kolizje(maze.linie2)
                player.win(screen)
                player.napisy(screen, font_style)
                player.draw()

        if player.poziom>2:
            screen.fill((0 ,255, 127))
            text_win = font_style2.render("Wygrana!", True, (0, 0, 0))
            napisy_sterowanie(screen, font_style)
            screen.blit(text_win, [screen.get_width() / 2 - 120, screen.get_height() / 2 - 50])
            sterowanie_oknem(player)


    if player.zycia<=0:
        screen.fill((255, 0, 0))
        text_koniec = font_style2.render("Porażka!", True, (0, 0, 0))
        screen.blit(text_koniec, [screen.get_width()/2-120,screen.get_height()/2-50])
        napisy_sterowanie(screen, font_style)
        sterowanie_oknem(player)

    pygame.display.update()
    pygame.display.flip()

pygame.quit()