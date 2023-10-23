import pygame
from copy import deepcopy
from random import choice, randrange


L, H = 12, 13
TILE = 45

GAME_RES = L * TILE, H * TILE
RES = 825,650
FPS = 60

pygame.init()
table = pygame.display.set_mode(RES)
ecran = pygame.Surface(GAME_RES)
pygame.display.set_caption("SENTAKS GAME")
clock = pygame.time.Clock()




grid = [pygame.Rect(x * TILE,y * TILE, TILE, TILE) for x in range(L) for y in range (H)]


# construction des figures

figures_pos = [[(-1,0),(-2,0),(0,0),(1,0)],
               [(0,-1),(-1,-1),(-1,0),(0,0)],
               [(-1,0),(-1,1),(0,0),(0,-1)],
               [(0,0),(-1,0),(0,1),(-1,-1)],
               [(0,0),(0,-1),(0,1),(-1,-1)],
               [(0,0),(0,-1),(0,1),(1,-1)],
               [(0,0),(0,-1),(0,1),(-1,0)]]

figures =[[pygame.Rect(x + L // 2, y + 1, 1, 1) for x,y in fig_pos]for fig_pos in figures_pos]
figure_rect = pygame.Rect(0,0, TILE - 2, TILE - 2)
# champs = [[0 for i in range(L) for j in range (H)]] 
champs = [[0 for i in range(L)] for j in range(H)]



konte,vites,limit = 0,60,2000

temps_ecoule = 0
intervalle_descente = 0.33  # 1/3 de seconde



background = pygame.image.load('1.webp').convert()
cover = pygame.image.load('bg2.jpg').convert()

# style ekriti
main_font = pygame.font.Font('tetris.ttf', 30)
font = pygame.font.Font('tetris.ttf', 45)

# ekriti
titre = main_font.render('SENTAKS Game', True, pygame.Color('purple'))
score_text = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('orange'))

record_text = font.render('record:', True, pygame.Color('blue'))

# fonction pou koule
get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))


figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

score, lignes = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}




# fonction pou bay bordure



def bordures():
    if figure[i].x < 0 or figure[i].x > L - 1:
        return False
    elif figure[i].y > H - 1 or champs[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))




while True:
    ctrl = 0
    vire = False
    record = get_record()
    table.blit(background, (0, 0))
    table.blit(ecran, (20, 20))
    ecran.blit(cover, (0, 0))
    # delai pou pleun lignes yo
    for i in range(lignes):
        pygame.time.wait(200)

    # mouvman
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ctrl = -1
            elif event.key == pygame.K_RIGHT:
                ctrl = 1
            elif event.key == pygame.K_DOWN:
                limit = 100
            elif event.key == pygame.K_UP:
                vire = True

       # Bouje x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += ctrl
        if not bordures():
            figure = deepcopy(figure_old)
            break

   

    
    # tan pase
    temps_ecoule += clock.get_rawtime() / 1000  

    # si temps écoulé plis pase intervalle_descente voyel anba
    if temps_ecoule >= intervalle_descente:
        temps_ecoule = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not bordures():
                for i in range(4):
                    champs[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                limit = 2000
                break        
            
    # bouje y
    konte += vites
    if konte > limit:
        konte = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not bordures():
                for i in range(4):
                    champs[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                limit = 2000
                break
    
     # efase line ki full yo
    ligne, lignes = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(L):
            if champs[row][i]:
                count += 1
            champs[ligne][i] = champs[row][i]
        if count < L:
            ligne -= 1
        else:
            vites += 3
            lignes += 1
            
     # compute score
    score += scores[lignes]
     
            
    # vire
    center = figure[0]
    figure_old = deepcopy(figure)
    if vire:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y - y
            
            if not bordures():
                figure = deepcopy(figure_old)
                break
            
    # cadriye ecran 
    [pygame.draw.rect(ecran, (40,40,40), i_rect, 1) for i_rect in grid]
    
    #figi
    for i in range (4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(ecran, color, figure_rect)
    
    
    #champs
    
    for y, raw in enumerate(champs):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(ecran, col, figure_rect)
                
    #   nouvo form
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(table, next_color, figure_rect)
                
                
    # title
    
    table.blit(titre, (567, 35))
    table.blit(score_text, (567, 450))
    table.blit(font.render(str(score), True, pygame.Color('white')), (570, 500))
    table.blit(title_record, (567, 540))
    table.blit(font.render(record, True, pygame.Color('gold')), (570, 580))

  
    
    # game over
    for i in range(L):
        if champs[0][i]:
            set_record(record, score)
            champs = [[0 for i in range(L)] for i in range(H)]
            konte, vites, limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(ecran, get_color(), i_rect)
                table.blit(ecran, (20, 20))
                pygame.display.flip()
                clock.tick(200)
    
    
     
    pygame.display.flip()
    clock.tick(FPS)