import html
import random
import pygame

# Vraag de speler om een naam (str)
naam = input("Wat is je naam? ").strip()
if naam == "":
    naam = "Speler"

# Lees het record uit een bestand (int)
try:
    with open("highscore.txt", "r", encoding="utf-8") as bestand:
        record = int(bestand.read())
except (FileNotFoundError, ValueError):
    record = 0

# ---------- Instellingen ----------
pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 20
GRID_W = WIDTH // CELL
GRID_H = HEIGHT // CELL
MOVE_DELAY = 120  # Milliseconden tussen bewegingen

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# De slang is een lijst met posities.
snake = [
    (GRID_W // 2, GRID_H // 2),
    (GRID_W // 2 - 1, GRID_H // 2),
    (GRID_W // 2 - 2, GRID_H // 2),
]

direction = (1, 0)
new_direction = direction
score = 0  # int
timer = 0
running = True
game_over = False

# Dictionary: elke toets hoort bij een bewegingsrichting.
controls = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


def random_food():
    """Kies een leeg vakje voor het eten."""
    empty_spots = []

    # for-lussen zoeken alle lege vakjes.
    for y in range(GRID_H):
        for x in range(GRID_W):
            if (x, y) not in snake:
                empty_spots.append((x, y))

    if len(empty_spots) == 0:
        return None

    return random.choice(empty_spots)


def draw_cell(x, y, color):
    """Teken één vakje."""
    pygame.draw.rect(
        screen,
        color,
        (x * CELL, y * CELL, CELL, CELL),
    )


def draw_snake():
    """Teken de slang."""
    for index, body_part in enumerate(snake):
        if index == 0:
            color = GREEN
        else:
            color = DARK_GREEN

        draw_cell(body_part[0], body_part[1], color)


def draw_food(food):
    """Teken het eten."""
    if food is not None:
        draw_cell(food[0], food[1], RED)


def draw_score():
    """Toon de score met een f-string."""
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"{naam} | Score: {score} | Record: {record}", True, WHITE)
    screen.blit(text, (10, 10))


def save_html_result():
    """Schrijf de uitslag naar een HTML-bestand met CSS-opmaak."""
    safe_name = html.escape(naam)

    page = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <title>Snake-resultaat</title>
    <style>
        body {{
            background: #151515;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 80px;
        }}
        .kaart {{
            background: #252525;
            border: 2px solid #32c850;
            border-radius: 16px;
            display: inline-block;
            padding: 30px 50px;
        }}
        h1 {{ color: #32c850; }}
        .score {{ font-size: 24px; }}
    </style>
</head>
<body>
    <div class="kaart">
        <h1>Snake-resultaat</h1>
        <p class="score">Speler: {safe_name}</p>
        <p class="score">Eindscore: {score}</p>
        <p class="score">Record: {record}</p>
    </div>
</body>
</html>
"""

    with open("snake_resultaat.html", "w", encoding="utf-8") as bestand:
        bestand.write(page)


food = random_food()

# ---------- Game loop ----------
while running:
    elapsed_time = clock.tick(60)
    timer += elapsed_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key in controls:
                proposed_direction = controls[event.key]
                opposite_direction = (-direction[0], -direction[1])

                # Voorkom dat de slang meteen de andere kant opgaat.
                if proposed_direction != opposite_direction:
                    new_direction = proposed_direction

    # Beweeg de slang op vaste momenten.
    if timer >= MOVE_DELAY and not game_over:
        timer -= MOVE_DELAY
        direction = new_direction

        head_x = snake[0][0] + direction[0]
        head_y = snake[0][1] + direction[1]
        new_head = (head_x, head_y)
        eating = new_head == food

        # De staart beweegt weg als de slang niet eet.
        body_to_check = snake if eating else snake[:-1]

        hit_wall = (
            head_x < 0 or head_x >= GRID_W
            or head_y < 0 or head_y >= GRID_H
        )
        hit_snake = new_head in body_to_check

        if hit_wall or hit_snake:
            game_over = True
            running = False
        else:
            snake.insert(0, new_head)

            if eating:
                score += 1

                if score > record:
                    record = score
                    with open("highscore.txt", "w", encoding="utf-8") as bestand:
                        bestand.write(str(record))

                food = random_food()

                if food is None:
                    game_over = True
                    running = False
            else:
                snake.pop()

    screen.fill(BLACK)
    draw_food(food)
    draw_snake()
    draw_score()
    pygame.display.flip()

# ---------- Einde van het spel ----------
if game_over:
    screen.fill(BLACK)

    font = pygame.font.SysFont(None, 60)
    title = font.render("Game Over", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 250))

    score_font = pygame.font.SysFont(None, 36)
    result = score_font.render(f"Eindscore: {score}", True, WHITE)
    screen.blit(result, (WIDTH // 2 - result.get_width() // 2, 320))

    pygame.display.flip()
    pygame.time.wait(2000)

    save_html_result()
    print("Je resultaat is opgeslagen in snake_resultaat.html.")

pygame.quit()