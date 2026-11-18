import pygame

from personagens.personagem import Personagem
from personagens.projetil import Golpe, Projetil
from settings import BLUE, GREEN, ORANGE, RED, WHITE
from ui import carregar_imagem

class Heroi(Personagem):
    """O personagem do jogador: anda com WASD, ataca com ESPAÇO e usa o especial com o SHIFT esquerdo.

    Cada classe filha muda os números e troca os métodos atacar e especial.
    """

    def __init__(self, x, y, cor, vida, velocidade, nome, descricao):
        super().__init__(x, y, 24, cor, vida, velocidade)   # 24 px: cabe folgado num corredor de 32
        self.nome = nome
        self.descricao = descricao
        self.tempo_invulneravel = 0.8
        self.dano = 0                      # dano do ataque normal (aparece no cartão da classe)
        self.tempo_ataque = 0.5            # segundos entre um ataque e outro
        self.tempo_especial = 4
        self.empurrao_ataque = 0           # knockback dos ataques, em pixels por segundo (cada classe tem o seu)
        self.recarga_ataque = 0            # quanto falta para poder atacar de novo
        self.recarga_especial = 0

    def atualizar(self, dt, mapa):
        teclas = pygame.key.get_pressed()
        direcao = pygame.Vector2(0, 0)
        if teclas[pygame.K_a]:
            direcao.x -= 1
        if teclas[pygame.K_d]:
            direcao.x += 1
        if teclas[pygame.K_w]:
            direcao.y -= 1
        if teclas[pygame.K_s]:
            direcao.y += 1
        if direcao.length() > 0:
            self.direcao = direcao.normalize()   # na diagonal não fica mais rápido
            self.mover(self.direcao, dt, mapa)
        self.recarga_ataque = max(0, self.recarga_ataque - dt)
        self.recarga_especial = max(0, self.recarga_especial - dt)
        self.invulneravel = max(0, self.invulneravel - dt)

    def usar_ataque(self):
        """A TelaJogo chama quando aperta ESPAÇO. Devolve a lista de projéteis criados."""
        if self.recarga_ataque > 0:
            return []
        self.recarga_ataque = self.tempo_ataque
        return self.atacar()

    def usar_especial(self):
        """A TelaJogo chama quando aperta o SHIFT esquerdo."""
        if self.recarga_especial > 0:
            return []
        self.recarga_especial = self.tempo_especial
        return self.especial()

    def atacar(self):
        return []                          # cada classe troca este método

    def especial(self):
        return []                          # e este também


class Mago(Heroi):
    """Bola de fogo lenta e forte. Especial: anel com 12 bolas de fogo."""

    def __init__(self, x, y):
        super().__init__(x, y, BLUE, 60, 140, "Mago", "Frágil, mas com dano alto à distância.")
        self.dano = 30
        self.tempo_ataque = 0.6
        self.tempo_especial = 5
        self.empurrao_ataque = 250         # bola de fogo pesada: empurra bem
        self.imagem = carregar_imagem("mago.png")

    def atacar(self):
        velocidade = self.direcao * 180
        bola = Projetil(self.posicao, velocidade, tamanho=16, cor=RED, dano=self.dano, duracao=1.5, dono="heroi",
                        empurrao=self.empurrao_ataque)
        return [bola]

    def especial(self):
        bolas = []
        for i in range(12):                # uma bola a cada 30 graus
            velocidade = self.direcao.rotate(i * 30) * 180
            bola = Projetil(self.posicao, velocidade, tamanho=16, cor=RED, dano=20, duracao=1, dono="heroi",
                            empurrao=self.empurrao_ataque)
            bolas.append(bola)
        return bolas


class Arqueiro(Heroi):
    """Flecha rápida. Especial: três flechas em leque."""

    def __init__(self, x, y):
        super().__init__(x, y, GREEN, 80, 200, "Arqueiro", "Ágil, ataca rápido de longe.")
        self.dano = 10
        self.tempo_ataque = 0.3
        self.tempo_especial = 3
        self.empurrao_ataque = 120         # flecha leve: empurra pouco
        self.imagem = carregar_imagem("arqueiro.png")

    def atacar(self):
        velocidade = self.direcao * 400
        flecha = Projetil(self.posicao, velocidade, tamanho=8, cor=WHITE, dano=self.dano, duracao=1, dono="heroi",
                          empurrao=self.empurrao_ataque)
        return [flecha]

    def especial(self):
        flechas = []
        for angulo in (-15, 0, 15):
            velocidade = self.direcao.rotate(angulo) * 400
            flecha = Projetil(self.posicao, velocidade, tamanho=8, cor=WHITE, dano=10, duracao=1, dono="heroi",
                              empurrao=self.empurrao_ataque)
            flechas.append(flecha)
        return flechas


class Barbaro(Heroi):
    """Machadada logo na frente. Especial: giro que acerta todos em volta."""

    def __init__(self, x, y):
        super().__init__(x, y, ORANGE, 140, 150, "Bárbaro", "Resistente, luta de perto.")
        self.dano = 35
        self.tempo_ataque = 0.5
        self.tempo_especial = 4
        self.empurrao_ataque = 380         # machadada: a que empurra mais
        self.imagem = carregar_imagem("barbaro.png")

    def atacar(self):
        centro = self.posicao + self.direcao * 30   # metade do herói (12) + metade do golpe (18)
        return [Golpe(centro, tamanho=36, dano=self.dano, duracao=0.1, atravessa=False,
                      origem=self.posicao, empurrao=self.empurrao_ataque)]

    def especial(self):
        tamanho = 24 + 2 * 64                       # o herói (24) mais 64 px de cada lado
        return [Golpe(self.posicao, tamanho=tamanho, dano=25, duracao=0.3, atravessa=True,
                      origem=self.posicao, empurrao=self.empurrao_ataque * 1.2)]   # o giro joga mais longe
