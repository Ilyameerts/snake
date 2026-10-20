import random
import pygame

naam = input("Wat is je naam? ").strip()
if naam == "":
    naam = "Speler"

# Lees het recordbestand. Als het nog niet bestaat, begint het record op 0.
try:
    with open("highscore.txt", "r", encoding="utf-8") as bestand:
        record = int(bestand.read())
except (FileNotFoundError, ValueError):
    record = 0

pygame.init()

CEL = 20
KOLOMMEN = 30
RIJEN = 30
BREEDTE = KOLOMMEN * CEL
HOOGTE = RIJEN * CEL
BALK_HOOGTE = 50

scherm = pygame.display.set_mode((BREEDTE, HOOGTE + BALK_HOOGTE))
pygame.display.set_caption("Snake")
klok = pygame.time.Clock()

ZWART = (25, 25, 25)
WIT = (240, 240, 240)
GROEN = (50, 200, 80)
ROOD = (230, 60, 60)

slang = [(15, 15), (14, 15), (13, 15)]
richting = (1, 0)
score = 0
spel_bezig = True
game_over = False
beweging_toegestaan = True
tijd = 0
SNELHEID = 120  # Milliseconden tussen bewegingen

toetsen = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


def maak_eten():
    """Kies een leeg vakje voor het eten."""
    lege_vakjes = []

    for y in range(RIJEN):
        for x in range(KOLOMMEN):
            if (x, y) not in slang:
                lege_vakjes.append((x, y))

    if len(lege_vakjes) == 0:
        return None

    return random.choice(lege_vakjes)


def teken_tekst(tekst, grootte, x, y, kleur):
    """Zet tekst op het scherm."""
    lettertype = pygame.font.SysFont(None, grootte)
    afbeelding = lettertype.render(tekst, True, kleur)
    scherm.blit(afbeelding, (x, y))


eten = maak_eten()

while spel_bezig:
    tijd += klok.tick(60)

    for gebeurtenis in pygame.event.get():
        if gebeurtenis.type == pygame.QUIT:
            spel_bezig = False

        elif gebeurtenis.type == pygame.KEYDOWN:
            if gebeurtenis.key == pygame.K_ESCAPE:
                spel_bezig = False

            elif not game_over and beweging_toegestaan:
                if gebeurtenis.key in toetsen:
                    nieuwe_richting = toetsen[gebeurtenis.key]

                    # Voorkom dat de slang direct omkeert.
                    omgekeerde_richting = (-richting[0], -richting[1])
                    if nieuwe_richting != omgekeerde_richting:
                        richting = nieuwe_richting
                        beweging_toegestaan = False

    if not game_over and tijd >= SNELHEID:
        tijd = 0
        beweging_toegestaan = True

        kop_x = slang[0][0] + richting[0]
        kop_y = slang[0][1] + richting[1]
        nieuwe_kop = (kop_x, kop_y)
        eet_eten = nieuwe_kop == eten

        # De staart beweegt weg als de slang niet eet.
        lichaam = slang if eet_eten else slang[:-1]

        botst_tegen_muur = (
            kop_x < 0 or kop_x >= KOLOMMEN
            or kop_y < 0 or kop_y >= RIJEN
        )
        botst_tegen_zichzelf = nieuwe_kop in lichaam

        if botst_tegen_muur or botst_tegen_zichzelf:
            game_over = True
        else:
            slang.insert(0, nieuwe_kop)

            if eet_eten:
                score += 1

                if score > record:
                    record = score
                    with open("highscore.txt", "w", encoding="utf-8") as bestand:
                        bestand.write(str(record))

                eten = maak_eten()
                if eten is None:
                    game_over = True
            else:
                slang.pop()

    scherm.fill(ZWART)

    if eten is not None:
        pygame.draw.rect(
            scherm,
            ROOD,
            (eten[0] * CEL, eten[1] * CEL, CEL, CEL),
        )

    for vakje in slang:
        pygame.draw.rect(
            scherm,
            GROEN,
            (vakje[0] * CEL, vakje[1] * CEL, CEL, CEL),
        )

    pygame.draw.rect(scherm, (45, 45, 45), (0, HOOGTE, BREEDTE, BALK_HOOGTE))
    teken_tekst(f"{naam} | Score: {score} | Record: {record}", 30, 10, HOOGTE + 12, WIT)

    if game_over:
        teken_tekst("Game over! Druk op ESC om te sluiten.", 38, 90, HOOGTE // 2, WIT)

    pygame.display.flip()

pygame.quit()