
import pygame, time
import random
from pygame.locals import *

pygame.init()

SIZE = WIDTH, HEIGHT = 400, 600
FPS = 60
SPEED = 5
SPEED_ENEMY = 5
SCORE = 0
SCORE_COINS = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 18)
game_over = font.render("Game Over", True, BLACK)
background = pygame.image.load("AnimatedStreet.png")

# Setup screen
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Racer")

done = False

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("car2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED_ENEMY)
        if self.rect.bottom > HEIGHT:
            global SCORE
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("car1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-SPEED, 0)
        if self.rect.right < WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(SPEED, 0)

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, WIDTH - 30), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)


pygame.init()

original_coin_image = pygame.image.load("coin.png")
new_size = (18, 18)
smaller_coin_image = pygame.transform.scale(original_coin_image, new_size)

# SpecialCoin class
class SpecialCoin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = smaller_coin_image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, WIDTH - 30), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)


# Initializing player, enemy,coins
P1 = Player()
E1 = Enemy()
C1 = Coin()
SC1 = SpecialCoin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
special_coins = pygame.sprite.Group()
special_coins.add(SC1)
all_sprites = pygame.sprite.Group()
all_sprites.add(E1, P1, C1, SC1)

# Speed increasing
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Main game loop
while not done:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == INC_SPEED:
            SPEED_ENEMY += 0.35

    screen.blit(background, (0, 0))
    scores = font_small.render("Score:" + str(SCORE), True, BLACK)
    scores_coins = font_small.render("Coins:" + str(SCORE_COINS), True, GREEN)
    screen.blit(scores, (10, 10))
    screen.blit(scores_coins, (315, 10))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # Collision detection
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("crash.wav").play()
        time.sleep(1)
        game_over = font.render("Game Over", True, WHITE)  
        screen.blit(game_over, (20, 250))
    
 
        scores = font_small.render("Score:" + str(SCORE), True, WHITE)  
        scores_coins = font_small.render("Coins:" + str(SCORE_COINS), True, GREEN) 
        screen.blit(scores, (165, 330))
        screen.blit(scores_coins, (165, 350))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(1)
        done = True

    # Collecting coins
    collected_coins = pygame.sprite.spritecollide(P1, coins, dokill=False) + pygame.sprite.spritecollide(P1, special_coins, dokill=False)
    for coin in collected_coins:
        if isinstance(coin, SpecialCoin):
            SCORE_COINS += 2
        else:
            SCORE_COINS += 1
        coin.rect.top = 0
        coin.rect.center = (random.randint(40, WIDTH - 40), 0)

    pygame.display.update()
    clock.tick(FPS)