import random
from pygame import Rect

# Define o tamanho da janela (em pixels)
WIDTH = 800
HEIGHT = 600
TITLE = "Teste Kodland"
GRAVITY = 0.5

# Cenas do Jogo
MENU = "menu"
JOGO = "jogando"
game_state = MENU

# Classe para animação do personagem e inimigos
class Animacao:
    def __init__(self, lista_sprites, intervalo=0.15):
        self.sprites = lista_sprites
        self.intervalo = intervalo
        self.tempo = 0
        self.atual = 0

    def update(self, dt):
        self.tempo += dt
        if self.tempo >= self.intervalo:
            self.tempo = 0
            self.atual = (self.atual + 1) % len(self.sprites)

    def frame_atual(self):
        return self.sprites[self.atual]
    
# Classe para o jogador
class Player:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 24, 24)
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.has_key = False
        
        # Animações
        self.walk_anim = Animacao(["player_1", "player_2"], 0.1)
        self.idle_anim = Animacao(["player_1"], 0.0)
        self.current_anim = self.idle_anim

    def update(self, dt, chaos):
        # Andar
        self.vel_x = 0
        if keyboard.left:
            self.vel_x = -2
        if keyboard.right:
            self.vel_x = 2
        
        # Pular
        if (keyboard.up) and self.on_ground:
            self.vel_y = -12

        # Gravidade e Movimento
        self.vel_y += GRAVITY
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Colisão com chao
        self.on_ground = False
        for chao in chaos:
            if self.rect.colliderect(chao):
                if self.vel_y > 0: # Se tiver caindp
                    self.rect.bottom = chao.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0: # Pulando e batendo a cabeça
                    self.rect.top = chao.bottom
                    self.vel_y = 0

        # Atualizar animações
        if abs(self.vel_x) > 0:
            self.current_anim = self.walk_anim
        else:
            self.current_anim = self.idle_anim
        self.current_anim.update(dt)

    def draw(self):
        screen.blit(self.current_anim.frame_atual(), (self.rect.x, self.rect.y))

# Instacia o jogador 
jogador = Player(50, 520)

#Classe para o inimigos
class Inimigo:
    def __init__(self, x, y, direcao):
        self.rect = Rect(x, y, 30, 20)
        self.direcao = direcao 
        self.velocidade = 3
        self.anim = Animacao(["enemy_1", "enemy_2", "enemy_3"], 0.2)

    def update(self, dt):
        self.rect.x += self.velocidade * self.direcao
        self.anim.update(dt)

    def draw(self):
        screen.blit(self.anim.frame_atual(), (self.rect.x, self.rect.y))

#Classe para os canhões
class Canhao:
    def __init__(self, x, y, direcao):
        self.actor = Actor("gun", pos=(x, y))
        self.direcao = direcao 
        if direcao == 1:
            self.actor.angle = -90  # Vira para a direita
        else:
            self.actor.angle = 90   # Vira para a esquerda
        self.timer = 0
        self.fire_rate = 2.5 

    def update(self, dt, lista_sprites):
        self.timer += dt
        if self.timer >= self.fire_rate:
            novo_inimigo = Inimigo(self.actor.x, self.actor.y, self.direcao)
            lista_sprites.append(novo_inimigo)
            self.timer = random.randint(0, 3)

    def draw(self):
        self.actor.draw()

# Cria o cenário
chave = Rect(40, 40, 30, 30)
porta = Rect(730, 510, 40, 60)
canhoes = [Canhao(10, 100, 1), Canhao(10, 380, 1), Canhao(790, 230, -1)]
inimigos = [] 
chaos = [
    Rect(0, 580, 800, 30),    
    Rect(100, 150, 100, 20),  
    Rect(350, 150, 100, 20),
    Rect(600, 150, 100, 20),
    Rect(250, 300, 100, 20),
    Rect(500, 300, 100, 20),
    Rect(100, 450, 100, 20),
    Rect(350, 450, 100, 20),
    Rect(600, 450, 100, 20),
]

# Função pra desenhar as plataformas repetidas
def draw_chaos_repetidos(rect, image_name):
    #Definindo tamanho do sprite
    tam_x = 18  
    tam_y = 25 

    # Loop para preencher a largura e a altura do Rect
    for x in range(rect.left, rect.right, tam_x):
        for y in range(rect.top, rect.bottom, tam_y):
            screen.blit(image_name, (x, y))

def update(dt):
    global game_state, inimigos
    if game_state == JOGO:
        jogador.update(dt, chaos)
        
        # Atualizar Canhões e Inimigos
        for c in canhoes:
            c.update(dt, inimigos)
        
        for e in inimigos[:]:
            e.update(dt)
            # Colisão jogador vs inimigo
            if jogador.rect.colliderect(e.rect):
                reset_level()

        # Colisão com Chave
        if jogador.rect.colliderect(chave) and not jogador.has_key:
            jogador.has_key = True

        # Colisão com Porta
        if jogador.rect.colliderect(porta) and jogador.has_key:
            print("Você venceu!")
            game_state = MENU

def reset_level():
    global inimigos
    jogador.rect.topleft = (50, 520)
    jogador.has_key = False
    inimigos = []

# Criar a cena do menu
botao_inicio = Rect(250, 200, 300, 60)

def draw_menu():
    # Cria botão Iniciar
    screen.draw.filled_rect(botao_inicio, (50, 150, 50))
    screen.draw.text("JOGAR", center=botao_inicio.center, fontsize=30, color="white")

# Se clicar, muda de cena
def on_mouse_down(pos):
    global game_state
    if game_state == MENU:
        if botao_inicio.collidepoint(pos):
           game_state = JOGO

def draw():
    screen.clear()
    if game_state == MENU:
        draw_menu()
    else:
        for c in chaos:
            draw_chaos_repetidos(c, "ground_2")

        if not jogador.has_key:
            screen.blit("key", (chave.x, chave.y))
        
        screen.blit("door", (porta.x, porta.y))
        
        for c in canhoes: c.draw()
        for e in inimigos: e.draw()
        jogador.draw()