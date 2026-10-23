import html
import random
import pygame

# Lees het record uit een bestand
try:
    with open("highscore.txt", "r", encoding="utf-8") as bestand:
        record = int(bestand.read())
except (FileNotFoundError, ValueError):
    record = 0

pygame.init()

# Instellingen
WIDTH = 1255
HEIGHT = 600
CELL = 20
GRID_W = WIDTH // CELL
GRID_H = HEIGHT // CELL
MOVE_DELAY = 120

BLACK = (20, 20, 20) 
WHITE = (255, 255, 255)
PINK = (255, 105, 180)
DARK_PINK = (230, 70, 150)
APPLE_GREEN = (50, 205, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

start_foto = pygame.image.load("startscherm.png").convert()
start_foto = pygame.transform.scale(start_foto, (WIDTH, HEIGHT))
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("worm over")
clock = pygame.time.Clock()

gameover_foto = pygame.image.load("wormover.png").convert()
gameover_foto = pygame.transform.scale(gameover_foto, (WIDTH, HEIGHT))




# Spelgegevens
naam = ""
score = 0
worm = []
direction = (1, 0)
new_direction = direction
food = None
timer = 0
game_state = "start"  # Mogelijke waarden: start, playing, game_over
running = True

# Dictionary met de besturing
controls = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


def random_food(worm_parts):
    """Kies een leeg vakje voor de appel."""
    empty_spots = []

    for y in range(GRID_H):
        for x in range(GRID_W):
            if (x, y) not in worm_parts:
                empty_spots.append((x, y))

    if not empty_spots:
        return None

    return random.choice(empty_spots)


def draw_text(text, size, x, y, color=BLACK):
    """Toon tekst in het midden van het scherm."""
    font = pygame.font.SysFont(None, size)
    image = font.render(text, True, color)
    screen.blit(image, (x - image.get_width() // 2, y))


def start_game():
    """Begin een nieuw spel."""
    global score, worm, direction, new_direction, food, timer, game_state

    score = 0
    worm = [
        (GRID_W // 2, GRID_H // 2),
        (GRID_W // 2 - 1, GRID_H // 2),
        (GRID_W // 2 - 2, GRID_H // 2),
    ]
    direction = (1, 0)
    new_direction = direction
    food = random_food(worm)
    timer = 0
    game_state = "playing"


def save_html_result():
    """Sla de uitslag op als een HTML-pagina met CSS."""
    safe_name = html.escape(naam)

    page = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <title>Worm-resultaat</title>
    <style>
        body {{
            background: #141414;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 80px;
        }}
        .kaart {{
            display: inline-block;
            padding: 30px 50px;
            background: #252525;
            border: 3px solid #ff69b4;
            border-radius: 16px;
        }}
        h1 {{ color: #ff69b4; }}
        p {{ font-size: 24px; }}
    </style>
</head>
<body>
    <div class="kaart">
        <h1>Worm-resultaat</h1>
        <p>Speler: {safe_name}</p>
        <p>Score: {score}</p>
        <p>Record: {record}</p>
    </div>
</body>
</html>
"""

    with open("worm_resultaat.html", "w", encoding="utf-8") as bestand:
        bestand.write(page)


while running:
    elapsed_time = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif game_state == "start":
                if event.key == pygame.K_RETURN and naam.strip():
                    naam = naam.strip()
                    start_game()
                elif event.key == pygame.K_BACKSPACE:
                    naam = naam[:-1]
                elif event.unicode.isprintable() and len(naam) < 20:
                    naam += event.unicode

            elif game_state == "playing" and event.key in controls:
                proposed_direction = controls[event.key]
                opposite_direction = (-direction[0], -direction[1])

                if proposed_direction != opposite_direction:
                    new_direction = proposed_direction

            elif game_state == "game_over" and event.key == pygame.K_r:
                start_game()

    if game_state == "playing":
        timer += elapsed_time

        if timer >= MOVE_DELAY:
            timer -= MOVE_DELAY
            direction = new_direction

            head_x = worm[0][0] + direction[0]
            head_y = worm[0][1] + direction[1]
            new_head = (head_x, head_y)
            eating = new_head == food

            # De staart beweegt weg als de slang niet eet.
            body_to_check = worm if eating else worm[:-1]

            hit_wall = (
                head_x < 0 or head_x >= GRID_W
                or head_y < 0 or head_y >= GRID_H
            )
            hit_worm = new_head in body_to_check

            if hit_wall or hit_worm:
                game_state = "game_over"
                save_html_result()
            else:
                worm.insert(0, new_head)

                if eating:
                    score += 1

                    if score > record:
                        record = score
                        with open("highscore.txt", "w", encoding="utf-8") as bestand:
                            bestand.write(str(record))

                    food = random_food(worm)

                    if food is None:
                        game_state = "game_over"
                        save_html_result()
                else:
                    worm.pop()

    screen.fill(WHITE)

    if game_state == "start":
        screen.blit(start_foto, (0, 0))
        draw_text("", 72, WIDTH // 2, 150, PINK)
        draw_text("Typ je naam en druk op Enter", 20, WIDTH // 2, 240)
        draw_text(naam + "|", 30, WIDTH // 2, 270, BLACK)
        draw_text("", 28, WIDTH // 2, 390)

    elif game_state == "playing":
        if food is not None:
            pygame.draw.rect(
                screen,
                APPLE_GREEN,
                (food[0] * CELL, food[1] * CELL, CELL, CELL),
            )

        for index, part in enumerate(worm):
            color = PINK if index == 0 else DARK_PINK
            pygame.draw.rect(
                screen,
                color,
                (part[0] * CELL, part[1] * CELL, CELL, CELL),
            )

        draw_text(f"{naam} | Score: {score} | Record: {record}", 30, WIDTH // 2, 20)

    elif game_state == "game_over":
        screen.blit(gameover_foto, (0, 0))
        draw_text(f"Score: {score}  |  Record: {record}", 36, WIDTH // 2, 240)
        draw_text("Druk op R om opnieuw te spelen", 25, WIDTH // 2, 420)
       

    pygame.display.flip()

pygame.quit()