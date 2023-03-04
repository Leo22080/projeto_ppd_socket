#  Projeto de Sockets
## 1) Objetivo: Implementar o Jogo *Gekitai* com  Sockets
Gekitai, traduzido do Japonês significa repelir, e as peças ao serem colocadas vão repelindo
ou empurrando outras peças que já estão no tabuleiro. O tabuleiro é quadrado com 6 linhas
e 6 colunas, ou seja, são 36 casas. Um jogo para dois jogadores e cada um tem 8 peças.
### Objetivo do jogo
Colocar três peças alinhadas em qualquer direção (depois de realizar os “empurrões” ou
deixar as oito peças de um mesmo jogador no tabuleiro.
### Regras
Cada jogador joga uma peça no tabuleiro de forma intercalada. Ao posicionar uma peça, a
mesmo “empurra” outras peças que estão nas casas ao redor, inclusive as do próprio
jogador. Não se pode empurrar duas ou mais peças alinhadas. Ao empurrar uma peça e essa
sair do tabuleiro, a mesma retorna ao jogador.
## 2) Funcionalidades Básicas
- [x] Controle de turno, com definição de quem inicia a partida
- [x] Movimentação de peças do tabuleiro
- [ ] Desistência
- [x] Chat para comunicação durante toda a partida
## 3) Implementação ![alt](https://www.pygame.org/docs/_static/pygame_tiny.png?f=webp&w=12)
- Esse jogo foi escrito em Python com a biblioteca Pygame <https://www.pygame.org>
- Pygame é uma biblioteca de jogos multiplataforma feita para ser utilizada em conjunto com a linguagem de programação Python
- Pygame não é uma biblioteca nativa do python precisa ser instalada:   
`python -m pip install -U pygame`
- Cada jogador alterna sua vez de jogar onde ele posiciona sua peça no tabuleiro em um espaço vazio quando possui peças
- O *"empurrar"* é feito de forma altomática.
- Uma vitória é atingida quando o jogador consegue alinhar três de suas peças em qualquer direção ou quando todas suas peças estão no tabuleiro
- Após a uma vitória o jogo pode ser reiniciado precionando a tecla ESC por qualquer um dos jogadores
- A tecla F-12 ativa e desativa o chat
