import pygame as pg
import sys
from pygame.math import Vector2
import random
from spidev import SpiDev

class MCP3008:
    def __init__(self, bus=1, device=2):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000  # 1MHz

    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000  # 1MHz

    def read(self, channel=0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def close(self):
        self.spi.close()

adc = MCP3008()

class Rakieta(object):

    def __init__(self,game,nr):
        self.game = game
        self.nr = nr
        self.width = 5
        self.lenght = 70
        self.control = 500
        self.size = self.game.window.get_size()
        if nr == 1:
            self.pos = Vector2(0,self.size[1]/2-self.lenght/2)
        else:
            self.pos = Vector2(self.size[0]-self.width,self.size[1]/2-self.lenght/2)
        self.vel = Vector2(0, 1.5)
        self.hitbox = pg.Rect(self.pos[0],self.pos[1],self.width,self.lenght)

    def tick(self):
        if self.nr == 1:
            self.control = adc.read(channel=1)
            if self.hitbox.colliderect(self.game.UP_WALL):
                self.pos = Vector2(0,5)
            if self.hitbox.colliderect(self.game.DOWN_WALL):
                self.pos = Vector2(0,self.size[1]-5-self.lenght)
            if self.control<450:
                self.pos += 0.2*self.vel
            if self.control<300:
                self.pos += 0.4*self.vel
            if self.control<200:
                self.pos += 0.7*self.vel
            if self.control<100:
                self.pos += self.vel
            if self.control > 550:
                self.pos -= 0.2 * self.vel
            if self.control > 750:
                self.pos -= 0.4 * self.vel
            if self.control > 950:
                self.pos -= 0.7 * self.vel
            if self.control > 1000:
                self.pos -= self.vel
        else :
            self.control = adc.read(channel=4)
            if self.hitbox.colliderect(self.game.UP_WALL):
                self.pos = Vector2(self.size[0]-self.width,5)
            if self.hitbox.colliderect(self.game.DOWN_WALL):
                self.pos = Vector2(self.size[0]-self.width,self.size[1]-5-self.lenght)
            if self.control < 450:
                self.pos += 0.2 * self.vel
            if self.control < 300:
                self.pos += 0.4 * self.vel
            if self.control < 200:
                self.pos += 0.7 * self.vel
            if self.control < 100:
                self.pos += self.vel
            if self.control > 550:
                self.pos -= 0.2 * self.vel
            if self.control > 750:
                self.pos -= 0.4 * self.vel
            if self.control > 950:
                self.pos -= 0.7 * self.vel
            if self.control > 1000:
                self.pos -= self.vel

    def draw(self):
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.width, self.lenght)
        pg.draw.rect(self.game.window,(0,200,255), self.hitbox)

class ball(object):

    def __init__(self,game):
        self.game = game
        self.diameter = 15
        self.direction = random.randint(1,2)
        if self.direction == 1:
            self.direction = -1
        else:
            self.direction = 1
        self.size = self.game.window.get_size()
        self.pos = Vector2(self.size[0]/2-self.diameter/2,self.size[1]/2-self.diameter/2)
        self.vel = Vector2(4,4)
        self.hitbox = pg.Rect(self.pos[0],self.pos[1],self.diameter,self.diameter)

    def tick(self):
        if self.hitbox.colliderect(self.game.UP_WALL):
            self.pos = Vector2(self.pos[0],5+self.diameter/2)
            self.vel = self.vel.reflect(Vector2(0,-1))
        if self.hitbox.colliderect(self.game.DOWN_WALL):
            self.pos = Vector2(self.pos[0],self.size[1]-5-self.diameter)
            self.vel = self.vel.reflect(Vector2(0,1))
        if self.hitbox.colliderect(self.game.R1.hitbox):
            self.pos = Vector2(self.game.R1.width,self.pos[1])
            self.vel = self.vel.reflect(Vector2(1, 0))
        if self.hitbox.colliderect(self.game.R2.hitbox):
            self.pos = Vector2(self.size[0] - self.game.R1.width - self.diameter, self.pos[1])
            self.vel = self.vel.reflect(Vector2(-1, 0))
        if self.pos[0] > self.size[0] or self.pos[0] < 0:
            self.pos = Vector2(self.size[0]/2-self.diameter/2,self.size[1]/2-self.diameter/2)
            self.direction *= -1
        self.pos += self.vel * self.direction

    def draw(self):
        self.hitbox = pg.Rect(self.pos[0],self.pos[1],self.diameter,self.diameter)
        #pg.draw.rect(self.game.window,(0,255,0),self.hitbox)
        pg.draw.circle(self.game.window,(255,255,255),(int(self.pos[0])+int(self.diameter/2),int(self.pos[1])+int(self.diameter/2)),int(self.diameter/2))


class Pingpong(object):

    def __init__(self):
        #Config
        self.maxFPS = 20

        #Init
        pg.init()
        self.resolution = (480,320)
        self.window = pg.display.set_mode((0,0),pg.FULLSCREEN)
        self.FPSclock = pg.time.Clock()
        self.FPSdelta = 0.0

        #Objects
        self.R1 = Rakieta(self,1)
        self.R2 = Rakieta(self,2)
        self.BALL = ball(self)
        self.UP_WALL = pg.Rect(0,0,self.window.get_size()[0],5)
        self.DOWN_WALL = pg.Rect(0,self.window.get_size()[1]-5,self.window.get_size()[0],5)

        while True:
            #Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit(0)
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    sys.exit(0)

            #Ticks
            self.FPSdelta += self.FPSclock.tick() / 1000.0
            while self.FPSdelta > 1 / self.maxFPS:
                self.tick()
                self.FPSdelta -= 1 / self.maxFPS

            #Drawing
            self.window.fill((0, 0, 0))
            self.draw()
            pg.display.flip()


    def tick(self):
        self.R1.tick()
        self.R2.tick()
        self.BALL.tick()

    def draw(self):
        self.R1.draw()
        self.R2.draw()
        self.BALL.draw()
        pg.draw.rect(self.window,(255,0,0),self.UP_WALL)
        pg.draw.rect(self.window, (255, 0, 0), self.DOWN_WALL)

if __name__ == '__main__':
    Pingpong()