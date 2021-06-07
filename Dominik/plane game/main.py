# PLANE GAME
# AUTHOR: DOMINIK BOGIELCZYK

import pygame
from pygame.math import Vector2
import time
import sys
import random
import RPi.GPIO as GPIO
from plane_class import Plane
from MCP3008_class import MCP3008

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.IN,pull_up_down=GPIO.PUD_UP)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Portable little console')
pygame.mouse.set_visible(0)

font70 = pygame.font.SysFont("bahnschrift", 70)
font40 = pygame.font.SysFont("bahnschrift", 40)
font20 = pygame.font.SysFont("bahnschrift", 20)

def write_text(font,text,color,pos):
    text = font.render(text, True, color)
    screen.blit(text, text.get_rect(center=(pos.x, pos.y)))


def plane_game():
# NEW TARGETS GENERATING
    def targets_generating():
        new_targets_pos = []
        for i in range(random.randint(4, 7)):  # 6 TO 12 - NUMBER OF THE NEW TARGETS
            n = random.randint(1, 14) #new target position choosing

            while n in new_targets_pos:  # ADD UNIQUE POSITION OF THE TARGET
                n = random.randint(1, 14)

            new_targets_pos.append(n)

        for target_pos in new_targets_pos:  # ADD UNIQUE TARGETS POSITIONS TO LIST
            targets.append(Vector2(target_pos * 22 + 8, 8))

        return targets
        
    dt = 0.0
    fps = 20.0
    clock = pygame.time.Clock()

    adc = MCP3008()

    plane = Plane(screen)
    targets = []
    bullets=[]

    points=0
    
    n=0

    last_targets_time = time.time()
    new_targets_time=2.5

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
            if pygame.key.get_pressed()[pygame.K_LEFT] or adc.read(channel=2)<=50:
                delta_x -= 200/fps
            if pygame.key.get_pressed()[pygame.K_RIGHT] or adc.read(channel=2)>=700:
                delta_x += 200/fps
            plane.move(delta_x)

            if n>=2:
                n=0
            else:
                n+=1

            #bullet every 3 frames
            if n==2 and (GPIO.input(37) == 0 or pygame.key.get_pressed()[pygame.K_SPACE]):
                bullets.append(Vector2(plane.get_position()[0] + 10, plane.get_position()[1] - 10))

            #bullets move in y-axis
            for bullet in bullets:
                bullet.y-=150/fps

            # new targets every 3 seconds
            if time.time() - last_targets_time > new_targets_time:
                last_targets_time = time.time()
                new_targets_time=0.95*new_targets_time

                # previous targets move in y-axis
                for target in targets:
                    target.y += 22

                # generate new targets
                targets_generating()

            targets_copy=targets
            bullets_copy=bullets

            #collision - target and bullet
            for target in targets_copy:
                for bullet in bullets_copy:
                    if pygame.Rect(target.x,target.y,20,20).colliderect(pygame.Rect(bullet.x-5,bullet.y-5,10,10)):
                        targets.remove(target)
                        bullets.remove(bullet)
                        points+=1

            #remove out of screen bullets
            for bullet in bullets_copy:
                if bullet.x<15:
                    bullets.remove(bullet)

            

            # cleaning screen
            screen.fill((0, 0, 0))

            plane.draw()

            #frame
            pygame.draw.line(screen, (255, 255, 255), (2, 2), (16*22 + 8, 2), 4)
            pygame.draw.line(screen, (255, 255, 255), (2, screen.get_height()-2), (16 * 22 + 8, screen.get_height()-2), 4)
            pygame.draw.line(screen, (255, 255, 255), (2, 2), (2, screen.get_height()-2), 4)
            pygame.draw.line(screen,(255,255,255),(16*22 + 8,2),(16*22 + 8,screen.get_height()-2),4)

            for target in targets:
                pygame.draw.rect(screen, (255, 255, 0),pygame.Rect(target.x,target.y,20,20))

            for bullet in bullets:
                pygame.draw.circle(screen, (255, 20, 0),[int(bullet.x),int(bullet.y)],5)

            write_text(font70,str(points),(0, 0, 255),Vector2(screen.get_width() -50, screen.get_height()/2))
            write_text(font20,"points",(0, 0, 255),Vector2(screen.get_width() - 50, screen.get_height() / 2 +50))

            plane_position=plane.get_position()
            
            #end screen
            if len(targets)>0 and targets[0].y > plane_position.y-15:
                screen.fill((0, 0, 0))
                write_text(font40,"Your score:",(255, 0, 0),Vector2(screen.get_width()/2, 75))
                write_text(font70,str(points),(255, 0, 0),Vector2(screen.get_width()/2, 150))
                write_text(font20,"Joystick left to quit or right to new game",(255, 255, 255),Vector2(screen.get_width()/2, 220))
                pygame.display.update()

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or adc.read(channel=2)<=50:
                            pygame.quit()
                            sys.exit()
                        if adc.read(channel=2)>=700:
                            plane_game()

            pygame.display.flip()


plane_game()


