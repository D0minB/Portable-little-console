import pygame
import time
import sys
from Maze import Maze
from  Player import Player

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([480, 320])
player=Player(screen)
maze=Maze(screen,width=2,color=(255, 0, 255))
fps = 10.0
dx=0
dy=0
dt=0
poziom=1
zycia=3
dlugosc=0
szerokosc=0
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


    if zycia>0:

        if poziom==1:
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
            player.move(dx, dy)
            screen.fill((0, 0, 0))
            maze.set_color((255, 255, 0))
            maze.draw_level_1()
            for linia in maze.linie:
                if linia[0] == linia[2]:
                    dlugosc = abs(linia[3] - linia[1])
                    szerokosc = 2
                if linia[1] == linia[3]:
                    szerokosc = abs(linia[2] - linia[0])
                    dlugosc = 2
                if pygame.Rect(player.x_, player.y_, 6, 6).colliderect(
                        pygame.Rect(linia[0], linia[1], szerokosc, dlugosc)) == True:
                    player.x_ = 16
                    player.y_ = 310
                    zycia -= 1

            pygame.draw.rect(screen, (255, 255, 255), [332, 0,18, 10])
            if pygame.Rect(player.x_, player.y_, 6, 6).colliderect(pygame.Rect(332, 0, 18, 10)) == True:
                player.x_ = 16
                player.y_ = 310
                poziom += 1
            text_zycia = font_style.render("Życia: " + str(zycia), True, (255, 0, 0))
            screen.blit(text_zycia, [0, 0])
            text_zycia = font_style.render("Poziom: " + str(poziom), True, (255, 0, 0))
            screen.blit(text_zycia, [0, 20])
            player.draw()

        if poziom == 2:
                dx = 0
                dy = 0
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    dx -= 5
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    dx += 5
                if pygame.key.get_pressed()[pygame.K_UP]:
                    dy -= 5
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    dy += 5
                player.move(dx, dy)
                screen.fill((255, 228, 225))
                maze.set_color((0 ,139, 139))
                maze.draw_level_2()
                for linia in maze.linie2:
                    if linia[0] == linia[2]:
                        dlugosc = abs(linia[3] - linia[1])
                        szerokosc = 2
                    if linia[1] == linia[3]:
                        szerokosc = abs(linia[2] - linia[0])
                        dlugosc = 2
                    if pygame.Rect(player.x_, player.y_, 6, 6).colliderect(
                            pygame.Rect(linia[0], linia[1], szerokosc, dlugosc)) == True:
                        player.x_ = 16
                        player.y_ = 310
                        zycia -= 1

                pygame.draw.rect(screen, (255, 255, 255), [332, 0, 18, 10])
                if pygame.Rect(player.x_, player.y_, 6, 6).colliderect(pygame.Rect(332, 0, 18, 10)) == True:
                    player.x_ = 16
                    player.y_ = 310
                    poziom += 1
                text_zycia = font_style.render("Życia: " + str(zycia), True, (255, 0, 0))
                screen.blit(text_zycia, [0, 0])
                text_zycia = font_style.render("Poziom: " + str(poziom), True, (255, 0, 0))
                screen.blit(text_zycia, [0, 20])
                player.draw()
        if poziom>2:
            screen.fill((0 ,255, 127))
            text_win = font_style2.render("Wygrana!", True, (0, 0, 0))
            text_wylacz = font_style.render("Wciśnij q żeby zamknąć gre", True, (0, 0, 0))
            text_wlacz = font_style.render("Wciśnij r żeby zagrac jeszcze raz", True, (0, 0, 0))
            screen.blit(text_win, [screen.get_width() / 2 - 120, screen.get_height() / 2 - 50])
            screen.blit(text_wylacz, [screen.get_width() / 2 - 140, screen.get_height() / 2 + 10])
            screen.blit(text_wlacz, [screen.get_width() / 2 - 150, screen.get_height() / 2 + 30])
            if pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_r]:
                zycia = 3
                poziom = 1


    if zycia<=0:
        screen.fill((255, 0, 0))
        text_koniec = font_style2.render("Porażka!", True, (0, 0, 0))
        text_wylacz=font_style.render("Wciśnij q żeby zamknąć gre",True,(0,0,0))
        text_wlacz = font_style.render("Wciśnij r żeby zagrac jeszcze raz", True, (0, 0, 0))
        screen.blit(text_koniec, [screen.get_width()/2-120,screen.get_height()/2-50])
        screen.blit(text_wylacz, [screen.get_width() / 2 - 140, screen.get_height() / 2 +10])
        screen.blit(text_wlacz, [screen.get_width() / 2 - 150, screen.get_height() / 2 + 30])
        if pygame.key.get_pressed()[pygame.K_q]:
            pygame.quit()
            sys.exit()
        if pygame.key.get_pressed()[pygame.K_r]:
            zycia=3
            poziom=1

    pygame.display.update()
    pygame.display.flip()

pygame.quit()