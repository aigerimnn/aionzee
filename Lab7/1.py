import pygame
from datetime import datetime
pygame.init()
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
WHITE = (255, 255, 255)
FPS = 60
clock = pygame.time.Clock()
bg = pygame.image.load('mickey-clock.jpg')
BG_WIDTH = 500
BG_HEIGHT = 500
BG_X_POS = (SCREEN_WIDTH / 2 - BG_WIDTH / 2)  # Initial positions
BG_Y_POS = (SCREEN_HEIGHT / 2 - BG_HEIGHT / 2)
# Big Arrow setup
big_arrow = pygame.image.load('big-arrow.png')
BIG_ARROW_WIDTH = 35
BIG_ARROW_ASPECT_RATIO = 0.13
BIG_ARROW_HEIGHT = int(BIG_ARROW_WIDTH / BIG_ARROW_ASPECT_RATIO)
big_arrow = pygame.transform.scale(big_arrow, (BIG_ARROW_WIDTH, BIG_ARROW_HEIGHT))
big_arrow_rect = big_arrow.get_rect()
big_arrow_rect.center = CENTER
# Little Arrow setup with corrected aspect ratio based on original dimensions
little_arrow = pygame.image.load('small-arrow.png')
LITTLE_ARROW_WIDTH = 50
LITTLE_ARROW_ASPECT_RATIO = 3.275  # Corrected based on original dimensions (80x262)
LITTLE_ARROW_HEIGHT = int(LITTLE_ARROW_WIDTH * LITTLE_ARROW_ASPECT_RATIO)  # Adjusted calculation
little_arrow = pygame.transform.scale(little_arrow, (LITTLE_ARROW_WIDTH, LITTLE_ARROW_HEIGHT))
little_arrow_rect = little_arrow.get_rect()
little_arrow_rect.center = CENTER
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    now = datetime.now()
    second_angle = now.second * -6
    minute_angle = now.minute * -6
    # Rotate big arrow
    rotated_big_arrow = pygame.transform.rotate(big_arrow, second_angle)
    rotated_big_arrow_rect = rotated_big_arrow.get_rect(center=CENTER)
    # Rotate little arrow
    rotated_little_arrow = pygame.transform.rotate(little_arrow, minute_angle)
    rotated_little_arrow_rect = rotated_little_arrow.get_rect(center=CENTER)
    screen.fill(WHITE)
    screen.blit(bg, (BG_X_POS, BG_Y_POS))
    screen.blit(rotated_big_arrow, rotated_big_arrow_rect)
    screen.blit(rotated_little_arrow, rotated_little_arrow_rect)
    pygame.display.flip()
    clock.tick(FPS)