import pygame, sys, random
from pygame.locals import *

pygame.init()
pygame.font.init()
main_clock = pygame.time.Clock()

n = 0
a = 600  # bok okna
b = 30  # bok małego kwadratu
iloscbialka = 30
generate = False

# konfiguracja okna
window = pygame.display.set_mode((a, a), 0, 32)
pygame.display.set_caption('Pingwinki')

# konfiguracja staych
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
font = pygame.font.SysFont("Comic Sans MS", 35)

obazekmal = pygame.image.load('/Users/michalkopczewski/Desktop/Python/Gra pingwiny/cartoon-penguin-pixel-design_61878-525.jpg')
obrazekmaly = pygame.transform.scale(obazekmal, (b,b))

obrazegracza = pygame.image.load('/Users/michalkopczewski/Desktop/Python/Gra pingwiny/00119009_AV1_1531_4800-3200-rgb-3072x2048.jpg')
obrazekgracza = pygame.transform.scale(obrazegracza, (75, 75))

generating_pinguin = pygame.mixer.Sound('/Users/michalkopczewski/Desktop/Python/Gra pingwiny/95991981.mp3')
znikanie = pygame.mixer.Sound('/Users/michalkopczewski/Desktop/Python/Gra pingwiny/208894348.mp3')

colors = [BLACK, WHITE, RED, GREEN, BLUE]
bialkocolor = [RED, GREEN, BLUE]

szybkoscgracza = 3
szybkoscbialka = 1

moveleft = False
moveright = False
moveup = False
movedown = False

bialko = []

LG = 'lr'
LD = 'LD'
PG = 'PG'
PD = 'PD'
kierunki = [LG, LD, PG, PD]

player = pygame.Rect(200, 400, 75, 75)

def bialkomovement():
    for r in bialko:
        if r['kier'] == LD:
            r['rect'].left -= szybkoscbialka
            r['rect'].top += szybkoscbialka
        if r['kier'] == PD:
            r['rect'].left += szybkoscbialka
            r['rect'].top += szybkoscbialka
        if r['kier'] == LG:
            r['rect'].left -= szybkoscbialka
            r['rect'].top -= szybkoscbialka
        if r['kier'] == PG:
            r['rect'].left += szybkoscbialka
            r['rect'].top -= szybkoscbialka
        # Sprawdzenie odbicia
        if r['rect'].top < 0:
            if r['kier'] == LG:
                r['kier'] = LD
            if r['kier'] == PG:
                r['kier'] = PD
        if r['rect'].bottom > a:
            if r['kier'] == LD:
                r['kier'] = LG
            if r['kier'] == PD:
                r['kier'] = PG
        if r['rect'].left < 0:
            if r['kier'] == LG:
                r['kier'] = PG
            if r['kier'] == LD:
                r['kier'] = PD
        if r['rect'].right > a:
            if r['kier'] == PG:
                r['kier'] = LG
            if r['kier'] == PD:
                r['kier'] = LD

        window.blit(obrazekmaly, r['rect'])
        # pygame.draw.rect(window, r['kolor'], r['rect'])
    return bialko


def generatebialko(number):
    global r, bialko
    for i in range(number):
        r = {'rect': pygame.Rect(random.randint(0, a - b), random.randint(0, a - b), b, b),
             'kolor': random.choice(bialkocolor), 'kier': random.choice(kierunki)}
        bialko.append(r)
    return bialko


window.fill(WHITE)
generatebialko(iloscbialka)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                moveright = False
                moveleft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveleft = False
                moveright = True
            if event.key == K_DOWN or event.key == K_s:
                moveup = False
                movedown = True
            if event.key == K_UP or event.key == K_w:
                movedown = False
                moveup = True

        if event.type == pygame.KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveleft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveright = False
            if event.key == K_DOWN or event.key == K_s:
                movedown = False
            if event.key == K_UP or event.key == K_w:
                moveup = False

    window.fill(WHITE)
    # pygame.draw.rect(window, BLACK, player)
    window.blit(obrazekgracza, player)



    n +=1
    iloscbialka = len(bialko)
    if iloscbialka <= 0:
        generate = True
    if iloscbialka <= 30 and generate == True and (n % 10) == 0:
        generatebialko(1)
        generating_pinguin.play()
    if iloscbialka > 30:
        generate = False
        n = 0


    bialkomovement()
    if moveleft == True and player.left > 0:
        player.left -= szybkoscgracza
    if moveright == True and player.left < (a - 75):
        player.left += szybkoscgracza
    if moveup == True and player.top > 0:
        player.top -= szybkoscgracza
    if movedown == True and player.top < (a - 75):
        player.top += szybkoscgracza

    # pygame.draw.rect(window, BLACK, player)              Potem odchasztagowac

    for r in bialko[:]:
        if player.colliderect(r['rect']):
            bialko.remove(r)
            znikanie.play()

    # Pokazywanie ilości kwadratów
    text = font.render('Obecna ilość pingwinów:   ' + str(len(bialko)), True, RED)
    basictext = text.get_rect()
    window.blit(text, [10, 545])


    pygame.display.update()
    main_clock.tick(60)


