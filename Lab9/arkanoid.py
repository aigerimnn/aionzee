import pygame
import random

pygame.init()

W, H = 1200, 800
FPS = 60

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()
done = False
bg = (0, 0, 0)  

# Paddle parameters
paddleW = 150
paddleH = 25
paddleSpeed = 20
paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)

# Ball parameters
ballRadius = 20
ballSpeed = 6
ball_rect = int(ballRadius * 2 ** 0.5)
ball = pygame.Rect(random.randrange(ball_rect, W - ball_rect), H // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# Game score setup
game_score = 0
game_score_fonts = pygame.font.SysFont('comicsansms', 40)
game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (255, 255, 255))
game_score_rect = game_score_text.get_rect()
game_score_rect.center = (210, 20)

collision_sound = pygame.mixer.Sound('catch.mp3')

# Collision detection
def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    else:
        dx = -dx
    return dx, dy

# Blocks
block_list = [pygame.Rect(10 + 120 * i, 50 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(0, 0, 255) for _ in range(10) for _ in range(4)] 

# Game over sighn
losefont = pygame.font.SysFont('comicsansms', 40)
losetext = losefont.render('Game Over', True, (255, 255, 255))
losetextRect = losetext.get_rect()
losetextRect.center = (W // 2, H // 2)

# Win sighn
winfont = pygame.font.SysFont('comicsansms', 40)
wintext = winfont.render('You win yay', True, (0, 0, 0))
wintextRect = wintext.get_rect()
wintextRect.center = (W // 2, H // 2)

# Pause
pausefont = pygame.font.SysFont('comicsansms', 80)
pausetext = pausefont.render('Pause', True, (255, 255, 255))
pausetextRect = pausetext.get_rect()
pausetextRect.center = (W // 2, H // 2)
paused = False

# Game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  
                paused = not paused

    if not paused:
        screen.fill(bg)
        [pygame.draw.rect(screen, color_list[color], block) for color, block in enumerate(block_list)]
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), paddle)
        pygame.draw.circle(screen, pygame.Color(255, 0, 0), ball.center, ballRadius)

        ball.x += ballSpeed * dx
        ball.y += ballSpeed * dy

        if ball.centerx < ballRadius or ball.centerx > W - ballRadius:
            dx = -dx
        if ball.centery < ballRadius + 50:
            dy = -dy
        if ball.colliderect(paddle) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, paddle)
        
        # Block collision
        hitIndex = ball.collidelist(block_list)
        if hitIndex != -1:
            hitRect = block_list.pop(hitIndex)
            color_list.pop(hitIndex)
            dx, dy = detect_collision(dx, dy, ball, hitRect)
            game_score += 1
            collision_sound.play()

        game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (255, 255, 255))
        screen.blit(game_score_text, game_score_rect)

        # Game over condition
        if ball.bottom > H:
            screen.fill(bg)
            screen.blit(losetext, losetextRect)
        # Win condition
        elif not block_list:
            screen.fill(bg)
            screen.blit(wintext, wintextRect)

        # Paddle control
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddleSpeed
        if key[pygame.K_RIGHT] and paddle.right < W:
            paddle.right += paddleSpeed
    else:
        #"Pause" text when paussing
        screen.blit(pausetext, pausetextRect)

    pygame.display.flip()  
    clock.tick(FPS)  