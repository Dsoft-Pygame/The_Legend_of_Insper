import pygame

from personagens.personagem import Personagem
from personagens.projetil import Golpe, Projetil
from settings import BLUE, GREEN, ORANGE, RED, WHITE


class Heroi(Personagem):
    """O personagem do jogador: anda com WASD, ataca com ESPAÇO e usa o especial com o SHIFT esquerdo.

    Cada classe filha muda os números e troca os métodos atacar e especial.
    """

    def __init__(self, x, y, cor, vida, velocidade, nome, descricao):
        super().__init__(x, y, 12, cor, vida, velocidade)   # 12 px: cabe folgado num corredor de 16
        self.nome = nome
        self.descricao = descricao
        self.tempo_invulneravel = 0.8
        self.dano = 0                      # dano do ataque normal (aparece no cartão da classe)
        self.tempo_ataque = 0.5            # segundos entre um ataque e outro
        self.tempo_especial = 4
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
        super().__init__(x, y, BLUE, 60, 70, "Mago", "Frágil, mas com dano alto à distância.")
        self.dano = 30
        self.tempo_ataque = 0.6
        self.tempo_especial = 5

    def atacar(self):
        velocidade = self.direcao * 90
        bola = Projetil(self.posicao, velocidade, tamanho=8, cor=RED, dano=self.dano, duracao=1.5, dono="heroi")
        return [bola]

    def especial(self):
        bolas = []
        for i in range(12):                # uma bola a cada 30 graus
            velocidade = self.direcao.rotate(i * 30) * 90
            bola = Projetil(self.posicao, velocidade, tamanho=8, cor=RED, dano=20, duracao=1, dono="heroi")
            bolas.append(bola)
        return bolas


class Arqueiro(Heroi):
    """Flecha rápida. Especial: três flechas em leque."""

    def __init__(self, x, y):
        super().__init__(x, y, GREEN, 80, 100, "Arqueiro", "Ágil, ataca rápido de longe.")
        self.dano = 10
        self.tempo_ataque = 0.3
        self.tempo_especial = 3

    def atacar(self):
        velocidade = self.direcao * 200
        flecha = Projetil(self.posicao, velocidade, tamanho=4, cor=WHITE, dano=self.dano, duracao=1, dono="heroi")
        return [flecha]

    def especial(self):
        flechas = []
        for angulo in (-15, 0, 15):
            velocidade = self.direcao.rotate(angulo) * 200
            flecha = Projetil(self.posicao, velocidade, tamanho=4, cor=WHITE, dano=10, duracao=1, dono="heroi")
            flechas.append(flecha)
        return flechas


class Barbaro(Heroi):
    """Machadada logo na frente. Especial: giro que acerta todos em volta."""

    def __init__(self, x, y):
        super().__init__(x, y, ORANGE, 140, 75, "Bárbaro", "Resistente, luta de perto.")
        self.dano = 35
        self.tempo_ataque = 0.5
        self.tempo_especial = 4

    def atacar(self):
        centro = self.posicao + self.direcao * 15   # metade do herói (6) + metade do golpe (9)
        return [Golpe(centro, tamanho=18, dano=self.dano, duracao=0.1, atravessa=False)]

    def especial(self):
        tamanho = 12 + 2 * 32                       # o herói (12) mais 32 px de cada lado
        return [Golpe(self.posicao, tamanho=tamanho, dano=25, duracao=0.3, atravessa=True)]
