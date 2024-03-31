import pygame
import random
# Инициализация Pygame
pygame.init()
# Определение констант
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20
FPS = 10
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# Определение класса Snake
class Snake:
    def __init__(self):
        self.position = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = "RIGHT"
        self.change_direction_to = self.direction
    def change_direction(self, direction):
        if direction == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        if direction == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        if direction == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        if direction == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"
    def move(self):
        if self.direction == "RIGHT":
            self.position[0] += BLOCK_SIZE
        if self.direction == "LEFT":
            self.position[0] -= BLOCK_SIZE
        if self.direction == "UP":
            self.position[1] -= BLOCK_SIZE
        if self.direction == "DOWN":
            self.position[1] += BLOCK_SIZE
        self.body.insert(0, list(self.position))
    def check_collision(self):
        if self.position[0] >= SCREEN_WIDTH or self.position[0] < 0 or \
           self.position[1] >= SCREEN_HEIGHT or self.position[1] < 0:
            return True
        for body_part in self.body[1:]:
            if self.position == body_part:
                return True
        return False
    def get_head_position(self):
        return self.position
    def get_body(self):
        return self.body
# Определение класса Food
class Food:
    def __init__(self):
        self.position = [random.randrange(1, SCREEN_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randrange(1, SCREEN_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
    def spawn_food(self):
        self.position = [random.randrange(1, SCREEN_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randrange(1, SCREEN_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
    def get_food_position(self):
        return self.position
# Инициализация игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
# Инициализация змейки и еды
snake = Snake()
food = Food()
# Основной игровой цикл
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")
            if event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            if event.key == pygame.K_UP:
                snake.change_direction("UP")
            if event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")
    snake.move()
    if abs(snake.get_head_position()[0] - food.get_food_position()[0]) < BLOCK_SIZE and \
       abs(snake.get_head_position()[1] - food.get_food_position()[1]) < BLOCK_SIZE:
        food.spawn_food()
    else:
        snake.body.pop()
    if snake.check_collision():
        pygame.quit()
        quit()
    screen.fill(WHITE)
    for position in snake.get_body():
        pygame.draw.rect(screen, GREEN, pygame.Rect(position[0], position[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(food.get_food_position()[0], food.get_food_position()[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.display.update()
    clock.tick(FPS)
