# SNAKE
# AUTHOR: DOMINIK BOGIELCZYK
import time
from pygame.math import Vector2
from random import randint
import pygame
import sys
from collections import Counter
from MCP3008_class import MCP3008


class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, orientation_, is_head=False, is_fruit=False):
        super().__init__()
        self.orientation = orientation_
        if is_head == 0 and is_fruit == 0:
            self.image_h = pygame.image.load("textures/snake_sprite_horizontal.png")
            self.image_v = pygame.image.load("textures/snake_sprite_vertical.png")
            self.image = self.image_h  # default image
        elif is_head == 1:
            self.image_left = pygame.image.load("textures/snake_head_left.png")
            self.image_right = pygame.image.load("textures/snake_head_right.png")
            self.image_up = pygame.image.load("textures/snake_head_up.png")
            self.image_down = pygame.image.load("textures/snake_head_down.png")
            self.image = self.image_left  # default image
        else:
            self.image = pygame.image.load("textures/fruit.png")

        self.rect = screen.blit(self.image, (pos_x, pos_y))

    def update(self, dir="left", delta=0):
        if dir == "left" and self.rect.x - delta >= 20:
            self.rect.x = self.rect.x - delta
        elif dir == "right" and self.rect.x + delta <= screen.get_width() - 40:
            self.rect.x = self.rect.x + delta
        elif dir == "up" and self.rect.y - delta >= 60:
            self.rect.y = self.rect.y - delta
        elif dir == "down" and self.rect.y + delta <= screen.get_height() - 40:
            self.rect.y = self.rect.y + delta

        self.orientation = dir

        if self.orientation == "left":
            self.image = self.image_left
        elif self.orientation == "right":
            self.image = self.image_right
        elif self.orientation == "up":
            self.image = self.image_up
        else:
            self.image = self.image_down

    def get_orientation(self):
        return self.orientation


class Wall_part(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load("textures/wall.png")
        self.rect = screen.blit(self.image, (pos_x, pos_y))


pygame.init()
pygame.mouse.set_visible(0)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((480, 320))

font20 = pygame.font.SysFont("calibri", 20)
font40 = pygame.font.SysFont("calibri", 40)
font30 = pygame.font.SysFont("calibri", 30)


def make_background():
    background = pygame.sprite.Group()
    arena = pygame.sprite.Sprite()
    arena.image = pygame.image.load("textures/background.png")
    arena.rect = screen.blit(arena.image, (20, 60))
    background.add(arena)

    for i in range(int((screen.get_height() - 40) / 20)):
        background.add(Wall_part(0, 40 + 20 * i))
        background.add(Wall_part(screen.get_width() - 20, 40 + 20 * i))

    for i in range(int((screen.get_width() - 40) / 20)):
        background.add(Wall_part(20 + 20 * i, 40))
        background.add(Wall_part(20 + 20 * i, screen.get_height() - 20))
    return background


def draw_text(text, font, color, position):
    t = font.render(text, True, color)
    text_rect = t.get_rect(center=(position.x, position.y))
    screen.blit(t, text_rect)
    pygame.display.update(text_rect.x, text_rect.y-5, text_rect.width, text_rect.height+10)


def start_screen(background):
    screen.fill((0, 0, 0))
    background.draw(screen)

    draw_text("SNAKE", font40, (122, 154, 175), Vector2((screen.get_width() / 2, 20)))
    draw_text("Sterowanie strzałkami", font20, (255, 255, 255),
              Vector2(screen.get_width() / 2, screen.get_height() / 2 - 50))
    draw_text("Spacja - rozpocznij grę", font20, (255, 255, 255),
              Vector2(screen.get_width() / 2, screen.get_height() / 2))

    pygame.display.update()

    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                start_game = True


#################################################################################
def end_screen(points, record):
    screen.fill((0, 0, 0))

    text = font20.render("q - wyjdź, spacja - nowa gra", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() / 2, 260))
    screen.blit(text, text_rect)

    if points > record:
        f = open("snake_record.txt", "w")
        f.write(str(points))
        f.close()
        draw_text("NOWY REKORD", font40, (0, 255, 0), Vector2(screen.get_width() / 2, 50))
        draw_text("Twój wynik: " + str(points), font40, (0, 255, 0),
                  Vector2(screen.get_width() / 2, screen.get_height() / 2))
    else:
        draw_text("KONIEC GRY", font40, (255, 0, 0), Vector2(screen.get_width() / 2, 50))
        draw_text("Twój wynik: " + str(points), font40, (255, 0, 0),
                  Vector2(screen.get_width() / 2, screen.get_height() / 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                snake(False)

adc = MCP3008()

def snake(start=True):
    dt = 0.0
    fps = 4.0
    clock = pygame.time.Clock()
    points = 0
    direction = "left"
    lvl = 1
    lvl_points = 0  # points at this level
    next_level = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70] #how many points to next lvl
    block_size = 20
    first_frame = True

    # SNAKE INIT
    snake_head_group = pygame.sprite.Group()
    snake_body_group = pygame.sprite.Group()
    snake_head = Block(screen.get_width() / 2, screen.get_height() / 2, orientation_=direction, is_head=True)
    snake_head_group.add(snake_head)
    for i in range(4):
        snake_body_group.add(
            Block(screen.get_width() / 2 + block_size * (i + 1), screen.get_height() / 2, orientation_=direction))

    # MAKE BACKGROUND - WALLS AND SAND
    background = make_background()

    # FRUIT INIT
    fruit_group = pygame.sprite.Group()
    fruit = Block(20 + 5 * 20, 60 + 7 * 20, None, None, True)
    fruit_group.add(fruit)

    # LOAD RECORD
    with open("snake_record.txt") as f:
        record = list(f)
        record = ''.join(record)  # converting list into string
        record = int(record)

    while True:
        t1 = time.time()
        if start == 1:
            start_screen(background)
        start = 0
        t2 = time.time()

        dt -= t2 - t1

        dt += clock.tick() / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()

            if (pygame.key.get_pressed()[pygame.K_LEFT] or adc.read(channel=2) < 50) and direction != "right":
                direction = "left"
            if (pygame.key.get_pressed()[pygame.K_RIGHT] or adc.read(channel=2) > 600) and direction != "left":
                direction = "right"
            if (pygame.key.get_pressed()[pygame.K_UP] or adc.read(channel=1) > 600) and direction != "down":
                direction = "up"
            if (pygame.key.get_pressed()[pygame.K_DOWN] or adc.read(channel=1) < 50) and direction != "up":
                direction = "down"

        while dt > 1 / fps:
            dt -= 1 / fps
            pos = []
            orientation = []
            for obj in snake_head_group:
                pos.append(Vector2(obj.rect.x, obj.rect.y))
                orientation.append(obj.get_orientation())

            for obj in snake_body_group:
                pos.append(Vector2(obj.rect.x, obj.rect.y))
                orientation.append(obj.get_orientation())

            # Head meet other snake part
            temp = Counter([tuple(x) for x in pos])
            unique_pos = [list(k) for k, v in temp.items() if v == 1]
            if len(pos) > len(unique_pos):
                end_screen(points, record)

            # Update snake after movement
            i = 0
            for obj in snake_body_group:
                obj.orientation = orientation[i]
                if orientation[i] == "left" or orientation[i] == "right":
                    obj.image = obj.image_h
                else:
                    obj.image = obj.image_v
                obj.rect = screen.blit(obj.image, (pos[i].x, pos[i].y))
                i += 1

            # GAME END
            for head in snake_head_group:
                if head.rect.x < block_size or head.rect.x > screen.get_width() - 2 * block_size or head.rect.y < 3 * block_size or head.rect.y > screen.get_height() - 2 * block_size:
                    end_screen(points, record)

            # THE SNAKE EATS THE FRUIT
            if snake_head.rect.colliderect(fruit.rect) == 1:
                points += 1
                lvl_points += 1

                # NEW FRUIT GENERATING
                fruit.rect.x = 20 + randint(0, 21) * 20
                fruit.rect.y = 60 + randint(0, 11) * 20

                # FRUIT CAN'T BE IN PLACE WHERE SNAKE IS
                for i in range(len(pos)):
                    if pos[i].x == fruit.rect.x and pos[i].y == fruit.rect.y:
                        fruit.rect.x = 20 + randint(0, 21) * 20
                        fruit.rect.y = 60 + randint(0, 11) * 20
                        i = 0

                fruit_group.draw(screen)

                pygame.display.update(pygame.Rect(fruit.rect.x, fruit.rect.y, 20, 20))

                if lvl_points < next_level[lvl - 1]:
                    text = font20.render(str(points), True, color)
                    text_rect = text.get_rect(topleft=(100, 5))
                    screen.blit(text, text_rect)
                    pygame.display.update(pygame.Rect(text_rect.x, text_rect.y, text_rect.width + 5, text_rect.height))

                snake_body_group.add(
                    Block(pos[len(pos) - 1].x, pos[len(pos) - 1].y, orientation_=orientation[len(orientation) - 1]))

            # NEXT LEVEL
            if lvl_points >= next_level[lvl - 1]:
                lvl += 1
                lvl_points = 0

                draw_text("POZIOM " + str(lvl), font40, (255, 0, 0),
                          Vector2(screen.get_width() / 2, screen.get_height() / 2))
                draw_text("Naciśnij spację", font20, (255, 0, 0),
                          Vector2(screen.get_width() / 2, screen.get_height() / 2 + 80))

                # WAITING FOR SPACE PRESS
                t1 = time.time()
                start_level = False
                while not start_level:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                            pygame.quit()
                            sys.exit()
                        if pygame.key.get_pressed()[pygame.K_SPACE]:
                            start_level = True
                t2 = time.time()
                dt -= t2 - t1

                # FASTER SNAKE MOVEMENT IN NEXT LEVEL
                fps += 0.5

                # SNAKE RETURN TO SIZE = 4
                i = 0
                for obj in snake_body_group:
                    if i >= 3:
                        snake_body_group.remove(obj)
                    i += 1

                first_frame = True

            # DRAWING
            if points > record:
                record_info = points
                color = (0, 255, 0)
            else:
                record_info = record
                color = (122,154,175)

            snake_head_group.update(direction, block_size)
            screen.fill((0, 0, 0))
            background.draw(screen)

            snake_head_group.draw(screen)
            snake_body_group.draw(screen)

            draw_text("Punkty:  " + str(points) + "      Rekord:  " + str(record_info), font30, color,
                      Vector2(135, 20))
            draw_text("Poziom " + str(lvl) + "    " + str(lvl_points) + "/" + str(next_level[lvl - 1]), font30, color,
                      Vector2((screen.get_width() - 100, 20)))

            if first_frame == 1:
                fruit_group.draw(screen)
                pygame.display.update()
            else:
                # head update
                for obj in snake_head_group:
                    pygame.display.update(pygame.Rect(obj.rect.x, obj.rect.y, 20, 20))
                # previous head update
                pygame.display.update(pygame.Rect(pos[0].x, pos[0].y, 20, 20))

                # last snake part update
                pygame.display.update(pygame.Rect(pos[len(pos) - 1].x, pos[len(pos) - 1].y, 20, 20))

            first_frame = False


snake()
