import pygame as pg
import sys
from pygame.math import Vector2

class Rocket(object):

    def __init__(self,game):
        self.game = game
        self.speed = 1.2
        self.gravity = 0.5
        size = self.game.window.get_size()
        self.pos = Vector2(size[0]/2,size[1]/2)
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)

    def add_force(self, force):
        self.acc += force

    def tick(self):
        #Input
        pressed = pg.key.get_pressed()
        if pressed[pg.K_w]:
            self.add_force(Vector2(0,-self.speed))
        if pressed[pg.K_s]:
            self.add_force(Vector2(0,self.speed))
        if pressed[pg.K_a]:
            self.add_force(Vector2(-self.speed,0))
        if pressed[pg.K_d]:
            self.add_force(Vector2(self.speed,0))

        #Phisics
        #Friction
        self.vel *= 0.8
        #Gravity
        self.vel -= Vector2(0,-self.gravity)

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

    def draw(self):
        points = [Vector2(0,-10), Vector2(5,5), Vector2(-5,-5)]
        angle = self.vel.angle_to(Vector2(0,1))
        points = [p.rotate(angle) for p in points]
        points = [Vector2(p.x,p.y*-1) for p in points]
        points = [self.pos + p*2 for p in points]
        pg.draw.polygon(self.game.window, (0,100,255), points)



class Game(object):

    def __init__(self):
        #Config
        self.maxFPS = 20.0

        #Init
        pg.init()
        self.resolution = (480,320)
        self.window = pg.display.set_mode(self.resolution)
        self.FPSclock = pg.time.Clock()
        self.FPSdelta = 0.0

        #Objects
        self.player = Rocket(self)

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
        self.player.tick()

    def draw(self):
        self.player.draw()

if __name__ == '__main__':
    Game()