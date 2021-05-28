import pygame
import time
from Maze import Maze
from  Player import Player

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([480, 320])
player=Player(screen)
maze=Maze(screen,width=2,color=(255, 0, 255))
maze.set_color((255,255,0))
fps = 10.0
dx=0
dy=0
dt=0
dlugosc=0
szerokosc=0

running = True
while running:
 dt += clock.tick() / 1000.0
 while dt > 1 / fps:
    dt -= 1 / fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    maze.draw_level_1()

    dx=0
    dy=0
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        dx -= 4
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        dx += 4
    if pygame.key.get_pressed()[pygame.K_UP]:
        dy -= 4
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        dy += 4
    player.move(dx,dy)
    for linia in maze.linie:
        if linia[0]==linia[2]:
            dlugosc=abs(linia[3]-linia[1])
            szerokosc=2
        if linia[1]==linia[3]:
            szerokosc=abs(linia[2]-linia[0])
            dlugosc=2
        if pygame.Rect(player.x_, player.y_, 6, 6).colliderect(pygame.Rect(linia[0], linia[1], szerokosc, dlugosc)) == True:
            player.x_=16
            player.y_=310


    player.draw()
    pygame.display.update()
    pygame.display.flip()

pygame.quit()