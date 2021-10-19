import pygame
import sys

class Button(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("textures/"+file).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self,file):
        self.image = pygame.image.load("textures/"+file).convert()


pygame.init()
pygame.mouse.set_visible(0)
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((480, 320))
background = pygame.sprite.Group()


def draw_text(text, font, color, position):
    t = font.render(text, True, color)
    text_rect = t.get_rect(center=(position.x, position.y))
    screen.blit(t, text_rect)
    pygame.display.update(text_rect.x, text_rect.y-5, text_rect.width, text_rect.height+10)


def menu():

    screen.fill((0, 0, 0))
    names = ["nowa_gra_on.png","nowa_gra_off.png","rekordy_on.png","rekordy_off.png","muzyka_on_y.png",
             "muzyka_on_g.png","muzyka_off_y.png","muzyka_off_g.png"]
    buttons = pygame.sprite.Group()

    state = 1
    sound = 0

    for i in range(len(names)):
        if i == 0 or i == 3:
            buttons.add(Button(names[i],screen.get_width()/2, 60 + 80*len(buttons)))
        if sound == 1 and i == 4:
            buttons.add(Button(names[i], screen.get_width() / 2, 60 + 80 * len(buttons)))
        if sound == 0 and i == 6:
            buttons.add(Button(names[i], screen.get_width() / 2, 60 + 80 * len(buttons)))

    buttons.draw(screen)
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
                            if state < 1:
                                state = 1

                        if pygame.key.get_pressed()[pygame.K_s]:
                            state += 1
                            if state > 3:
                                state = 3

                        if pygame.key.get_pressed()[pygame.K_SPACE] and state == 3:
                            sound = not sound

                        state1 = [0, 3]
                        state2 = [1, 2]
                        state3 = [1, 3]

                        if sound:
                            state1.append(4)
                            state2.append(4)
                            state3.append(5)
                        else:
                            state1.append(6)
                            state2.append(6)
                            state3.append(7)

                        j = 0
                        for b in buttons:
                            if state == 1:
                                b.update(names[state1[j]])
                            if state == 2:
                                b.update(names[state2[j]])
                            if state == 3:
                                b.update(names[state3[j]])


                            j += 1

                        screen.fill((0, 0, 0))
                        buttons.draw(screen)
                        pygame.display.update()



                dt -= 1 / 20





menu()
