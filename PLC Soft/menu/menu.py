import pygame
import sys
from pygame.math import Vector2
import os
import time
import RPi.GPIO as GPIO
import spidev
from MCP3008_class import MCP3008

sys.path.insert(0 , '/home/pi/Desktop/main/menu/Maze')
import Game
sys.path.insert(0 , '/home/pi/Desktop/main/menu/Snake')
import snake
sys.path.insert(0 , '/home/pi/Desktop/main/menu/Pong')
import pong
sys.path.insert(0 , '/home/pi/Desktop/main/menu/Plane')
import plane
sys.path.insert(0 , '/home/pi/Desktop/main/menu/Hunter')
import HunterGame

# Open SPI bus
spi = spidev.SpiDev()
spi.open(1, 2)
spi.max_speed_hz = 1000000

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
left_switch = 32
GPIO.setup(left_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

adc = MCP3008()


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
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

os.chdir('/home/pi/Desktop/main/menu')
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
    os.chdir('/home/pi/Desktop/main/menu')
    with open("Hunter/hunter_record.txt") as f:
        hunter_record = list(f)
        hunter_record = ''.join(hunter_record)  # converting list into string
        hunter_date = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime("Hunter/hunter_record.txt")))
    with open("Maze/maze_record.txt") as f:
        maze_record = list(f)
        maze_record = ''.join(maze_record)
        maze_date = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime("Maze/maze_record.txt")))
    with open("Snake/snake_record.txt") as f:
        snake_record = list(f)
        snake_record = ''.join(snake_record)
        snake_date = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime("Snake/snake_record.txt")))
    with open("Pong/pong_record.txt") as f:
        pong_record = list(f)
        pong_record = ''.join(pong_record)
        pong_date = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime("Pong/pong_record.txt")))
    with open("Plane/plane_record.txt") as f:
        plane_record = list(f)
        plane_record = ''.join(plane_record)
        plane_date = time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime("Plane/plane_record.txt")))

    points = [hunter_record, maze_record, snake_record, pong_record, plane_record]
    dates = [hunter_date, maze_date, snake_date, pong_date, plane_date]

    screen.fill((0, 0, 0))
    for i in range(5):
        draw_text(texts[i], font20, grey, Vector2((70, 40 + i * 40)))
        draw_text(points[i] + " pkt.", font15, grey, Vector2((screen.get_width() / 2, 40 + i * 40)))
        draw_text(dates[i], font10, grey, Vector2((screen.get_width() - 90, 40 + i * 40)))

    draw_text("MENU", font20, green, Vector2((screen.get_width() / 2, screen.get_height() - 50)))

    pygame.display.update()

    return_to_menu = False
    prev_switch = GPIO.input(left_switch)
    while not return_to_menu:
        prev_switch = GPIO.input(left_switch)
        time.sleep(0.05)
        if prev_switch == 1 and GPIO.input(left_switch) == 0:
            return_to_menu = True
            menu()


def games():
    state = 0
    texts = ["HUNTER", "MAZE", "SNAKE", "PONG", "PLANE", "MENU"]

    screen.fill((0, 0, 0))
    offset = 40
    delta = 45

    prev_val = adc.read(channel=4)

    for i in range(len(texts) - 1):
        if i == state:
            draw_text(texts[i], font25, green, Vector2(screen.get_width() / 2, offset + delta * i))
        else:
            draw_text(texts[i], font25, yellow, Vector2(screen.get_width() / 2, offset + delta * i))
    draw_text(texts[5], font25, grey, Vector2(screen.get_width() / 2, offset + delta * 5))
    pygame.display.update()
    time.sleep(0.2)

    while True:
        update = False
        if prev_val > 50 and adc.read(channel=4) < 50:
            state += 1
            if state > 5:
                state = 5
            update = True

        elif prev_val < 600 and adc.read(channel=4) > 600:
            state -= 1
            if state < 0:
                state = 0
            update = True

        if update:
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
        
        if GPIO.input(left_switch) == 0 and state == 0:
            HunterGame.HunterGame()

        if GPIO.input(left_switch) == 0 and state == 1:
            Game.Game()

        if GPIO.input(left_switch) == 0 and state == 2:
            snake.snake()

        if GPIO.input(left_switch) == 0 and state == 3:
            pong.Pingpong()

        if GPIO.input(left_switch) == 0 and state == 4:
            plane.plane_game()

        if GPIO.input(left_switch) == 0 and state == 5:
            menu()

        prev_val = adc.read(channel=4)
        time.sleep(0.05)


def menu():
    state = 0
    sound = 0
    offset = 50
    delta = 70
    prev_switch = GPIO.input(left_switch)
    prev_val = adc.read(channel=4)

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

    while True:
        update = False

        if prev_val > 50 and adc.read(channel=4) < 50:
            update = True
            state += 1
            if state > 3:
                state = 3

        elif prev_val < 600 and adc.read(channel=4) > 600:
            update = True
            state -= 1
            if state < 0:
                state = 0


        if prev_switch == 1 and GPIO.input(left_switch) == 0 and state == 0:
            games()

        elif GPIO.input(left_switch) == 0 and state == 1:
            records()

        if prev_switch == 1 and GPIO.input(left_switch) == 0 and state == 2:
            sound = not sound
            update = True

        if GPIO.input(left_switch) == 0 and state == 3:
            pygame.quit()
            sys.exit()

        if update:
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
                            draw_text(texts[2], font40, yellow, Vector2(screen.get_width() / 2, offset + delta * i))
                        else:
                            draw_text(texts[3], font40, yellow, Vector2(screen.get_width() / 2, offset + delta * i))

                if state == 3:
                    draw_text(texts[4], font40, red, Vector2(screen.get_width() / 2, offset + delta * 3))
                else:
                    draw_text(texts[4], font40, yellow, Vector2(screen.get_width() / 2, offset + delta * 3))

            pygame.display.update()

        prev_switch = GPIO.input(left_switch)
        prev_val = adc.read(channel=4)
        time.sleep(0.05)


if __name__ == '__main__':
    menu()
