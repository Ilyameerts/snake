import pygame
import random
import sys

# ---------- Setup ----------
pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20
GRID_W = WIDTH // CELL
GRID_H = HEIGHT // CELL

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 128, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# ---------- Snake ----------
snake = [(GRID_W // 2, GRID_H // 2),
         (GRID_W // 2 - 1, GRID_H // 2),
         (GRID_W // 2 - 2, GRID_H // 2)]
direction = (1, 0)
new_direction = direction
score = 0

# ---------- Food ----------
def random_food():
    while True:
        food = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
        if food not in snake:
            return food

food = random_food()

# ---------- Functions ----------
def draw_cell(x, y, color):
    pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))

def draw_snake():
    for i, body in enumerate(snake):
        color = GREEN if i == 0 else (0, 200, 0)
        draw_cell(body[0], body[1], color)

def draw_food():
    draw_cell(food[0], food[1], RED)

def draw_score():
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

# ---------- Game loop ----------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                new_direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                new_direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                new_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                new_direction = (1, 0)

    direction = new_direction

    head_x = snake[0][0] + direction[0]
    head_y = snake[0][1] + direction[1]

    new_head = (head_x, head_y)

    # Walls / self collision
    if (head_x < 0 or head_x >= GRID_W or head_y < 0 or head_y >= GRID_H or
            new_head in snake):
        running = False

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        food = random_food()
    else:
        snake.pop()

    screen.fill(BLACK)
    draw_food()
    draw_snake()
    draw_score()
    pygame.display.flip()

    clock.tick(10)

# ---------- Game over ----------
font = pygame.font.SysFont(None, 60)
text = font.render("Game Over", True, WHITE)
screen.blit(text, (170, 260))
font2 = pygame.font.SysFont(None, 30)
text2 = font2.render(f"Final Score: {score}", True, WHITE)
screen.blit(text2, (210, 310))
pygame.display.flip()

pygame.time.wait(2000)
pygame.quit()
sys.exit()