import pygame
import sys
from pygame.math import Vector2
import os
import time


class Button(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("textures/" + file).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, file):
        self.image = pygame.image.load("textures/" + file).convert()


pygame.init()
pygame.mouse.set_visible(0)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((480, 320))

font10 = pygame.font.Font("font/KOMTITBR.ttf", 10)
font15 = pygame.font.Font("font/KOMTITBR.ttf", 15)
font20 = pygame.font.Font("font/KOMTITBR.ttf", 20)
font25 = pygame.font.Font("font/KOMTITBR.ttf", 25)
font40 = pygame.font.Font("font/KOMTITBR.ttf", 40)

green = (26, 255, 26)
yellow = (255, 255, 26)
red = (255, 0, 0)
grey = (122, 154, 175)


def draw_text(text, font, color, position):
    t = font.render(text, True, color)
    text_rect = t.get_rect(center=(position.x, position.y))
    screen.blit(t, text_rect)
    pygame.display.update(text_rect.x, text_rect.y, text_rect.width, text_rect.height)


def records():
    texts = ["HUNTER", "MAZE", "SNAKE", "PONG", "PLANE"]

    with open("hunter_record.txt") as f:
        hunter_record = list(f)
        hunter_record = ''.join(hunter_record)  # converting list into string
        hunter_date = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime("hunter_record.txt")))
    with open("maze_record.txt") as f:
        maze_record = list(f)
        maze_record = ''.join(maze_record)
        maze_date = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime("maze_record.txt")))
    with open("snake_record.txt") as f:
        snake_record = list(f)
        snake_record = ''.join(snake_record)
        snake_date = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime("snake_record.txt")))
    with open("pong_record.txt") as f:
        pong_record = list(f)
        pong_record = ''.join(pong_record)
        pong_date = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime("pong_record.txt")))
    with open("plane_record.txt") as f:
        plane_record = list(f)
        plane_record = ''.join(plane_record)
        plane_date = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime("plane_record.txt")))

    points = [hunter_record, maze_record, snake_record, pong_record, plane_record]
    dates = [hunter_date, maze_date, snake_date, pong_date, plane_date]

    screen.fill((0, 0, 0))
    for i in range(5):
        draw_text(texts[i], font20, grey, Vector2((70, 40 + i * 40)))
        draw_text(points[i] + " pkt.", font15, grey, Vector2((screen.get_width()/2, 40 + i * 40)))
        draw_text(dates[i], font10, grey, Vector2((screen.get_width() - 90, 40 + i * 40)))

    draw_text("MENU", font20, green, Vector2((screen.get_width()/2, screen.get_height() - 50)))

    pygame.display.update()

    return_to_menu = False
    while not return_to_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                return_to_menu = True
                menu()


def games():
    state = 0
    texts = ["HUNTER", "MAZE", "SNAKE", "PONG", "PLANE", "MENU"]

    screen.fill((0, 0, 0))
    offset = 40
    delta = 45

    for i in range(len(texts)-1):
        if i == state:
            draw_text(texts[i], font25, green, Vector2(screen.get_width() / 2, offset + delta * i))
        else:
            draw_text(texts[i], font25, yellow, Vector2(screen.get_width() / 2, offset + delta * i))
    draw_text(texts[5], font25, grey, Vector2(screen.get_width() / 2, offset + delta * 5))
    pygame.display.update()

    dt = 0
    clock = pygame.time.Clock()

    while True:
        dt += clock.tick() / 1000.0
        while dt > 1 / 20:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_w]:
                        state -= 1
                        if state < 0:
                            state = 0

                    elif pygame.key.get_pressed()[pygame.K_s]:
                        state += 1
                        if state > 5:
                            state = 5

                    if pygame.key.get_pressed()[pygame.K_SPACE] and state == 5:
                        menu()

                    screen.fill((0, 0, 0))
                    for i in range(len(texts)):
                        if i == 5 and i != state:
                            draw_text(texts[i], font25, grey, Vector2(screen.get_width() / 2, offset + delta * i))
                        else:
                            if i == state:
                                draw_text(texts[i], font25, green, Vector2(screen.get_width() / 2, offset + delta * i))
                            else:
                                draw_text(texts[i], font25, yellow, Vector2(screen.get_width() / 2, offset + delta * i))



                    pygame.display.update()


def menu():
    state = 0
    sound = 0
    offset = 50
    delta = 70

    screen.fill((0, 0, 0))
    texts = ["NOWA GRA", "REKORDY", "MUZYKA: ON", "MUZYKA: OFF", "ZAMKNIJ"]

    draw_text(texts[0], font40, green, Vector2(screen.get_width() / 2, offset + 70 * 0))
    draw_text(texts[1], font40, yellow, Vector2(screen.get_width() / 2, offset + 70 * 1))
    if sound:
        draw_text(texts[2], font40, yellow, Vector2(screen.get_width() / 2, offset + 70 * 2))
    else:
        draw_text(texts[3], font40, yellow, Vector2(screen.get_width() / 2, offset + 70 * 2))
    draw_text(texts[4], font40, yellow, Vector2(screen.get_width() / 2, offset + 70 * 3))

    pygame.display.update()

    dt = 0
    clock = pygame.time.Clock()

    while True:
        dt += clock.tick() / 1000.0
        while dt > 1 / 20:
            next_screen = False

            while not next_screen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if pygame.key.get_pressed()[pygame.K_w]:
                            state -= 1
                            if state < 0:
                                state = 0

                        if pygame.key.get_pressed()[pygame.K_s]:
                            state += 1
                            if state > 3:
                                state = 3

                        if pygame.key.get_pressed()[pygame.K_SPACE] and state == 0:
                            games()

                        if pygame.key.get_pressed()[pygame.K_SPACE] and state == 1:
                            records()

                        if pygame.key.get_pressed()[pygame.K_SPACE] and state == 2:
                            sound = not sound

                        if pygame.key.get_pressed()[pygame.K_SPACE] and state == 3:
                            pygame.quit()
                            sys.exit()

                        screen.fill((0, 0, 0))
                        for i in range(3):
                            if i != 2:
                                if i == state:
                                    draw_text(texts[i], font40, green, Vector2(screen.get_width() / 2, offset + delta * i))
                                else:
                                    draw_text(texts[i], font40, yellow, Vector2(screen.get_width() / 2, offset + delta * i))
                            else:
                                if i == state:
                                    if sound:
                                        draw_text(texts[2], font40, green, Vector2(screen.get_width() / 2, offset + delta * i))
                                    else:
                                        draw_text(texts[3], font40, green, Vector2(screen.get_width() / 2, offset + delta * i))
                                else:
                                    if sound:
                                        draw_text(texts[2], font40, yellow,
                                                  Vector2(screen.get_width() / 2, offset + delta * i))
                                    else:
                                        draw_text(texts[3], font40, yellow,
                                                  Vector2(screen.get_width() / 2, offset + delta * i))

                        if state == 3:
                            draw_text(texts[4], font40, red, Vector2(screen.get_width() / 2, offset + delta * 3))
                        else:
                            draw_text(texts[4], font40, yellow, Vector2(screen.get_width() / 2, offset + delta * 3))

                        pygame.display.update()

                dt -= 1 / 20


menu()
