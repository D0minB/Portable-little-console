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
GPIO.setup(33,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(31,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(32,GPIO.IN,pull_up_down=GPIO.PUD_UP)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Portable little console')
pygame.mouse.set_visible(0)

font70 = pygame.font.SysFont("calibri", 70)
font40 = pygame.font.SysFont("calibri", 40)
font20 = pygame.font.SysFont("calibri", 20)

adc = MCP3008()

def draw_text(font,text,color,pos):
    text = font.render(text, True, color)
    screen.blit(text, text.get_rect(center=(pos.x, pos.y)))
    
def start_screen(plane):
    screen.fill((0, 0, 0))
    width=6
    pygame.draw.lines(screen, (255, 255, 255), 1,[(width/2, width/2), (16*22 + 8, width/2), (16*22 + 8, screen.get_height()-width/2),(width/2,screen.get_height()-width/2)], width)
    plane.draw()
    
    w=15*22+8
    draw_text(font40,"PLANE", (255, 255, 255), Vector2((w/2, 30)))
    draw_text(font20,"STEROWANIE:", (255, 255, 0),
              Vector2(w/2, screen.get_height() / 2 - 50))
    draw_text(font20,"STRZAŁ - PRZYCISK 'W GÓRĘ'", (255, 255, 0),
              Vector2(w/2, screen.get_height() / 2 - 20))
    draw_text(font20,"LEWO-PRAWO - JOYSTICK LUB PRZYCISKI", (255, 255, 0),
              Vector2(w/2, screen.get_height() / 2 + 10))
    draw_text(font20,"PRZYCISK 'W DÓŁ' - ROZPOCZNIJ GRĘ", (255, 255, 255),
              Vector2(w/2, screen.get_height() / 2 + 60))

    pygame.display.update()

    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_SPACE] or GPIO.input(32) == 0:
                start_game = True 
                
    
def end_screen(new_record,points):
    screen.fill((0, 0, 0)) 

    if new_record==1:
        f=open("record.txt","w")
        f.write(str(points))
                    
        draw_text(font40,"NOWY REKORD",(0, 255, 0),Vector2(screen.get_width()/2, 75))
        draw_text(font70,str(points),(0, 255, 0),Vector2(screen.get_width()/2, 150))
        draw_text(font20,"JOYSTICK: LEWO - WYJDZ, PRAWO - NOWA GRA",(0, 255, 0),Vector2(screen.get_width()/2, 220))
                    
    else:
        draw_text(font40,"TWÓJ WYNIK:",(255, 255, 0),Vector2(screen.get_width()/2, 75))
        draw_text(font70,str(points),(255, 255, 0),Vector2(screen.get_width()/2, 150))
        draw_text(font20,"JOYSTICK: LEWO - WYJDZ, PRAWO - NOWA GRA",(255, 255, 0),Vector2(screen.get_width()/2, 220))
                    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or adc.read(channel=2)<=50 or pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if adc.read(channel=2)>=700:
                plane_game()


def plane_game():
# NEW TARGETS GENERATING
    def targets_generating():
        new_targets_pos = []
        for i in range(random.randint(4, 7)):  # 6 TO 12 - NUMBER OF THE NEW TARGETS
            n = random.randint(1, 14) #new target position choosing

            while n in new_targets_pos:  # ADD UNIQUE POSITION OF THE TARGET
                n = random.randint(1, 14)

            new_targets_pos.append(n)

        for target_pos in new_targets_pos:  # ADD UNIQUE TARGETS TO LIST
            targets.append(pygame.Rect(target_pos * 22 + 8, 8,20,20))

        return targets
            
    dt = 0.0
    fps= 30.0
    clock = pygame.time.Clock()
    start = True


    plane = Plane(screen)
    targets = []
    bullets=[]

    points=0
    
    new_record=0

    last_targets_time = time.time()
    new_targets_time=2.5
    new_bullets_time=0.1
    last_bullets_time=time.time()
    bullets_velocity=11

    # GENERATE FIRST TARGETS
    targets_generating()
    
    with open("record.txt") as f:
        record = list(f)
        record = ''.join(record) # converting list into string
        record = int(record)
        
    first_frame=1
    
    while True:
        dt += clock.tick() / 1000.0
        
        t1 = time.time()
        if start == 1:
            start_screen(plane)
        start = 0
        t2 = time.time()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                pygame.quit()
                sys.exit()
    
        
        while dt > 1 / fps:
            result_change=0
            run=time.time()
            dt -= 1 / fps
            targets_move=0
          
            # plane move
            delta_x = 0
            # plane controlling
            if GPIO.input(31) == 0 :#pygame.key.get_pressed()[pygame.K_LEFT]:# or adc.read(channel=2)<=50:
                delta_x -= 11
            if GPIO.input(33) == 0 : #pygame.key.get_pressed()[pygame.K_RIGHT]:# or adc.read(channel=2)>=700:
                delta_x += 11
            plane.move(delta_x)
            
            to_update=[]
            
            #collision - target and bullet
            for bullet in bullets:
                index = pygame.Rect(bullet.x-5,bullet.y-5,10,10).collidelist(targets)
                
                if index>=0:
                    to_update.append(pygame.Rect(targets[index]))
                    to_update.append(pygame.Rect(bullet.x-5,bullet.y-5,10,10))
                    targets.pop(index)
                    bullet.x=-30
                    points+=1
                    result_change=1
   
            for i in range(len(bullets)):
                if i<len(bullets):
                    if bullets[i].x==-30:
                        bullets.pop(i)
            
            #remove out of screen bullets
            for i in range(len(bullets)):
                if i<len(bullets): 
                    if bullets[i].y-5<bullets_velocity+10:
                        to_update.append(pygame.Rect(bullets[i].x-5,bullets[i].y-5,10,10))
                        bullets.pop(i)
            
            
            #new bullet 
            if time.time()-last_bullets_time>new_bullets_time and GPIO.input(37) == 0: # or pygame.key.get_pressed()[pygame.K_SPACE]):
                last_bullets_time=time.time()
                bullets.append(Vector2(plane.get_position()[0] + 10, plane.get_position()[1] - 10))

            # new targets 
            if time.time() - last_targets_time > new_targets_time:
                last_targets_time = time.time()
                new_targets_time=0.99*new_targets_time
                targets_move=1

                # previous targets move in y-axis
                for target in targets:
                    target.y += 22

                # generate new targets
                targets_generating()
  
            
            #bullets move in y-axis
            for bullet in bullets:
                bullet.y-=bullets_velocity
            
            
            # cleaning screen
            screen.fill((0, 0, 0))
            
            plane.draw()
            plane.update(delta_x)
            
            
            #frame
            width=6
            pygame.draw.lines(screen, (255, 255, 255), 1,[(width/2, width/2), (16*22 + 8, width/2), (16*22 + 8, screen.get_height()-width/2),(width/2,screen.get_height()-width/2)], width)

            for bullet in bullets:
                pygame.draw.circle(screen, (255, 20, 0),[int(bullet.x),int(bullet.y)],5)
                #bullet in actual position
                to_update.append(pygame.Rect(bullet.x-5,bullet.y-5,10,10))
                #erase bullet in previous postion
                to_update.append(pygame.Rect(bullet.x-5,bullet.y-5+bullets_velocity,10,10))

            
            for target in targets:
                pygame.draw.rect(screen, (255, 255, 0),target)
       
            
            plane_position=plane.get_position()
           
            
            #end screen
            if len(targets)>0 and targets[0].y > plane_position.y-15:
                end_screen(new_record,points)

            if targets_move == True:
                for t in targets:
                    y=t.y-22
                    if y<0:
                        y=0
                        
                    to_update.append(pygame.Rect(t.x,y,20,20+22))
                
                
            if first_frame==1:
                draw_text(font20,"REKORD",(255, 255, 0),Vector2(screen.get_width() - 50, 100))
                draw_text(font70,str(record),(255, 255, 0),Vector2(screen.get_width() -50, 50))
                draw_text(font20,"PKT.",(255, 255, 0),Vector2(screen.get_width() - 50, screen.get_height() / 2 +90))
                

                pygame.display.update() #we update all pixels
                
            elif result_change==True:
                if points>record:
                    draw_text(font70,str(points),(0, 255, 0),Vector2(screen.get_width() -50, 50))
                    draw_text(font70,str(points),(0, 255, 0),Vector2(screen.get_width() -50, screen.get_height()/2+40))
                    new_record=1
                    to_update.append(pygame.Rect(screen.get_width()-90, 20,90,70))    

                else:
                    draw_text(font70,str(record),(255, 255, 0),Vector2(screen.get_width() -50, 50))
                    draw_text(font70,str(points),(255, 255, 0),Vector2(screen.get_width() -50, screen.get_height()/2+40))
                    
                to_update.append(pygame.Rect(screen.get_width()-90, screen.get_height()/2-10,90,70))                
           
            pygame.display.update(to_update)
                
            
            first_frame=0

plane_game()
