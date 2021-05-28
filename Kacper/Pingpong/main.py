import pygame as pg
import sys


if __name__ == '__main__':
    max_fps = 20
    pg.init()
    window = pg.display.set_mode((480,320))
    box = pg.Rect(10,10,50,50)
    clock = pg.time.Clock()
    d = 0.0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit(0)
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                sys.exit(0)

        d += clock.tick()/1000.0
        while d > 1/max_fps:
            d -= 1/max_fps

            keys = pg.key.get_pressed()
            if keys[pg.K_d]:
                box.x += 4
            if keys[pg.K_s]:
                box.y += 4
            if keys[pg.K_w]:
                box.y -= 4
            if keys[pg.K_a]:
                box.x -= 4

        window.fill((0,0,0))
        pg.draw.rect(window, (0,150,255),box)
        pg.display.flip()
