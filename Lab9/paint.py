import pygame
import sys
import math

pygame.init()

screen_width, screen_height = 900, 700
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
current_color = GREEN  


font_size = 24
font = pygame.freetype.SysFont("Arial", font_size)

tool = None
drawing = False

def draw_text(text, position, color):
    font.render_to(screen, position, text, color)

screen.fill(WHITE)
pygame.display.flip()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.VIDEORESIZE:
            # window resizing
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            screen.fill(WHITE)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                tool = 'rectangle'
            elif event.key == pygame.K_c:
                tool = 'circle'
            elif event.key == pygame.K_e:
                tool = 'eraser'
            elif event.key == pygame.K_s:
                current_color = RED if current_color == GREEN else GREEN
            elif event.key == pygame.K_q:
                tool = 'square'
            elif event.key == pygame.K_t:
                tool = 'triangle'
            elif event.key == pygame.K_u:
                tool = 'equilateral'
            elif event.key == pygame.K_h:
                tool = 'rhombus'

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            drawing = True
            start_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drawing = False
            end_pos = event.pos
            if tool == 'rectangle':
                pygame.draw.rect(screen, current_color, pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])))
            elif tool == 'circle':
                radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                pygame.draw.circle(screen, current_color, start_pos, radius)
            elif tool == 'square':
                side_length = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                pygame.draw.rect(screen, current_color, pygame.Rect(start_pos[0], start_pos[1], side_length, side_length))
            elif tool == 'triangle':
                pygame.draw.polygon(screen, current_color, [start_pos, (start_pos[0], end_pos[1]), end_pos])
            elif tool == 'equilateral':
                base_length = math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
                height = (math.sqrt(3) / 2) * base_length
                apex_x = (start_pos[0] + end_pos[0]) / 2
                apex_y = start_pos[1] - height
                pygame.draw.polygon(screen, current_color, [start_pos, end_pos, (apex_x, apex_y)])
            elif tool == 'rhombus':
                dx = (end_pos[0] - start_pos[0]) / 2
                dy = (end_pos[1] - start_pos[1]) / 2
                mid_x = (start_pos[0] + end_pos[0]) / 2
                mid_y = (start_pos[1] + end_pos[1]) / 2
                vert1 = (mid_x - dy, mid_y + dx)
                vert2 = (mid_x + dy, mid_y - dx)
                pygame.draw.polygon(screen, current_color, [start_pos, vert1, end_pos, vert2])
            pygame.display.flip()

        elif event.type == pygame.MOUSEMOTION and drawing:
            if tool == 'eraser':
                pygame.draw.rect(screen, WHITE, pygame.Rect(event.pos[0], event.pos[1], 10, 10))
            pygame.display.flip()

    # Display drawing instructions in two rows
    pygame.draw.rect(screen, WHITE, (0, 0, screen_width, 50))
    draw_text("R: Rectangle, C: Circle, E: Eraser, S: Switch Color", (10, 5), BLACK)
    draw_text("Q: Square, T: Triangle, U: Equilateral, H: Rhombus", (10, 30), BLACK)
    pygame.display.flip()

