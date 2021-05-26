import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([480, 320])

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((0, 0, 0))

    # Draw a solid blue circle in the center

    pygame.draw.line(screen, (255, 0, 255),
                     (230, 320), (230, 200), True)
    pygame.draw.line(screen, (255, 0, 255),
                     (250, 320), (250, 220), True)
    pygame.draw.line(screen, (255, 0, 255),
                     (250, 220), (300, 220), True)
    pygame.draw.line(screen, (255, 0, 255),
                     (230, 200), (280, 200), True)
    pygame.draw.line(screen, (255, 0, 255),
                     (300, 220), (300, 0), True)
    pygame.draw.line(screen, (255, 0, 255),
                     (280, 200), (280, 100), True)
    pygame.draw.line(screen, (255, 0, 255),
                     (280, 200), (280, 50), True)
    pygame.draw.line(screen, (255, 0, 255),
                     (280, 50), (290, 50), True)
    pygame.draw.line(screen, (255, 0, 255),
                     (290, 50), (290, 0), True)
    pygame.display.update()
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()