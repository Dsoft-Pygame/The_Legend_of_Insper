import pygame

from personagens.entidade import Entidade
from settings import YELLOW


class Projetil(Entidade):
    """Tudo que voa e dá dano, como flecha e bola de fogo. Some na parede ou quando o tempo acaba."""

    def __init__(self, posicao, velocidade, tamanho, cor, dano, duracao, dono):
        super().__init__(posicao.x, posicao.y, tamanho, tamanho, cor)
        self.velocidade = pygame.Vector2(velocidade)   # direção e rapidez, em pixels por segundo
        self.dano = dano
        self.duracao = duracao                         # segundos até sumir
        self.dono = dono                               # "heroi" ou "inimigo": não acerta o próprio lado
        self.atravessa = False                         # True: acerta todos que encostar
        self.ja_acertou = []                           # quem já levou dano deste projétil

    def atualizar(self, dt):
        self.posicao += self.velocidade * dt
        self.duracao -= dt

    def acabou(self, mapa):
        return self.duracao <= 0 or self.bateu_na_parede(mapa)

    def bateu_na_parede(self, mapa):
        return not mapa.area_livre(self.retangulo())


class Golpe(Projetil):
    """Golpe corpo a corpo: fica parado, acerta todos na área e some sozinho."""

    def __init__(self, posicao, tamanho, dano, duracao):
        super().__init__(posicao, (0, 0), tamanho, YELLOW, dano, duracao, "heroi")
        self.atravessa = True

    def bateu_na_parede(self, mapa):
        return False                                   # pode encostar na parede sem sumir
