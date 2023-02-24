import pygame
import os, time

titulo = pygame.image.load(os.path.join('imgs', 'titulo.png'))
tabuleiro = pygame.image.load(os.path.join('imgs', 'tabuleiro.png'))
pecabranca = pygame.image.load(os.path.join('imgs', 'pecabranca.png'))
pecapreta = pygame.image.load(os.path.join('imgs/pecapreta.png'))
jogadorVencedor = 0

# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZACLARO = (220, 220, 220)

# definindo outras constantes do jogo
LARGURAJANELA = 800
ALTURAJANELA = 600
LARGURATITULO = titulo.get_width()
ALTURATITULO = titulo.get_height()
LARGURATABULEIRO = tabuleiro.get_width()
ALTURATABULEIRO = tabuleiro.get_height()
TABULEIROORIGEM = (int((LARGURAJANELA - LARGURATABULEIRO) / 2), ALTURATITULO + 25)

posJogador1 = {}
posJogador2 = {}
for i in range(2):
    for j in range(4):
        posJogador1[(i, j)] = (i * 80 + (LARGURAJANELA + LARGURATABULEIRO) / 2, j * 80 + (ALTURAJANELA - 235) / 2)
        posJogador2[(i, j)] = (i * 80 + (LARGURAJANELA - LARGURATABULEIRO - 320) / 2, j * 80 + (ALTURAJANELA - 235) / 2)

pecasJogador1 = [
    {'peca': pygame.image.load('imgs/pecabranca.png'), 'pos': posJogador1[(1, 0)], 'livre': True,
     'base': posJogador1[(1, 0)], 'player': 1},
    {'peca': pygame.image.load('imgs/pecabranca.png'), 'pos': posJogador1[(1, 1)], 'livre': True,
     'base': posJogador1[(1, 1)], 'player': 1},
    {'peca': pygame.image.load('imgs/pecabranca.png'), 'pos': posJogador1[(1, 2)], 'livre': True,
     'base': posJogador1[(1, 2)], 'player': 1},
    {'peca': pygame.image.load('imgs/pecabranca.png'), 'pos': posJogador1[(1, 3)], 'livre': True,
     'base': posJogador1[(1, 3)], 'player': 1},
    {'peca': pygame.image.load('imgs/pecabranca.png'), 'pos': posJogador1[(0, 0)], 'livre': True,
     'base': posJogador1[(0, 0)], 'player': 1},
    {'peca': pygame.image.load('imgs/pecabranca.png'), 'pos': posJogador1[(0, 1)], 'livre': True,
     'base': posJogador1[(0, 1)], 'player': 1},
    {'peca': pygame.image.load('imgs/pecabranca.png'), 'pos': posJogador1[(0, 2)], 'livre': True,
     'base': posJogador1[(0, 2)], 'player': 1},
    {'peca': pygame.image.load('imgs/pecabranca.png'), 'pos': posJogador1[(0, 3)], 'livre': True,
     'base': posJogador1[(0, 3)], 'player': 1},
]

pecasJogador2 = [
    {'peca': pygame.image.load('imgs/pecapreta.png'), 'pos': posJogador2[(0, 0)], 'livre': True,
     'base': posJogador2[(0, 0)], 'player': 2},
    {'peca': pygame.image.load('imgs/pecapreta.png'), 'pos': posJogador2[(0, 1)], 'livre': True,
     'base': posJogador2[(0, 1)], 'player': 2},
    {'peca': pygame.image.load('imgs/pecapreta.png'), 'pos': posJogador2[(0, 2)], 'livre': True,
     'base': posJogador2[(0, 2)], 'player': 2},
    {'peca': pygame.image.load('imgs/pecapreta.png'), 'pos': posJogador2[(0, 3)], 'livre': True,
     'base': posJogador2[(0, 3)], 'player': 2},
    {'peca': pygame.image.load('imgs/pecapreta.png'), 'pos': posJogador2[(1, 0)], 'livre': True,
     'base': posJogador2[(1, 0)], 'player': 2},
    {'peca': pygame.image.load('imgs/pecapreta.png'), 'pos': posJogador2[(1, 1)], 'livre': True,
     'base': posJogador2[(1, 1)], 'player': 2},
    {'peca': pygame.image.load('imgs/pecapreta.png'), 'pos': posJogador2[(1, 2)], 'livre': True,
     'base': posJogador2[(1, 2)], 'player': 2},
    {'peca': pygame.image.load('imgs/pecapreta.png'), 'pos': posJogador2[(1, 3)], 'livre': True,
     'base': posJogador2[(1, 3)], 'player': 2},
]

# matriz 6x6 com valores todos None
matrizTabuleiro = [[None for x in range(6)] for y in range(6)]

posTabuleiro = {}
for i in range(6):
    for j in range(6):
        posTabuleiro[(i, j)] = (TABULEIROORIGEM[0] + i * 80, TABULEIROORIGEM[1] + j * 80)


# Funçao que retorna as coordenadas x, y em relaçao ao tabuleiro
def getCoordenadas(posX, poxY):
    x = (posX - TABULEIROORIGEM[0]) // 80
    y = (poxY - TABULEIROORIGEM[1]) // 80
    return (x, y)


# Definir funcao pegarPeca
def pegarPecaLivre(pecas):
    for peca in pecas:
        if peca['livre']:
            peca['livre'] = False
            return peca
    return None


# Defininda a função jogar
def jogar(player, coor, matriz):
    """
    Pega uma peça livre na base
    move a peça para a posição do clique no tabuleiro
    chama a função empurrar a partir das coordenadas da peça
    """
    pecas = None
    if player == '1':
        pecas = pecasJogador1
    elif player == '2':
        pecas = pecasJogador2

    peca = pegarPecaLivre(pecas)
    peca['pos'] = posTabuleiro[coor]
    matriz[coor[1]][coor[0]] = peca
    empurrar(coor, matriz)


# Funcão para mover a peça
def mover(peca, origem, destino, matriz):
    """
    Caso as coordenadas do destino esteja no tabuleiro e não exista um peça la
    move-se a peca para o destino
    caso as coordenadas do destino esteja fora do tabuleiro
    move-se a peça para sua base
    """

    x = destino[0]
    y = destino[1]
    if (0 <= x <= 5) and (0 <= y <= 5):
        peca2 = matriz[y][x]
        if not peca2:
            matriz[origem[1]][origem[0]] = None
            matriz[destino[1]][destino[0]] = peca
            peca['pos'] = posTabuleiro[destino]

    else:
        matriz[origem[1]][origem[0]] = None
        peca['pos'] = peca['base']
        peca['livre'] = True


# Funçao empurrar as peças:
def empurrar(coor, matriz):
    """
    Para cada uma das oito direções
    move-se uma uma casa a partir da peça parando na extremidade ou ao encontrar uma peça
    caso exista uma peca guarda-se o movimento contendo a peca a posição de origem e a de destino
    chama a função mover() para cada movimento.
    """
    movimentos = []

    for i, j in [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]:

        x = coor[0] + i
        y = coor[1] + j
        peca = None
        while (0 <= x <= 5) and (0 <= y <= 5):
            peca = matrizTabuleiro[y][x]
            x += i
            y += j
            if peca:
                break

        if peca:
            movimentos.append((peca, (x - i, y - j), (x, y)))

    for peca, origem, destino in movimentos:
        mover(peca, origem, destino, matriz)


def noTabuleiro(coor):
    x = coor[0]
    y = coor[1]
    return (0 <= x <= 5) and (0 <= y <= 5)


def verificarJogada(matriz, surface):

    for linha in range(len(matriz)):
        for peca in matriz[linha]:
            if peca:
                coor = getCoordenadas(peca['pos'][0], peca['pos'][1])
                player = peca['player']

                for i, j in [(0, -1), (1, -1), (1, 0), (1, 1)]:
                    if marcarJogada(surface, coor, player, (i, j)):
                        return True
    return marcarTodos(matriz, surface)


def marcarTodos(matriz, surface):
    player1 = []
    player2 = []
    for linha in range(len(matriz)):
        for peca in matriz[linha]:
            if peca:
                if peca['player'] == 1:
                    player1.append((peca['pos'][0] + 40, peca['pos'][1] + 40))
                if peca['player'] == 2:
                    player2.append((peca['pos'][0] + 40, peca['pos'][1] + 40))

    if len(player1) == 8:
        for coor in player1:
            pygame.draw.circle(surface, (255, 0, 0), coor, 40, 4)
        return True

    elif len(player2) == 8:
        for coor in player2:
            pygame.draw.circle(surface, (255, 0, 0), coor, 40, 4)
        return True
    return False


def marcarJogada(surface, coor, player, dir):
    xA = coor[0] + dir[0]
    yA = coor[1] + dir[1]
    xB = coor[0] - dir[0]
    yB = coor[1] - dir[1]
    if(0 <= xA <= 5) and (0 <= yA <= 5) and (0 <= xB <= 5) and (0 <= yB <= 5):
        pecaA = matrizTabuleiro[yA][xA]
        pecaB = matrizTabuleiro[yB][xB]
        if pecaA and pecaB:

            if pecaA['player'] == player and pecaB['player'] == player:
                x1, y1 = pecaA['pos']
                x1 += 40
                y1 += 40
                x2, y2 = matrizTabuleiro[coor[1]][coor[0]]['pos']
                x2 += 40
                y2 += 40
                x3, y3 = pecaB['pos']
                x3 += 40
                y3 += 40
                pygame.draw.circle(surface, (255, 0, 0), (x1, y1), 40, 4)
                pygame.draw.circle(surface, (255, 0, 0), (x2, y2), 40, 4)
                pygame.draw.circle(surface, (255, 0, 0), (x3, y3), 40, 4)
                return True
        return False


def iniciarJogo():

    for peca in pecasJogador1:
        peca['pos'] = peca['base']
        peca['livre'] = True
    for peca in pecasJogador2:
        peca['pos'] = peca['base']
        peca['livre'] = True
    limparTabuleiro()


def limparTabuleiro():
    for i in range(6):
        for j in range(6):
            matrizTabuleiro[i][j] = None







