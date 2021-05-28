import pygame as pg


if __name__ == '__main__':
    window = pg.display.set_mode((480,320))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit(0)

        pg.draw.rect(window, (0,150,255), pg.Rect(10,50,200,100))
        pg.display.flip()