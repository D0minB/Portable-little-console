# PLANE GAME
# AUTHOR: DOMINIK BOGIELCZYK

import pygame
from pygame.math import Vector2
import time
import sys
import random
import RPi.GPIO as GPIO
from plane_class import Plane
from MCP3008_class import MCP3008

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.IN,pull_up_down=GPIO.PUD_UP)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Portable little console')
pygame.mouse.set_visible(0)

font70 = pygame.font.SysFont("calibri", 70)
font40 = pygame.font.SysFont("calibri", 40)
font20 = pygame.font.SysFont("calibri", 20)

def write_text(font,text,color,pos):
    text = font.render(text, True, color)
    screen.blit(text, text.get_rect(center=(pos.x, pos.y)))


def plane_game():
# NEW TARGETS GENERATING
    def targets_generating():
        new_targets_pos = []
        for i in range(random.randint(4, 7)):  # 6 TO 12 - NUMBER OF THE NEW TARGETS
            n = random.randint(1, 14) #new target position choosing

            while n in new_targets_pos:  # ADD UNIQUE POSITION OF THE TARGET
                n = random.randint(1, 14)

            new_targets_pos.append(n)

        for target_pos in new_targets_pos:  # ADD UNIQUE TARGETS POSITIONS TO LIST
            targets.append(Vector2(target_pos * 22 + 8, 8))

        return targets
            
    dt = 0.0
    fps= 18.0
    clock = pygame.time.Clock()

    adc = MCP3008()

    plane = Plane(screen)
    targets = []
    bullets=[]

    points=0
    
    n=0
    
    new_record=0

    last_targets_time = time.time()
    new_targets_time=2.5

    # GENERATE FIRST TARGETS
    targets_generating()
    
    with open("record.txt") as f:
        record = list(f)
        record = ''.join(record) # converting list into string
        record = int(record)
        
    first_frame=1
    
    while True:
        dt += clock.tick() / 1000.0
        result_change=0

        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()
                
        
        
        while dt > 1 / fps:
            dt -= 1 / fps
            targets_move=0
          
            # plane move
            delta_x = 0
            # plane controlling
            if pygame.key.get_pressed()[pygame.K_LEFT] or adc.read(channel=2)<=50:
                delta_x -= 240/fps
            if pygame.key.get_pressed()[pygame.K_RIGHT] or adc.read(channel=2)>=700:
                delta_x += 240/fps
            plane.move(delta_x)
            
            if n>=1:
                n=0
            else:
                n+=1
            
            #new bullet every 2 frames
            if n==1 and (GPIO.input(37) == 0 or pygame.key.get_pressed()[pygame.K_SPACE]):
                bullets.append(Vector2(plane.get_position()[0] + 10, plane.get_position()[1] - 10))

            #bullets move in y-axis
            for bullet in bullets:
                bullet.y-=250/fps

            # new targets 
            if time.time() - last_targets_time > new_targets_time:
                last_targets_time = time.time()
                new_targets_time=0.98*new_targets_time
                targets_move=1

                # previous targets move in y-axis
                for target in targets:
                    target.y += 22

                # generate new targets
                targets_generating()


            #collision - target and bullet
            for target in targets:
                for bullet in bullets:
                    if pygame.Rect(target.x,target.y,20,20).colliderect(pygame.Rect(bullet.x-5,bullet.y-5,10,10)):
                        target.x=-30
                        bullets.remove(bullet)
                        points+=1
                        result_change=1
            
            for i in range(len(targets)):
                if i<len(targets):
                    if targets[i].x==-30:
                        targets.pop(i)
            
            #remove out of screen bullets
            for i in range(len(bullets)):
                if i<len(bullets): 
                    if bullets[i].y<15:
                        bullets.pop(i)

            # cleaning screen
            screen.fill((0, 0, 0))

            plane.draw()

            #frame
            width=6
            pygame.draw.lines(screen, (255, 255, 255), 1,[(width/2, width/2), (16*22 + 8, width/2), (16*22 + 8, screen.get_height()-width/2),(width/2,screen.get_height()-width/2)], width)

            for target in targets:
                pygame.draw.rect(screen, (255, 255, 0),pygame.Rect(target.x,target.y,20,20))

            for bullet in bullets:
                pygame.draw.circle(screen, (255, 20, 0),[int(bullet.x),int(bullet.y)],5)
                
            if points>record:
                write_text(font70,str(points),(0, 255, 0),Vector2(screen.get_width() -50, 50))
                new_record=1

            else:
                write_text(font70,str(record),(0, 255, 0),Vector2(screen.get_width() -50, 50))
            
            write_text(font20,"RECORD",(0, 255, 0),Vector2(screen.get_width() - 50, 100))
            
            write_text(font70,str(points),(255, 255, 0),Vector2(screen.get_width() -50, screen.get_height()/2+40))
            write_text(font20,"POINTS",(255, 255, 0),Vector2(screen.get_width() - 50, screen.get_height() / 2 +90))

            plane_position=plane.get_position()
            
            #end screen
            if len(targets)>0 and targets[0].y > plane_position.y-15:
                screen.fill((0, 0, 0))
 
                write_text(font20,"JOYSTICK: LEFT TO QUIT OR RIGHT TO NEW GAME",(255, 255, 0),Vector2(screen.get_width()/2, 220))

                if new_record==1:
                    f=open("record.txt","w")
                    f.write(str(points))
                    
                    write_text(font40,"NEW RECORD",(0, 255, 0),Vector2(screen.get_width()/2, 75))
                    write_text(font70,str(points),(0, 255, 0),Vector2(screen.get_width()/2, 150))
                    
                else:
                    write_text(font40,"YOUR SCORE:",(255, 255, 0),Vector2(screen.get_width()/2, 75))
                    write_text(font70,str(points),(255, 255, 0),Vector2(screen.get_width()/2, 150))
                    
                pygame.display.update()

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or adc.read(channel=2)<=50:
                            pygame.quit()
                            sys.exit()
                        if adc.read(channel=2)>=700:
                            plane_game()

            if first_frame or points>record:
                pygame.display.update() #pygame.Rect(screen.get_width()-90, 20,90,70
                
            
            if first_frame==1:
                pygame.display.update()
                
            elif result_change==1:
                pygame.display.update(pygame.Rect(screen.get_width()-90, screen.get_height()/2-10,90,70))
                

            pygame.display.update(pygame.Rect(0,0,360,screen.get_height()))
            
            first_frame=0
        

plane_game()
