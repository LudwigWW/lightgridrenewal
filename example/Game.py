#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
counter = 0

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
SPEED = 5
SCORE = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")
foreground = pygame.image.load("Foreground.png")
# foregroundCenter = (SCREEN_WIDTH/2, SCREEN_HEIGHT-foreground.get_rect().height/2)


#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Road(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.images = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png'), pygame.image.load('R10.png'), pygame.image.load('R11.png'), pygame.image.load('R12.png')]
        self.rect = self.images[0].get_rect()
        self.counter = 0
        self.index = 0
        self.frames = len(self.images)-1
        self.image = self.images[self.index]
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-self.rect.height/2)

    def move(self, inc):
        self.counter += inc
        if (self.counter > 100):
            self.counter -= 100
            self.index += 1
            if(self.index > self.frames):
                self.index = 0

        self.image = self.images[self.index]


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED/2)
        if (self.rect.bottom > (SCREEN_HEIGHT+100)):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player1.png")
        self.image = pygame.transform.scale_by(self.image, 0.95)
        self.rect = self.image.get_rect()
        self.rect.center = (160, SCREEN_HEIGHT - 50)
        self.other = 0
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > -50:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  

class Background(pygame.sprite.Sprite):
    def __init__(self, shifted):
        super().__init__() 
        self.image = pygame.image.load("Background.png")
        self.image = pygame.transform.scale_by(self.image, (0.3, 0.3))
        self.rect = self.image.get_rect()
        self.bgCounter = 0
        width = self.rect.width
        print(width)
        self.rect.center = (SCREEN_WIDTH/2, self.rect.height/2)
        if (shifted):
            self.rect.center = (SCREEN_WIDTH/2-width, self.rect.height/2)
       
    def set_other(self, other):
        self.other = other

    def get_rect(self):
        return self.rect

    def move(self, dist):
        self.bgCounter += dist
        pixelDist = self.bgCounter // 100
        if (self.bgCounter > 100):
            self.bgCounter -= (100*pixelDist)
            
        self.rect.move_ip(pixelDist, 0)

        # print(self.rect.bottomleft)
        # print(self.other.rect.bottomleft)
    
    def reset(self):
        if (self.rect.bottomleft[0] > (SCREEN_WIDTH)):
            self.rect.bottomleft = (self.other.rect.bottomleft[0] - self.rect.width, self.other.rect.bottomleft[1])


#Setting up Sprites        
P1 = Player()
E1 = Enemy()

#Setting up Background
BG = Background(False)
BG2 = Background(True)
BG.set_other(BG2)
BG2.set_other(BG)
R = Road()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
# all_sprites.add(BG)

bg_sprites = pygame.sprite.Group()
bg_sprites.add(BG)
bg_sprites.add(BG2)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#Game Loop
while True:
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 1      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    #Moves and Re-draws all Sprites


    for entity in bg_sprites:
        entity.move(SPEED)
    
    for entity in bg_sprites:
        entity.reset()
        DISPLAYSURF.blit(entity.image, entity.rect)

    DISPLAYSURF.blit(foreground, (7,10))


    R.move(SPEED)
    DISPLAYSURF.blit(R.image, R.rect)

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.1)
                
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
        
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        for entity in bg_sprites:
            entity.kill() 
        R.kill()
        time.sleep(1)
        pygame.quit()
        sys.exit()        
        

    if (counter > 100):
        print(FramePerSec.get_fps())
        counter = 0
    else:
        counter += 1
    pygame.display.update()
    FramePerSec.tick(FPS)
