import time
import pygame, sys
from  Player import Player


pygame.init()

clock = pygame.time.Clock()

fps = 10.0
dx = 0
dy = 0
dt = 0
size = [480, 320]
screen = pygame.display.set_mode(size)
player=Player(screen)


running = True
while running:
    dt += clock.tick() / 1000.0
    while dt > 1 / fps:
        dt -= 1 / fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        player.sterowanie(dx,dy)
        player.draw()


        pygame.display.update()
        pygame.display.flip()

pygame.quit()