import pygame
from MCP3008_class import MCP3008
import RPi.GPIO as GPIO
adc = MCP3008()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

left_switch = 32
right_switch = 33
GPIO.setup(left_switch, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_switch, GPIO.IN,pull_up_down=GPIO.PUD_UP)
class Player(pygame.Rect):

    def __init__(self,screen):
        self.x_=16
        self.y_=310
        self.screen_=screen
        self.zycia=3
        self.poziom=1
        self.width_=6
        self.height_=6
        self.color_=(255, 69, 0)
        self.counter_a=0





    def draw(self):
            pygame.draw.rect(self.screen_, self.color_, pygame.Rect(self.x_,self.y_,self.width_,self.height_))

    def move(self,dx,dy):
        if self.x_+dx-self.width_/2>0 and self.x_+ dx+self.width_/2 < 475 and self.y_+dy>0 and self.y_+dy<320-self.height_/2:
                self.x_+=dx
                self.y_+=dy

    def sterowanie(self,dx,dy):
        dx = 0
        dy = 0
        if adc.read(channel=5) > 600:
            dx += 2
        if adc.read(channel=5) < 50:
            dx -= 2
        if adc.read(channel=4) < 50:
            dy += 2
        if adc.read(channel=4) > 600:
            dy -= 2
        self.move(dx, dy)

    def kolizje(self, linie):
        for linia in linie:
            if linia[0] == linia[2]:
                dlugosc = abs(linia[3] - linia[1])
                szerokosc = 2
            if linia[1] == linia[3]:
                szerokosc = abs(linia[2] - linia[0])
                dlugosc = 2
            if pygame.Rect(self.x_, self.y_, self.width_, self.height_).colliderect(
                    pygame.Rect(linia[0], linia[1], szerokosc, dlugosc)) == True:
                self.x_ = 16
                self.y_ = 310
                self.zycia -= 1

    def win(self,screen):
        self.x_ = 16
        self.y_ = 310
        self.poziom += 1

    def napisy(self,screen,font_style):
        text_zycia = font_style.render("Życia: " + str(self.zycia), True, (255, 0, 0))
        screen.blit(text_zycia, [0, 0])
        text_zycia = font_style.render("Poziom: " + str(self.poziom), True, (255, 0, 0))
        screen.blit(text_zycia, [0, 20])