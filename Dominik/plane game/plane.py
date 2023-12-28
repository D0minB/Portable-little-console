# PLANE GAME
# AUTHOR: DOMINIK BOGIELCZYK

import os
import sys
import time
import random
import concurrent.futures

import pygame
from pygame.math import Vector2
import RPi.GPIO as GPIO
from plane_class import Plane
from MCP3008_class import MCP3008

sys.path.insert(0, '/home/pi/Desktop/main/menu')
import menu

# GPIO config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
CONST_LEFT_SWITCH = 32
CONST_RIGHT_SWITCH = 33
GPIO.setup(CONST_LEFT_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CONST_RIGHT_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Pygame init
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(0)
screen_width = screen.get_width()
screen_height = screen.get_height()

# Fonts init
font15 = pygame.font.SysFont("dejavuserif", 15)
font20 = pygame.font.SysFont("dejavuserif", 20)
font40 = pygame.font.SysFont("dejavuserif", 40)
font50 = pygame.font.SysFont("dejavuserif", 50)

# MCP3008 init
adc = MCP3008()


def draw_text(font, text, color, pos):
    rendered_text = font.render(text, False, color)
    text_rect = rendered_text.get_rect(center=pos)
    screen.blit(rendered_text, text_rect)
    pygame.display.update(text_rect)
    

def start_screen(plane):
    screen.fill((0, 0, 0))
    width = 6
    w = 16 * 22 + 8

    pygame.draw.lines(screen, (255, 255, 255), False,
                      [(width / 2, width / 2), (width / 2, screen_height),
                       (w + width / 2, screen_height), (w + width / 2, width / 2)], width)
    plane.draw()

    draw_text(font40, "PLANE", (255, 255, 255), Vector2((w / 2, 30)))
    draw_text(font20, "STEROWANIE:", (255, 255, 0),
              Vector2(w / 2, screen_height / 2 - 50))
    draw_text(font15, "STRZAŁ - LEWY PRZYCISK", (255, 255, 0),
              Vector2(w / 2, screen_height / 2 - 20))
    draw_text(font15, "RUCH LEWO-PRAWO - LEWY JOYSTICK", (255, 255, 0),
              Vector2(w / 2, screen_height / 2 + 10))
    draw_text(font15, "LEWY PRZYCISK - ROZPOCZNIJ GRĘ", (255, 255, 255),
              Vector2(w / 2, screen_height / 2 + 60))

    pygame.display.update()

    start_game = False
    while not start_game:
        if GPIO.input(CONST_LEFT_SWITCH) == 0:
            start_game = True


def end_screen(new_record, points):
    screen.fill((0, 0, 0))

    if new_record == 1:
        f = open("plane_record.txt", "w")
        f.write(str(points))

        draw_text(font40, "NOWY REKORD", (0, 255, 0), Vector2(screen_width / 2, 75))
        draw_text(font50, str(points), (0, 255, 0), Vector2(screen_width / 2, 150))

    else:
        draw_text(font40, "TWÓJ WYNIK:", (255, 255, 0), Vector2(screen_width / 2, 75))
        draw_text(font50, str(points), (255, 255, 0), Vector2(screen_width / 2, 150))

    draw_text(font20, "Lewy przycisk - nowa gra", (255, 255, 255), Vector2(screen_width / 2, 230))
    draw_text(font20, "Prawy przycisk - koniec gry", (255, 255, 255), Vector2(screen_width / 2, 270))
    pygame.display.update()

    while True:
        if GPIO.input(CONST_LEFT_SWITCH) == 0:
            plane_game()
        elif GPIO.input(CONST_RIGHT_SWITCH) == 0:
            menu.games()
            

# NEW TARGETS GENERATING
def targets_generating(targets):
    new_targets_pos = random.sample(range(1, 15), random.randint(4, 7))  # 4 TO 7 - NUMBER OF THE NEW TARGETS, 1 TO 14 - location range
    targets.extend(pygame.Rect(pos * 22 + 8, 8, 20, 20) for pos in new_targets_pos)
    
    return targets


def plane_game():
    dt = 0.0
    Tp = 0.0
    fps = 50.0
    clock = pygame.time.Clock()
    start = True

    plane = Plane(screen)
    targets = []
    bullets = []

    points = 0

    new_record = False

    last_targets_time = time.time()
    new_targets_time = 2.5
    new_bullets_time = 0.1
    last_bullets_time = time.time()
    bullets_velocity = 11

    # GENERATE FIRST TARGETS
    targets = targets_generating([])

    # READ RECORD FROM FILE
    with open("plane_record.txt") as f:
        record = list(f)
        record = ''.join(record)  # converting list into string
        record = int(record)

    first_frame = True

    while True:
        dt += clock.tick() / 1000.0

        t1 = time.time()
        if start:
            start_screen(plane)
            start = False

        dt -= Tp


        while dt > 1 / fps:
            result_change = 1
            #dt -= 1 / fps
            targets_move = 1
            t1 = time.time()

            # plane move
            delta_x = 0
            
            # plane control
            if adc.read(channel=5) < 50:
                delta_x -= 22 #(int)(Tp*200)
            if adc.read(channel=5) > 600:
                delta_x += 22 #(int)(Tp*200)
            plane.move(delta_x)

     
            # collision - target and bullet
            bullet_rect = pygame.Rect(0, 0, 10, 10)
            for bullet in bullets:
                bullet_rect.topleft = (bullet.x - 5, bullet.y - 5 - bullets_velocity)
                index = bullet_rect.collidelist(targets)

                if index >= 0:
                    targets.pop(index)  # remove target
                    bullet.x = -30
                    points += 1
                    result_change = True

            # remove bullets after collision and out of screen bullets
            bullets = [bullet for bullet in bullets if bullet.x != -30 or bullet.y - 5 < bullets_velocity + 10]


            # new bullet
            if time.time() - last_bullets_time > new_bullets_time and GPIO.input(CONST_LEFT_SWITCH) == 0:
                last_bullets_time = time.time()
                bullets.append(Vector2(plane.get_position()[0] + 10, plane.get_position()[1] - 10))

            # new targets
            if time.time() - last_targets_time > new_targets_time:
                last_targets_time = time.time()
                new_targets_time = 0.99 * new_targets_time
                targets_move = True

                # previous targets move in y-axis
                for target in targets:
                    target.y += 22

                # generate new targets
                targets = targets_generating(targets)

            # bullets move in y-axis
            for bullet in bullets:
                bullet.y -= bullets_velocity

            # cleaning screen
            screen.fill((0, 0, 0))

            plane.draw()

            # bullets draw
            bullet_rect = pygame.Rect(0, 0, 10, 10)
            for bullet in bullets:
                pygame.draw.circle(screen, (255, 20, 0), [int(bullet.x), int(bullet.y)], 5)
                
            # targets draw
            for t in targets:
                pygame.draw.rect(screen, (255, 255, 0), t)

            plane_position = plane.get_position()
            
            # game end
            if len(targets) > 0 and targets[0].y > plane_position.y - 15:
                end_screen(new_record, points)

            width = 6
            
            pygame.draw.lines(screen, (255, 255, 255), False,
                                  [(width / 2, width / 2), (width / 2, screen_height - width / 2),
                                   (16 * 22 + 8 + width / 2, screen_height - width / 2),
                                   (16 * 22 + 8 + width / 2, width / 2)], 
                                   width)

            draw_text(font20, "REKORD", (255, 255, 0), Vector2(screen_width - 55, 100))
            draw_text(font20, "PKT.", (255, 255, 0), Vector2(screen_width - 55, screen_height / 2 + 90))

            
            if points > record:
                draw_text(font50, str(points), (0, 255, 0), Vector2(screen_width - 55, 50))
                draw_text(font50, str(points), (0, 255, 0),
                              Vector2(screen_width - 55, screen_height / 2 + 40))
                new_record = True

            else:
                draw_text(font50, str(record), (255, 255, 0), Vector2(screen_width - 55, 50))
                draw_text(font50, str(points), (255, 255, 0),
                              Vector2(screen_width - 55, screen_height / 2 + 40))
            
            
            # update all pixels
            pygame.display.flip()
            
            Tp = (time.time() - t1)
            
           