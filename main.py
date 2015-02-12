import pygame,sys,numpy
from pygame.locals import *
from numpy.random import random_integers as rand

def maze(width=51, height=51, complexity=.75, density=.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density    = int(density * (shape[0] // 2 * shape[1] // 2))
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return Z

def terminate():
    pygame.quit()
    sys.exit()

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

JANELA = pygame.display.set_mode((888,650),0,32)
TELA = pygame.display.get_surface()
pygame.display.set_caption('PyMan - The Python Pacman')

mapa = maze(24,36,.5,.5)

bloco_fechado = pygame.image.load('bloco_fechado.png')
bala = pygame.image.load('bala.png')
bala_especial = pygame.image.load('bala_especial.png')
pyman = pygame.image.load('pyman.png').convert()
pyman_surf = pyman
pymanx = 24
pymany = 24
direcao = 'left'
points = 0

mapa_balas = []

for linha in range(len(mapa)):
    mapa_balas.append(list(mapa[linha]))

for linha in range(len(mapa_balas)):
    for ponto in range(len(mapa_balas[linha])):
        mapa_balas[linha][ponto] = not mapa_balas[linha][ponto]

while True:
    TELA.fill((0,0,0))
    if mapa_balas[pymanx//24][pymany//24]: 
        mapa_balas[pymanx//24][pymany//24] = False
        points += 10
    for linha in range(len(mapa)):
        for ponto in range(len(mapa[linha])):
            if mapa[linha][ponto]:
                TELA.blit(bloco_fechado,(linha*24,ponto*24))
            else:
                if (mapa_balas[linha][ponto]):
                    TELA.blit(bala,(linha*24,ponto*24))
	for event in pygame.event.get():
		if event.type == QUIT: terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT: direcao = 'left'
            if event.key == K_RIGHT: direcao = 'right'
            if event.key == K_UP: direcao = 'up'
            if event.key == K_DOWN: direcao = 'down'
            if event.key == K_ESCAPE: terminate()
    if direcao == 'left':
        if not mapa[(pymanx-24)//24][pymany//24]:
            pymanx -= 24
            pyman_surf = pyman
    if direcao == 'right':
        if not mapa[(pymanx+24)//24][pymany//24]:
            pymanx += 24
            pyman_surf = pygame.transform.rotate(pyman,180)
    if direcao == 'up':
        if not mapa[pymanx//24][(pymany-24)//24]:
            pymany -= 24
            pyman_surf = pygame.transform.rotate(pyman,270)
    if direcao == 'down':
        if not mapa[pymanx//24][(pymany+24)//24]:
            pymany += 24
            pyman_surf = pygame.transform.rotate(pyman,90)
    print 'pyman:',pymanx,pymany

    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render('Pontos: '+str(points), True, (0,255,0), (0,0,0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (100, 624)
    TELA.blit(textSurfaceObj,textRectObj)

    TELA.blit(pyman_surf,(pymanx,pymany))
    direcao = 'stop'
    JANELA.blit(TELA,(0,0))
    pygame.display.update()
    fpsClock.tick(FPS)