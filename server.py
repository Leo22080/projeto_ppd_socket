import pygame
from gekitai import *


# Inicializando módulos de Pygame
pygame.init()

grade = Tabuleiro()

# Criando uma janela
janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption('Gekitai')

#threading
import threading


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True 
    thread.start()


# socket
import socket

HOST = "127.0.0.1"
PORT = 51000

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
    global turn, chatOn, msg, connection_established
    while True:
        data = conn.recv(1024).decode()
        if data == 'iniciar':
                grade.iniciarJogo()
                fimdeJogo = False
                playing = 'True'
        elif data == 'chat':
            chatOn = not chatOn
        elif chatOn:
            chat.escrever(data, 'dir')
        elif data == 'desistir':
            print('Finalizando conexao do cliente')
            grade.iniciarJogo()
            fimdeJogo = False
            turn = True
            playing = 'True'
            conn.send('desistir'.encode())
            conn.close()
            connection_established = False
            create_thread(waiting_for_connection)
            break
        else:
            data = data.split('-')
            x, y = int(data[0]), int(data[1])
            if data[2] == 'yourturn':
                turn = True
            if data[3] == 'False':
                fimdeJogo = True
            grade.jogar('2', (x, y))
            print(data)


def waiting_for_connection():
    global conn, addr, connection_established

    print("Waiting for connection....")
    
    conn , addr = sock.accept() # espera por uma conexão, e bloqueia qualquer novo thread 
    print("Client is connected!!!")

    connection_established = True

    receive_data()

create_thread(waiting_for_connection)

#Definição do chat
chat = Chat()

player = '1'
turn = True
playing = 'True'
chatOn = False

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
                if turn and not fimdeJogo and not chatOn:
                    rect = tabuleiro.get_rect().move(TABULEIROORIGEM)
                    if rect.collidepoint(pygame.mouse.get_pos()):

                        x, y = getCoordenadas(evento.pos[0], evento.pos[1])
                        if not grade.matrizTabuleiro[y][x]:
                            
                            send_data = '{}-{}-{}-{}'.format(x, y, 'yourturn', playing).encode()
                            conn.send(send_data)

                            grade.jogar(player, (x, y))
                            turn = False
                                                        
        if evento.type == pygame.KEYDOWN and connection_established:
            if evento.key == pygame.K_ESCAPE and fimdeJogo:
                grade.iniciarJogo()
                fimdeJogo = False
                playing = 'True'
                conn.send('iniciar'.encode())
                
            if evento.key == pygame.K_F12:
                chatOn = not chatOn
                conn.send('chat'.encode())

            if chatOn:
                if evento.key == pygame.K_BACKSPACE:
                    chat.linhaMestra.msg = chat.linhaMestra.msg[:-1]
                elif evento.key == pygame.K_RETURN and not chat.linhaMestra.msg == '':
                    try:
                        conn.send(chat.linhaMestra.msg.encode())
                        chat.escrever(chat.linhaMestra.msg, 'esq')
                        chat.linhaMestra.msg = ''

                    except:
                        pass
                else:
                    chat.linhaMestra.msg += evento.unicode

    # Preenchendo o fundo da janela com uma cor
    janela.fill((192, 192, 192))

    # preenchendo o fundo de janela com a sua imagem    
    janela.blit(titulo, ((LARGURAJANELA - LARGURATITULO) / 2, 0))
    janela.blit(tabuleiro, (TABULEIROORIGEM))

    for peca in pecasJogador1:
        janela.blit(peca.imagem, peca.pos)
        peca.atualizar()
    for peca in pecasJogador2:
        janela.blit(peca.imagem, peca.pos)
        peca.atualizar()

    fimdeJogo = grade.verificarJogada(janela)
    if fimdeJogo:
        playing = 'False'

    if chatOn:
        chat.drawChat(janela)
            
    # mostrando na tela tudo o que foi desenhado
    pygame.display.update()

# Encerrando módulos de Pygame
pygame.quit()
