import pygame,sys,maze,random
from pygame.locals import *

class Pyman(object):

    pygame.init()

    FPS = 30
    fpsClock = pygame.time.Clock()

    JANELA = pygame.display.set_mode((888,650),0,32)
    TELA = pygame.display.get_surface()
    pygame.display.set_caption('PyMan - The Python Pacman')

    mapa = maze.create(24,36,random.uniform(0.5999,0.7999),random.uniform(0.5999,0.7999))

    bloco_fechado = pygame.image.load('bloco_fechado.png')
    bloco_canto = pygame.image.load('bloco_canto.png')
    bloco_1abertura = pygame.image.load('bloco_1abertura.png')
    bloco_3abertura = pygame.image.load('bloco_3abertura.png')
    bloco_centro = pygame.image.load('bloco_centro.png')
    bala = pygame.image.load('bala.png')
    bala_especial = pygame.image.load('bala_especial.png')
    pyman = pygame.image.load('pyman.png').convert()
    pyman_surf = pyman
    pymanx = 24
    pymany = 24
    direcao = 'stop'
    points = 0

    blocos_lugares = []

    SPEED = 10

    ballas = []

    mapa_balas = []
    def __init__(self):
        self.convert_balas()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def get_near(self,linha,coluna):
        near_linha = []
        near_coluna = []
        if linha == 0:
            near_linha.append(False)
            near_linha.append(self.mapa[linha+1][coluna])
        if coluna == 0:
            near_coluna.append(False)
            near_coluna.append(self.mapa[linha][coluna+1])
        if linha == 36:
            near_linha.append(self.mapa[linha-1][coluna])
            near_linha.append(False)
        if coluna == 24:
            near_coluna.append(self.mapa[linha][coluna-1])
            near_coluna.append(False)
        if 0 < linha < 36:
            near_linha.append(self.mapa[linha-1][coluna])
            near_linha.append(self.mapa[linha+1][coluna])
        if 0 < coluna < 24:
            near_coluna.append(self.mapa[linha][coluna-1])
            near_coluna.append(self.mapa[linha][coluna+1])
        return near_linha,near_coluna

    def draw_bloco(self,linha,coluna):
        near_linha,near_coluna = self.get_near(linha,coluna)
        self.blocos_lugares.append((linha*24,coluna*24))
        # canto
        if not near_linha[0] and near_linha[1] and not near_coluna[0] and near_coluna[1]: return self.bloco_canto
        if not near_linha[0] and near_linha[1] and near_coluna[0] and not near_coluna[1]: return pygame.transform.rotate(self.bloco_canto,90)
        if near_linha[0] and not near_linha[1] and not near_coluna[0] and near_coluna[1]: return pygame.transform.rotate(self.bloco_canto,270)
        if near_linha[0] and not near_linha[1] and near_coluna[0] and not near_coluna[1]: return pygame.transform.rotate(self.bloco_canto,180)
        # centro
        if not near_linha[0] and not near_linha[1] and near_coluna[0] and near_coluna[1]: return pygame.transform.rotate(self.bloco_centro,90)
        if near_linha[0] and near_linha[1] and not near_coluna[0] and not near_coluna[1]: return self.bloco_centro
        # 3 lados
        if near_linha[0] and near_linha[1] and near_coluna[0] and not near_coluna[1]: return pygame.transform.rotate(self.bloco_3abertura,180)
        if near_linha[0] and near_linha[1] and not near_coluna[0] and near_coluna[1]: return pygame.transform.rotate(self.bloco_3abertura,0)
        if near_linha[0] and not near_linha[1] and near_coluna[0] and near_coluna[1]: return pygame.transform.rotate(self.bloco_3abertura,270)
        if not near_linha[0] and near_linha[1] and near_coluna[0] and near_coluna[1]: return pygame.transform.rotate(self.bloco_3abertura,90)
        # 1 lado
        if near_linha[0] and not near_linha[1] and not near_coluna[0] and not near_coluna[1]: return pygame.transform.rotate(self.bloco_1abertura,270)
        if not near_linha[0] and near_linha[1] and not near_coluna[0] and not near_coluna[1]: return pygame.transform.rotate(self.bloco_1abertura,90)
        if not near_linha[0] and not near_linha[1] and near_coluna[0] and not near_coluna[1]: return pygame.transform.rotate(self.bloco_1abertura,180)
        if not near_linha[0] and not near_linha[1] and not near_coluna[0] and near_coluna[1]: return pygame.transform.rotate(self.bloco_1abertura,0)

        return self.bloco_fechado

    def draw_map(self):
        for linha in range(len(self.mapa)):
            for ponto in range(len(self.mapa[linha])):
                if self.mapa[linha][ponto]:
                    self.TELA.blit(self.draw_bloco(linha,ponto),(linha*24,ponto*24))
                else:
                    if (self.mapa_balas[linha][ponto]):
                        self.ballas.append((linha*24,ponto*24))
                        self.TELA.blit(self.bala,(linha*24,ponto*24))

    def convert_balas(self):
        for linha in range(len(self.mapa)):
            self.mapa_balas.append(list(self.mapa[linha]))

        for linha in range(len(self.mapa_balas)):
            for ponto in range(len(self.mapa_balas[linha])):
                self.mapa_balas[linha][ponto] = not self.mapa_balas[linha][ponto]

    def pyman_collision_wall(self):
        walls = [self.bloco_fechado,self.bloco_canto,self.bloco_centro,self.bloco_1abertura,self.bloco_3abertura]
        for wall in self.blocos_lugares:
            wall_rec = pygame.Rect(wall[0],wall[1],24,24)
            pyman_rec = pygame.Rect(self.pymanx,self.pymany,24,24)
            if pyman_rec.colliderect(wall_rec):
                return True
        return False

    def pyman_collision_ball(self):
        if self.mapa_balas[self.pymanx//24][self.pymany//24]:
            self.mapa_balas[self.pymanx//24][self.pymany//24] = False
            self.points += 10

    def main(self):
        while True:
            self.pyman_collision_ball()
            self.TELA.fill((0,0,0))
            self.draw_map()
            for event in pygame.event.get():
                if event.type == QUIT: self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT: self.direcao = 'left'
                    if event.key == K_RIGHT: self.direcao = 'right'
                    if event.key == K_UP: self.direcao = 'up'
                    if event.key == K_DOWN: self.direcao = 'down'
                    if event.key == K_ESCAPE: self.terminate()
            if self.direcao == 'left':
                self.pyman_surf = self.pyman
                self.pymanx -= 24
                if self.pyman_collision_wall(): self.pymanx += 24
            if self.direcao == 'right':
                self.pymanx += 24
                self.pyman_surf = pygame.transform.rotate(self.pyman,180)
                if self.pyman_collision_wall(): self.pymanx -= 24
            if self.direcao == 'up':
                self.pymany -= 24
                self.pyman_surf = pygame.transform.rotate(self.pyman,270)
                if self.pyman_collision_wall(): self.pymany += 24
            if self.direcao == 'down':
                self.pymany += 24
                self.pyman_surf = pygame.transform.rotate(self.pyman,90)
                if self.pyman_collision_wall(): self.pymany -= 24
            self.direcao = 'stop'
            fontObj = pygame.font.Font('freesansbold.ttf', 32)
            textSurfaceObj = fontObj.render('Pontos: '+str(self.points), True, (0,255,0), (0,0,0))
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (100, 624)
            self.TELA.blit(textSurfaceObj,textRectObj)

            self.TELA.blit(self.pyman_surf,(self.pymanx,self.pymany))
            # direcao = 'stop'
            self.JANELA.blit(self.TELA,(0,0))
            pygame.display.update()
            self.fpsClock.tick(self.FPS)
p = Pyman()
p.main()