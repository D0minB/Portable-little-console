#!/usr/bin/python
import spidev
import time
import os
import pygame
import RPi.GPIO as GPIO
from pygame.math import Vector2
from MCP3008_class import MCP3008

pygame.init()
pygame.mouse.set_visible(0)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(1,2)
spi.max_speed_hz=1000000

font30 = pygame.font.SysFont("dejavuserif", 30)
font20 = pygame.font.SysFont("dejavuserif", 20)
font15 = pygame.font.SysFont("dejavuserif", 15)

red = (255, 0, 0)
yellow = (255, 255, 0)
green = (26, 255, 26)
grey = (122, 154, 175)
u_channel = 6
left_switch = 32

adc = MCP3008()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(left_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP) 

  
def draw_text(text, font, color, position):
    t = font.render(text, True, color)
    text_rect = t.get_rect(center=(position.x, position.y))
    screen.blit(t, text_rect)
    pygame.display.update(text_rect.x, text_rect.y, text_rect.width, text_rect.height)
    
def critical_state():
    screen.fill((0, 0, 0))
    t = 10
    
    for i in range(10):
        screen.fill((0, 0, 0))
        draw_text("KRYTCZNY POZIOM BATERII", font30, red, Vector2((screen.get_width()/2, screen.get_height()/2 - 30)))
        draw_text("WYŁĄCZENIE ZA  "+ str(t - i), font20, red, Vector2((screen.get_width()/2, screen.get_height()/2 + 30)))
        pygame.display.update()
        time.sleep(1)
    
    os.system("sudo shutdown -h now")
    
        
def warning():
    screen.fill((0,0,0))
    draw_text("NISKI POZIOM BATERII", font30, yellow, Vector2(screen.get_width()/2,screen.get_height()/2-60))
    draw_text("PODŁĄCZ ŁADOWARKĘ", font20, yellow, Vector2(screen.get_width()/2,screen.get_height()/2))
    draw_text("NACIŚNIJ LEWY PRZYCISK, ABY KONTYNUOWAĆ", font15, grey, Vector2((screen.get_width()/2, screen.get_height() - 50)))
    pygame.display.update()
        
    wait = True
    while wait:
        if GPIO.input(left_switch) == 0:
            wait = False
              
    #return to previous state

    
def charged_battery():
    screen.fill((0,0,0))
    draw_text("BATERIA NAŁADOWANA", font30, green,Vector2(screen.get_width()/2,screen.get_height()/2-60))
    draw_text("ODŁĄCZ ŁADOWARKĘ", font20, green,Vector2(screen.get_width()/2,screen.get_height()/2))
    draw_text("NACIŚNIJ LEWY PRZYCISK, ABY KONTYNUOWAĆ", font15, grey, Vector2((screen.get_width()/2, screen.get_height() - 50)))
    pygame.display.update()
        
    wait = True
    while wait:
        if GPIO.input(left_switch) == 0:
            wait = False
              
    #return to previous state

             
warning_val = 696 # 3,4V
critical_val = 655 # 3,2V
charged_val =  840 # 4,1V

while True:
    u = adc.read(u_channel)
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
            pygame.quit()
            sys.exit()
            
    if u < warning_val:
        if u < critical_val: 
            critical_state()
        else:
            warning()
    elif u > charged_val:
        charged_battery()
        
    time.sleep(60) #measurement cycle - 60sec
          
        
  