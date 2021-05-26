# PLANE GAME
# AUTHOR: DOMINIK BOGIELCZYK

import pygame
import sys
import time
import random
import numpy as np
from plane_class import Plane

pygame.init()
screen = pygame.display.set_mode((480, 255))
pygame.display.set_caption('Portable little console')
pygame.display.set_icon(pygame.image.load('logo.png'))

font_style = pygame.font.SysFont("bahnschrift", 40)
font_small = pygame.font.SysFont("bahnschrift", 15)

def plane_game():
    dt = 0.0
    fps = 10.0
    clock = pygame.time.Clock()

    plane = Plane(screen)
    targets = []
    bullets=[]

    points=0


    # NEW TARGETS GENERATING
    def targets_generating():
        new_targets_pos = []
        for i in range(random.randint(4, 7)):  # 6 TO 12 - NUMBER OF THE NEW TARGETS
            n = random.randint(0, 15) #new target position choosing

            while n in new_targets_pos:  # ADD UNIQUE POSITION OF THE TARGET
                n = random.randint(0, 15)

            new_targets_pos.append(n)

        for target_pos in new_targets_pos:  # ADD UNIQUE TARGETS POSITIONS TO LIST
            targets.append([target_pos * 22, 0])

        return targets

    last_targets_time = time.time()
    last_bullet_time=time.time()
    last_bullets_move=time.time()

    # GENERATE FIRST TARGETS
    targets_generating()

    while True:
        dt += clock.tick() / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        while dt > 1 / fps:
            dt -= 1 / fps

            # plane move
            delta_x = 0

            # plane controlling
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                delta_x -= int(150/fps)
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                delta_x += int(150/fps)
            plane.move(delta_x)

            # bullets generating
            if time.time() - last_bullet_time > 0.1:
                last_bullet_time = time.time()

                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    bullets.append([plane.get_position()[0] + 10, plane.get_position()[1] - 10])

            if time.time() - last_bullets_move > 0.02:
                last_bullets_move = time.time()

                #bullets move in y-axis
                for bullet in bullets:
                    bullet[1]-=150/fps

            # new targets every 3 seconds
            if time.time() - last_targets_time > 3.0:
                last_targets_time = time.time()

                # previous targets move in y-axis
                for target in targets:
                    target[1] += 22

                # generate new targets
                targets_generating()

            targets_copy=targets
            bullets_copy=bullets

            for target in targets_copy:
                for bullet in bullets_copy:
                    if pygame.Rect(target[0],target[1],20,20).colliderect(pygame.Rect(bullet[0]-10,bullet[1]-10,10,10)):
                        targets.remove(target)
                        bullets.remove(bullet)
                        points+=1

            #remove bullets and targets out of screen
            for bullet in bullets_copy:
                if bullet[1]<0:
                    bullets.remove(bullet)
            for target in targets_copy:
                if target[1]>screen.get_height():
                    targets.remove(target)

            [x,y]=plane.get_position()

            if len(targets)>0 and targets[0][1] > y:
                screen.fill((0, 0, 0))
                text_end = font_style.render("YOU LOST", True, (255, 0, 0))
                screen.blit(text_end, [480/2 - 75, 256/2 - 100])
                text = font_style.render(str(points), True, (255, 0, 0))
                screen.blit(text, [screen.get_width() / 2 - 25, screen.get_height() - 150])
                text = font_small.render("press q to quit or space to new game", True, (255, 255, 255))
                screen.blit(text, [120, 220])

                pygame.display.update()

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                            pygame.quit()
                            sys.exit()
                        if pygame.key.get_pressed()[pygame.K_SPACE]:
                            plane_game()

            # cleaning screen
            screen.fill((0, 0, 0))

            plane.draw()

            for target in targets:
                pygame.draw.rect(screen, (0, 255, 0),pygame.Rect(target[0],target[1],20,20))

            for bullet in bullets:
                pygame.draw.circle(screen, (255, 0, 0),[int(bullet[0]),int(bullet[1])],5)

            text = font_style.render(str(points), True, (0, 200, 0))
            screen.blit(text, [screen.get_width() -75, screen.get_height()/2])

            pygame.display.flip()


plane_game()


