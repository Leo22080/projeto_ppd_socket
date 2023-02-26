import pygame, os

titulo = pygame.image.load(os.path.join('imgs', 'titulo.png'))
tabuleiro = pygame.image.load(os.path.join('imgs', 'tabuleiro.png'))

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


posTabuleiro = {}
for i in range(6):
    for j in range(6):
        posTabuleiro[(i, j)] = (TABULEIROORIGEM[0] + i * 80, TABULEIROORIGEM[1] + j * 80)


# Funçao que retorna as coordenadas x, y em relaçao ao tabuleiro
def getCoordenadas(posX, poxY):
    x = (posX - TABULEIROORIGEM[0]) // 80
    y = (poxY - TABULEIROORIGEM[1]) // 80
    return (x, y)


class Peca:
    def __init__(self, diretorio, nome, pos, player):
        self.imagem = pygame.image.load(os.path.join(diretorio, nome))
        self.pos = pos
        self.livre = True
        self.base = pos
        self.player = player

    # Funcão para mover a peça
    def mover(self, origem, destino, matriz):
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
                matriz[destino[1]][destino[0]] = self
                self.pos = posTabuleiro[destino]

        else:
            matriz[origem[1]][origem[0]] = None
            self.pos = self.base
            self.livre = True


pecasJogador1 = [Peca('imgs', 'pecabranca.png', pos, '1') for pos in posJogador1.values()]
pecasJogador2 = [Peca('imgs', 'pecapreta.png', pos, '2') for pos in posJogador2.values()]

pecasJogador1.reverse()

# Definir funcao pegarPeca
def pegarPecaLivre(pecas):
    for peca in pecas:
        if peca.livre:
            peca.livre = False
            return peca
    return None


class Tabuleiro:
    def __init__(self):
        self.matrizTabuleiro = [[None for x in range(6)] for y in range(6)]
        

    # Defininda a função jogar
    def jogar(self, player, coor):
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
        peca.pos = posTabuleiro[coor]
        self.matrizTabuleiro[coor[1]][coor[0]] = peca
        self.empurrar(coor)

    # Funçao empurrar as peças:
    def empurrar(self, coor):
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
                peca = self.matrizTabuleiro[y][x]
                x += i
                y += j
                if peca:
                    break

            if peca:
                movimentos.append((peca, (x - i, y - j), (x, y)))

        for peca, origem, destino in movimentos:
            peca.mover(origem, destino, self.matrizTabuleiro)


    def verificarJogada(self, surface):
        matriz = self.matrizTabuleiro

        for linha in range(len(matriz)):
            for peca in matriz[linha]:
                if peca:
                    coor = getCoordenadas(peca.pos[0], peca.pos[1])
                    player = peca.player

                    for i, j in [(0, -1), (1, -1), (1, 0), (1, 1)]:
                        if self.marcarJogada(surface, coor, player, (i, j)):
                            return True
                        
        return self.marcarTodos(surface)


    def marcarTodos(self, surface):
        matriz = self.matrizTabuleiro
        
        player1 = []
        player2 = []
        for linha in range(len(matriz)):
            for peca in matriz[linha]:
                if peca:
                    if peca.player == '1':
                        player1.append((peca.pos[0] + 40, peca.pos[1] + 40))
                    if peca.player == '2':
                        player2.append((peca.pos[0] + 40, peca.pos[1] + 40))

        if len(player1) == 8:
            for coor in player1:
                pygame.draw.circle(surface, (255, 0, 0), coor, 40, 4)
            return True

        elif len(player2) == 8:
            for coor in player2:
                pygame.draw.circle(surface, (255, 0, 0), coor, 40, 4)
            return True
        return False


    def marcarJogada(self, surface, coor, player, direcao):
        xA = coor[0] + direcao[0]
        yA = coor[1] + direcao[1]
        xB = coor[0] - direcao[0]
        yB = coor[1] - direcao[1]
        if(0 <= xA <= 5) and (0 <= yA <= 5) and (0 <= xB <= 5) and (0 <= yB <= 5):
            pecaA = self.matrizTabuleiro[yA][xA]
            pecaB = self.matrizTabuleiro[yB][xB]
            if pecaA and pecaB:

                if pecaA.player == player and pecaB.player == player:
                    x1, y1 = pecaA.pos
                    x1 += 40
                    y1 += 40
                    x2, y2 = self.matrizTabuleiro[coor[1]][coor[0]].pos
                    x2 += 40
                    y2 += 40
                    x3, y3 = pecaB.pos
                    x3 += 40
                    y3 += 40
                    pygame.draw.circle(surface, (255, 0, 0), (x1, y1), 40, 4)
                    pygame.draw.circle(surface, (255, 0, 0), (x2, y2), 40, 4)
                    pygame.draw.circle(surface, (255, 0, 0), (x3, y3), 40, 4)
                    return True
            return False


    def iniciarJogo(self):

        for peca in pecasJogador1:
            peca.pos = peca.base
            peca.livre = True
        for peca in pecasJogador2:
            peca.pos = peca.base
            peca.livre = True
        self.limparTabuleiro()


    def limparTabuleiro(self):
        for i in range(6):
            for j in range(6):
                self.matrizTabuleiro[i][j] = None


        
