# PLANE GAME
# AUTHOR: DOMINIK BOGIELCZYK

import pygame, time, sys, os, random
from pygame.math import Vector2
import RPi.GPIO as GPIO
from plane_class import Plane
from MCP3008_class import MCP3008

sys.path.insert(0, '/home/pi/Desktop/main/menu')
import menu


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
left_switch = 32
right_switch = 33
GPIO.setup(left_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(0)

font15 = pygame.font.SysFont("dejavuserif", 15)
font20 = pygame.font.SysFont("dejavuserif", 20)
font40 = pygame.font.SysFont("dejavuserif", 40)
font50 = pygame.font.SysFont("dejavuserif", 50)

adc = MCP3008()


def draw_text(font, text, color, pos):
    t = font.render(text, False, color)
    text_rect = t.get_rect(center=(pos.x, pos.y))
    screen.blit(t, text_rect)
    pygame.display.update(text_rect.x, text_rect.y, text_rect.width, text_rect.height)


def start_screen(plane):
    screen.fill((0, 0, 0))
    width = 6
    w = 16 * 22 + 8

    pygame.draw.lines(screen, (255, 255, 255), False,
                      [(width / 2, width / 2), (width / 2, screen.get_height()),
                       (w + width / 2, screen.get_height()), (w + width / 2, width / 2)], width)
    plane.draw()

    draw_text(font40, "PLANE", (255, 255, 255), Vector2((w / 2, 30)))
    draw_text(font20, "STEROWANIE:", (255, 255, 0),
              Vector2(w / 2, screen.get_height() / 2 - 50))
    draw_text(font15, "STRZAŁ - LEWY PRZYCISK", (255, 255, 0),
              Vector2(w / 2, screen.get_height() / 2 - 20))
    draw_text(font15, "RUCH LEWO-PRAWO - LEWY JOYSTICK", (255, 255, 0),
              Vector2(w / 2, screen.get_height() / 2 + 10))
    draw_text(font15, "LEWY PRZYCISK - ROZPOCZNIJ GRĘ", (255, 255, 255),
              Vector2(w / 2, screen.get_height() / 2 + 60))

    pygame.display.update()

    start_game = False
    while not start_game:
        if GPIO.input(left_switch) == 0:
            start_game = True


def end_screen(new_record, points):
    screen.fill((0, 0, 0))

    if new_record == 1:
        os.chdir('/home/pi/Desktop/main/menu/Plane')
        f = open("plane_record.txt", "w")
        f.write(str(points))
        f.close()

        draw_text(font40, "NOWY REKORD", (0, 255, 0), Vector2(screen.get_width() / 2, 75))
        draw_text(font50, str(points), (0, 255, 0), Vector2(screen.get_width() / 2, 150))

    else:
        draw_text(font40, "TWÓJ WYNIK:", (255, 255, 0), Vector2(screen.get_width() / 2, 75))
        draw_text(font50, str(points), (255, 255, 0), Vector2(screen.get_width() / 2, 150))

    draw_text(font20, "Lewy przycisk - nowa gra", (255, 255, 255), Vector2(screen.get_width() / 2, 230))
    draw_text(font20, "Prawy przycisk - koniec gry", (255, 255, 255), Vector2(screen.get_width() / 2, 270))
    pygame.display.update()

    while True:
        if GPIO.input(left_switch) == 0:
            plane_game()
        elif GPIO.input(right_switch) == 0:
            menu.games()


def plane_game():
    # NEW TARGETS GENERATING
    def targets_generating():
        new_targets_pos = []
        for i in range(random.randint(4, 7)):  # 4 TO 7 - NUMBER OF THE NEW TARGETS
            n = random.randint(1, 14)  # new target position choosing

            while n in new_targets_pos:  # ADD UNIQUE POSITION OF THE TARGET
                n = random.randint(1, 14)

            new_targets_pos.append(n)

        for target_pos in new_targets_pos:  # ADD UNIQUE TARGETS TO LIST
            targets.append(pygame.Rect(target_pos * 22 + 8, 8, 20, 20))

        return targets

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
    targets_generating()

    # READ RECORD FROM FILE
    os.chdir('/home/pi/Desktop/main/menu/Plane')
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
            result_change = 0
            #dt -= 1 / fps
            targets_move = 0
            t1 = time.time()

            # plane move
            delta_x = 0
            delta = (int)(Tp*200)
            if delta<10:
                 delta = 10
            # plane controlling
            if adc.read(channel=5) < 50:
                delta_x -= delta
            if adc.read(channel=5) > 600:
                delta_x += delta
            plane.move(delta_x)

            to_update = []

            # collision - target and bullet
            for bullet in bullets:
                index = pygame.Rect(bullet.x - 5, bullet.y - 5 - bullets_velocity, 10, 10).collidelist(targets)

                if index >= 0:
                    to_update.append(pygame.Rect(targets[index]))
                    to_update.append(pygame.Rect(bullet.x - 5, bullet.y - 5, 10, 10))
                    targets.pop(index)  # remove target
                    bullet.x = -30
                    points += 1
                    result_change = True

            for i in range(len(bullets)):
                if i < len(bullets):
                    if bullets[i].x == -30:
                        bullets.pop(i)

            # remove out of screen bullets
            for i in range(len(bullets)):
                if i < len(bullets):
                    if bullets[i].y - 5 < bullets_velocity + 10:
                        to_update.append(pygame.Rect(bullets[i].x - 5, bullets[i].y - 5, 10, 10))
                        bullets.pop(i)

            # new bullet
            if time.time() - last_bullets_time > new_bullets_time and GPIO.input(left_switch) == 0:
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
                targets_generating()

            # bullets move in y-axis
            for bullet in bullets:
                bullet.y -= bullets_velocity

            # cleaning screen
            screen.fill((0, 0, 0))

            plane.draw()
            plane.update(delta_x)

            for bullet in bullets:
                pygame.draw.circle(screen, (255, 20, 0), [int(bullet.x), int(bullet.y)], 5)
                # bullet in actual position and erase bullet in previous position
                to_update.append(pygame.Rect(bullet.x - 5, bullet.y - 5, 10, 10 + bullets_velocity))

            plane_position = plane.get_position()

            # game end
            if len(targets) > 0 and targets[0].y > plane_position.y - 15:
                end_screen(new_record, points)

            if targets_move or first_frame:
                for t in targets:
                    y = t.y - 22
                    if y < 0:
                        y = 0
                    to_update.append(pygame.Rect(t.x, y, 20, 20 + 22))
                    pygame.draw.rect(screen, (255, 255, 0), t)

            if first_frame:
                # frame
                width = 6
                pygame.draw.lines(screen, (255, 255, 255), False,
                                  [(width / 2, width / 2), (width / 2, screen.get_height() - width / 2),
                                   (16 * 22 + 8 + width / 2, screen.get_height() - width / 2),
                                   (16 * 22 + 8 + width / 2, width / 2)], width)

                draw_text(font20, "REKORD", (255, 255, 0), Vector2(screen.get_width() - 55, 100))
                draw_text(font50, str(record), (255, 255, 0), Vector2(screen.get_width() - 55, 50))
                draw_text(font20, "PKT.", (255, 255, 0), Vector2(screen.get_width() - 55, screen.get_height() / 2 + 90))
                pygame.display.update()  # we update all pixels

            elif result_change:
                if points > record:
                    draw_text(font50, str(points), (0, 255, 0), Vector2(screen.get_width() - 55, 50))
                    draw_text(font50, str(points), (0, 255, 0),
                              Vector2(screen.get_width() - 55, screen.get_height() / 2 + 40))
                    new_record = True

                else:
                    draw_text(font50, str(record), (255, 255, 0), Vector2(screen.get_width() - 55, 50))
                    draw_text(font50, str(points), (255, 255, 0),
                              Vector2(screen.get_width() - 55, screen.get_height() / 2 + 40))
            
            
            pygame.display.update(to_update)
            Tp = (time.time() - t1)
            
            first_frame = 0



