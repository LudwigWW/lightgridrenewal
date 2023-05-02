#Imports
import pygame, sys
from pygame.locals import *
import random, time
from math import sin, radians

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 600
FramePerSec = pygame.time.Clock()
counter = 0
eventCounter = 0

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
obstacleImage = pygame.image.load("Enemy.png")
bushImage = pygame.image.load("Bush1.png")
treeImage = pygame.image.load("Tree1.png")

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
        self.reset()

    def reset(self):
        self.scale = 5
        self.image = pygame.transform.scale(obstacleImage, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.randomStart = random.randint(0,50)
        self.rect.center = (SCREEN_WIDTH/2+self.randomStart-25, 240)
        self.angle = abs((self.randomStart-25)/20)
        self.stepCounter = 10
        self.moveX = 0
        self.moveY = 0
        self.leftright = 1
        if (self.randomStart < 25):
            self.leftright = -1
        self.rect.top = 240

    def move(self):
        global SCORE
        self.stepCounter = self.stepCounter*1.02

        self.moveX += self.stepCounter*self.angle*SPEED
        self.moveY += self.stepCounter*SPEED
        self.scale = 5+0.05*self.stepCounter*SPEED
        

        pixelsX = self.leftright*(self.moveX // 500)
        if (self.moveX > 500):
            self.moveX -= self.leftright*pixelsX*500
            # self.rect = self.image.get_rect()

        pixelsY = self.moveY // 500
        if (self.moveY > 500):
            self.moveY -= pixelsY*500
            self.image = pygame.transform.scale(obstacleImage, (self.scale, self.scale))

        # if (self.leftright):
        self.rect.move_ip(pixelsX,pixelsY)
        # else:
        #     self.rect.move_ip(-pixelsX,pixelsY)
        if (self.rect.bottom > (SCREEN_HEIGHT+100)):
            SCORE += 1
            self.reset()
            

class RoadDecor(pygame.sprite.Sprite):
    def __init__(self, variation):
        super().__init__()
        self.variation = variation
        
        self.reset()
        
    def reset(self):
        self.scale = 5
        self.image = pygame.transform.scale(bushImage, (self.scale*2.5, self.scale))
        self.rect = self.image.get_rect()
        self.randomStart = random.randint(0,50)
        
        self.angle = 4+abs((self.randomStart-25)/10)
        self.stepCounter = 10
        self.moveX = 0
        self.moveY = 0
        self.leftright = 1
        if (self.randomStart < 25):
            self.leftright = -1
            self.angle += 2.5
        # self.rect.top = 240
        self.rect.center = (SCREEN_WIDTH/2+self.randomStart-25+60*self.leftright, 240+self.variation)

    def move(self):
        global SCORE
        self.stepCounter = self.stepCounter*1.02

        self.moveX += self.stepCounter*self.angle*SPEED
        self.moveY += self.stepCounter*SPEED
        self.scale = 2+0.4*self.stepCounter
        

        pixelsX = self.leftright*(self.moveX // 1000)
        if (self.moveX > 1000):
            self.moveX -= self.leftright*pixelsX*1000
            # self.rect = self.image.get_rect()

        pixelsY = self.moveY // 1000
        if (self.moveY > 1000):
            self.moveY -= pixelsY*1000
            self.image = pygame.transform.scale(bushImage, (self.scale*2.5, self.scale))

        # if (self.leftright):
        self.rect.move_ip(pixelsX,pixelsY)
        # else:
        #     self.rect.move_ip(-pixelsX,pixelsY)
        if (self.rect.bottom > (SCREEN_HEIGHT+100)):
            SCORE += 1
            self.reset()


class BGDecor(pygame.sprite.Sprite):
    def __init__(self, variation):
        super().__init__()
        self.variation = variation
        
        self.reset()
        
    def reset(self):
        self.scale = 5
        self.image = pygame.transform.scale(treeImage, (self.scale, self.scale*7))
        self.rect = self.image.get_rect()
        self.randomStart = random.randint(0,50)
        
        self.angle = 20+abs((self.randomStart-25)/10)
        self.stepCounter = 10
        self.moveX = 0
        self.moveY = 0
        self.appearRate = 100
        self.leftright = 1
        if (self.randomStart < 25):
            self.leftright = -1
        # self.rect.top = 240
        self.rect.center = (SCREEN_WIDTH/2+(self.randomStart-30)*0.2+40*self.leftright, 265-self.variation)

    def move(self):
        global SCORE
        self.stepCounter = self.stepCounter*1.02

        self.moveX += self.stepCounter*SPEED
        self.moveY += 0.1*self.stepCounter*self.angle*SPEED
        # self.scale += 0.1*self.stepCounter*SPEED
        # if (self.rect.left > 140 and self.rect.left < 260): # in center area
        #     self.moveY += self.appearRate*SPEED
        #     self.appearRate -= 1

        pixelsY = self.moveY // 1000
        if (self.moveY > 1000):
            self.moveY -= pixelsY*1000
            # self.image = pygame.transform.scale(treeImage, (self.scale, self.scale*7))

        pixelsX = self.leftright*(self.moveX // 1000)
        if (self.moveX > 1000):
            self.moveX -= self.leftright*pixelsX*1000
            self.scale += 0.1*self.leftright*pixelsX
            self.image = pygame.transform.scale(treeImage, (self.scale, self.scale*7))

            self.angle = self.angle * 0.98**(self.leftright*pixelsX)
            # self.rect = self.image.get_rect()


        # if (self.leftright):
        self.rect.move_ip(pixelsX,-pixelsY)
        # else:
        #     self.rect.move_ip(-pixelsX,pixelsY)


        if (self.rect.left > (SCREEN_WIDTH+50) or self.rect.left < -50):
            SCORE += 1
            self.reset()

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
        
        if self.rect.left > -200:
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
Decor1 = RoadDecor(5)
Decor2 = RoadDecor(10)
Decor3 = RoadDecor(0)


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
all_sprites.add(Decor1)
all_sprites.add(Decor2)
all_sprites.add(Decor3)
# all_sprites.add(BG)


bg_sprites = pygame.sprite.Group()

bg_sprites.add(BG)
bg_sprites.add(BG2)


bg_decor_sprites = pygame.sprite.Group()
Tree1 = BGDecor(random.randint(0,10))
bg_decor_sprites.add(Tree1)

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

    for entity in bg_decor_sprites:
        entity.move()
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
        

    if (eventCounter < 10):
        if (counter > 20):
            print(FramePerSec.get_fps())
            counter = 0
            if (eventCounter < 10):
                eventCounter += 1
                newBush = RoadDecor(random.randint(0,10))
                all_sprites.add(newBush)
                newTree = BGDecor(random.randint(0,10))
                bg_decor_sprites.add(newTree)
        else:
            counter += 1
        
    pygame.display.update()
    FramePerSec.tick(FPS)
