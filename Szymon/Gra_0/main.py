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
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        dx=0
        dx -= 4
        player.move(dx,0)
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        dx=0
        dx += 4
        player.move(dx,0)
    if pygame.key.get_pressed()[pygame.K_UP]:
        dy=0
        dy -= 4
        player.move(0,dy)
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        dy=0
        dy += 4
        player.move(0,dy)
    player.draw()
    pygame.display.update()
    pygame.display.flip()

pygame.quit()