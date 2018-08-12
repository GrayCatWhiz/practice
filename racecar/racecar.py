import time
import os
import platform
import sys
import random

import pygame
pygame.init()


screen_size = (500, 500)
scr_sizex, scr_sizey = screen_size
FPS = 60

white = (255, 255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
maroon = (128, 0, 0)
lime = (0, 255, 0)
green = (0, 128, 0)

car_width = 73

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(screen_size)
        self.fps_clock = pygame.time.Clock()
        pygame.display.set_caption('PyGame Tutorial -> https://pythonprogramming.net')
    

        self.x, self.y = screen_size
        self.x = self.x * 0.40
        self.y = self.y * 0.8
        self.x_change = 0
        self.car_speed = 0

        self.obstacle_sx = random.randrange(0, scr_sizex)
        self.obstacle_sy = -scr_sizey
        self.obstacle_speed = 7
        self.obstacle_x = 80
        self.obstacle_y = 80
        self.dodged = 0

        self.carImg = pygame.image.load('racecar.png')

        self.game_intro()
    
    def game_intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                # IF CLOSE BUTTON IS CLICKED
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    intro = False
                
                # IF A HOTKEY IS PRESSED
                if event.type == pygame.KEYDOWN:
                    # IF SPACE IS PRESSED
                    if event.key == pygame.K_SPACE:
                        self.game_run()
                    # IF ESCAPE IS PRESSED
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                        intro = False
            # BACKGROUND COLOR
            self.screen.fill(white)
            # GET MOUSE POSITION
            mouse = pygame.mouse.get_pos()
            # CHECK IF MOUSE IS CLICKED OR NOT
            click = pygame.mouse.get_pressed()
            largeText = pygame.font.Font('freesansbold.ttf', 60)
            TextSurf, TextRect = self.text_objects('PyGame Tutorial', largeText)
            TextRect.center = ((scr_sizex / 2), (scr_sizey / 2))
            # SHOW THE TEXT IN THE CENTER
            self.screen.blit(TextSurf, TextRect)

            # BUTTON
            # IF MOUSE HOVER CHANGE COLOR SHADE
            if 50 + 100 > mouse[0] > 50 and 350 + 100 > mouse[1] > 350:
                pygame.draw.rect(self.screen, lime, (50, 350, 100, 50))
                # IF MOUSE IS CLICKED DURING MOUSE HOVER RUNS THE GAME
                if click[0] == 1:
                    self.game_run()
            else:
                pygame.draw.rect(self.screen, green, (50, 350, 100, 50))
            if 350 + 100 > mouse[0] > 350 and 350 + 100 > mouse[1] > 350:
                pygame.draw.rect(self.screen, red, (350, 350, 100, 50))
                # IF MOUSE IS CLICKED DURING MOUSE HOVER CLOSES THE GAME
                if click[0] == 1:
                    pygame.quit()
                    quit()
                    intro = False
            else:
                pygame.draw.rect(self.screen, maroon, (350, 350, 100, 50))

            # TEXT FOR BUTTON
            smallText = pygame.font.Font('freesansbold.ttf', 20)
            TextSurf1, TextRect1 = self.text_objects('Start', smallText)
            TextRect1.center = ((50+(100 / 2)), (350+(50 / 2)))
            # SHOWS THE TEXT IN THE CENTER OF THE START BUTTON
            self.screen.blit(TextSurf1, TextRect1)
            TextSurf2, TextRect2 = self.text_objects('Quit', smallText)
            TextRect2.center = ((350+(100 / 2)), (350+(50 / 2)))
            # SHOWS THE TEXT IN THE CENTER OF THE QUIT BUTTON
            self.screen.blit(TextSurf2, TextRect2)

            # REFRESHES SCREEN PER LOOP
            pygame.display.update()
            # FPS
            self.fps_clock.tick(15)
    
    def game_run(self):
        null = False
        while not null:
            for event in pygame.event.get():
                # IF CLOSE BUTTON IS CLICKED
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    null = True
                
                # IF A HOTKEY IS PRESSED
                if event.type == pygame.KEYDOWN:
                    # LEFT ARROW
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.x_change = -5 + -self.car_speed
                    # RIGHT ARROW
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.x_change = 5 + self.car_speed
                    # LEFT AND RIGHT ARROW
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a and event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.x_change = -5 + -self.car_speed
                    # RIGHT AND LEFT ARROW
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d and event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.x_change = 5 + self.car_speed
                    
                    # IF ESCAPE HOTKEY IS PRESSED CLOSES THE GAME
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                # IF A HOTKEY IS RELEASED AFTER PRESSED
                if event.type == pygame.KEYUP:
                    # IDLE STATE
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                        self.x_change = 0
            
            # GET THE CURRENT POSITION FOR THE CAR
            self.x += self.x_change
            # BACKGROUND COLOR
            self.screen.fill((white))

            # GENERATE THE OBSTACLE
            self.obstacle()
            # SET THE OBSTACLE SPEED
            self.obstacle_sy += self.obstacle_speed
            # PLACE THE CAR
            self.car(self.x, self.y)
            # SETS THE GAME SCORE
            self.game_score(self.dodged)

            # IF YOU HIT THE BORDER
            if self.x >= self.y or self.x < 0:
                self.x_change = 0
            
            # SPAWN THE OBSTACLE RANDOMLY AND INCREASE THE SPEED PER OBSTACLE DODGED
            if self.obstacle_sy > scr_sizey:
                self.obstacle_sy = 0 - self.obstacle_y
                self.obstacle_sx = random.randrange(0, scr_sizex)
                self.dodged += 1
                self.obstacle_speed += 1
                self.car_speed += 1
                # RESET THE SPEED INTO ORIGINAL PER 10 OBSTACLE DODGED
                if self.dodged % 11 == 0:
                    self.obstacle_speed = 7
                    self.car_speed = 0
            
            # IF YOU HIT THE OBSTACLE
            if self.y < self.obstacle_sy + self.obstacle_y:
                if self.x > self.obstacle_sx and self.x < self.obstacle_sx + self.obstacle_x or self.x + car_width > self.obstacle_sx and self.x + car_width < self.obstacle_sx + self.obstacle_x:
                    self.text('You Crashed!')
            
            # REFRESHES SCREEN PER LOOP
            pygame.display.update()
            self.fps_clock.tick(FPS)
        
    def car(self, x, y):
        # THE CAR MODEL
        self.screen.blit(self.carImg, (x,y))
        pygame.display.update()
    
    def text_objects(self, text, font):
        self.textSurface = font.render(text, True, black)
        return self.textSurface, self.textSurface.get_rect()
    
    def text(self, text):
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((scr_sizex / 2), (scr_sizey / 2))
        # SHOWS THE TEXT IN THE CENTER
        self.screen.blit(TextSurf, TextRect)
        
        pygame.display.update()
        time.sleep(2)

        self.__init__()
    
    def obstacle(self):
        # CREATES THE OBSTACLE MODEL
        pygame.draw.rect(self.screen, black, (self.obstacle_sx, self.obstacle_sy, self.obstacle_x, self.obstacle_y))
    
    def game_score(self, count):
        # GAME SCORE
        font = pygame.font.SysFont(None, 25)
        text = font.render('Dodged: {0}'.format(str(count)), True, black)
        self.screen.blit(text, (0,0))

if __name__ == '__main__':
    Game()
    pygame.quit()
    quit()