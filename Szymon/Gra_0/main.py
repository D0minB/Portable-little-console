import pygame
pygame.init()
from Maze import Maze

screen = pygame.display.set_mode([480, 255])
maze=Maze(screen,width=2,color=(255, 0, 255))
maze.set_color((255,255,0))

running = True
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    maze.draw_level_1()



    pygame.display.update()
    pygame.display.flip()

pygame.quit()