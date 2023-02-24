import pygame
from tabuleiro import *

# Inicializando módulos de Pygame
pygame.init()

# Criando uma janela
janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption('Gekitai')

#threading
import threading


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True #this makes is so that these thread will auto quit before the code ends running
    thread.start()


# socket
import socket

HOST = "127.0.0.1"
PORT = 50000

ADDR = (HOST, PORT)
connection_established = False
conn, addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.bind(ADDR)
except socket.error as e:
    print(str(e))

sock.listen(1)

def receive_data():
    global turn
    while True:
        data = conn.recv(1024).decode()
        data = data.split('-')
        x, y = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            fimdeJogo = True
        jogar('2', (x, y), matrizTabuleiro)
        print(data)


def waiting_for_connection():
    global conn, addr, connection_established

    print("Waiting for connection....")
    
    conn , addr = sock.accept() # it will wait for a connection , also blocks any new threads 
    print("Client is connected!!!")

    connection_established = True

    receive_data()

create_thread(waiting_for_connection)


player = '1'
turn = True
playing = 'True'

deve_continuar = True
fimdeJogo = False

# Loop do jogo
while deve_continuar:

    # Checando eventos
    for evento in pygame.event.get():
        # Se for um evento QUIT
        if evento.type == pygame.QUIT:
            deve_continuar = False

        # quando o botao esquerdo do mouse é pressionado
        if evento.type == pygame.MOUSEBUTTONDOWN and connection_established:
            if pygame.mouse.get_pressed()[0]:
                if turn and not fimdeJogo:
                    rect = tabuleiro.get_rect().move(TABULEIROORIGEM)
                    if rect.collidepoint(pygame.mouse.get_pos()):

                        x, y = getCoordenadas(evento.pos[0], evento.pos[1])
                        if not matrizTabuleiro[y][x]:

                            
                            send_data = '{}-{}-{}-{}'.format(x, y, 'yourturn', playing).encode()
                            conn.send(send_data)

                            jogar(player, (x, y), matrizTabuleiro)
                            turn = False
                                                        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE and fimdeJogo:
                iniciarJogo()
                fimdeJogo = False
                playing = 'True'
            elif evento.key == pygame.K_BACKSPACE:
                deve_continuar = False

    # Preenchendo o fundo da janela com uma cor
    janela.fill((192, 192, 192))

    # preenchendo o fundo de janela com a sua imagem    
    janela.blit(titulo, ((LARGURAJANELA - LARGURATITULO) / 2, 0))
    janela.blit(tabuleiro, (TABULEIROORIGEM))

    for peca in pecasJogador1:
        janela.blit(peca['peca'], peca['pos'])
    for peca in pecasJogador2:
        janela.blit(peca['peca'], peca['pos'])

    fimdeJogo = verificarJogada(matrizTabuleiro, janela)
    if fimdeJogo:
        playing = 'False'

    # mostrando na tela tudo o que foi desenhado
    pygame.display.update()

# Encerrando módulos de Pygame
pygame.quit()
