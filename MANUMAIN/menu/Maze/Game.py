import pygame
import time
import sys
from Maze import Maze
from  Player import Player
from MCP3008_class import MCP3008
import RPi.GPIO as GPIO

sys.path.insert(0, '/home/pi/Desktop/main/menu')
import menu

adc = MCP3008()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33,GPIO.IN,pull_up_down=GPIO.PUD_UP) #prawy
GPIO.setup(32,GPIO.IN,pull_up_down=GPIO.PUD_UP) #lewy
class Game():


    def sterowanie_oknem(self,player):
        if GPIO.input(32) == 0:
            menu.menu()
        if GPIO.input(33) == 0:
            game=Game()

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(0)
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        clock = pygame.time.Clock()

        #screen = pygame.display.set_mode([480, 320])
        player = Player(screen)
        maze = Maze(screen, width=2)
        fps = 20.0
        dx = 0
        dy = 0
        dt = 0
        tlo_menu = pygame.sprite.Sprite()
        tlo_menu.image = pygame.image.load("menu.png").convert()
        tlo_menu.rect = tlo_menu.image.get_rect()
        tlo_wygrana = pygame.sprite.Sprite()
        tlo_wygrana.image = pygame.image.load("tlo_wygrana.png").convert()
        tlo_wygrana.rect = tlo_wygrana.image.get_rect()
        tlo_porazka = pygame.sprite.Sprite()
        tlo_porazka.image = pygame.image.load("tlo_porazka.png").convert()
        tlo_porazka.rect = tlo_porazka.image.get_rect()

        font_style = pygame.font.SysFont("dejavuserif", 20)

        
        while True:
            dt += clock.tick() / 1000.0
            while dt > 1 / fps:
                dt -= 1 / fps
                
                if player.counter_a==0:
                    screen.blit(tlo_menu.image, tlo_menu.rect)
                    pygame.display.flip()
                screen.fill((0, 0, 0))
                if GPIO.input(32) == 0 or player.counter_a==1:
                    player.counter_a=1
                    if player.zycia > 0:

                        if player.poziom == 1:
                            player.color_ = (255, 69, 0)
                            maze.set_color((255, 255, 0))
                            maze.draw_level_1()
                            player.kolizje(maze.linie)

                        if player.poziom == 2:
                            player.color_ = (255, 69, 0)
                            maze.set_color((0, 255, 255))
                            maze.draw_level_2()
                            player.kolizje(maze.linie2)
                        if player.poziom == 3:
                            player.color_ = (255, 69, 0)
                            maze.set_color((0, 255, 0))
                            maze.draw_level_3()
                            player.kolizje(maze.linie3)
                        if player.poziom == 4:
                            player.color_=	(0, 255, 255)
                            maze.set_color((255, 0, 0))
                            maze.draw_level_4()
                            player.kolizje(maze.linie4)
                        if player.poziom == 5:
                            player.color_=(0, 255, 255)
                            maze.set_color((255, 165, 0))
                            maze.draw_level_5()
                            maze.move()
                            player.kolizje(maze.linie51)
                            player.kolizje(maze.linie5)
                            
                        player.sterowanie(dx, dy)
                        if pygame.Rect(player.x_, player.y_, player.width_, player.height_).colliderect(pygame.Rect(332, 0, 18, 10)) == True:
                            player.win(screen, maze)
                        
                        player.napisy(screen, font_style)
                        player.draw()
                        #META
                        pygame.draw.rect(screen, (255, 255, 255), [332, 0, 18, 10]) 

                        if player.poziom > 5:
                            screen.blit(tlo_wygrana.image, tlo_wygrana.rect)
                            self.sterowanie_oknem(player)

                    if player.zycia <= 0:
                        screen.blit(tlo_porazka.image, tlo_porazka.rect)
                        self.sterowanie_oknem(player)

                    pygame.display.update()

