import random

import pygame

from personagens.personagem import Personagem
from settings import CYAN, PINK, PURPLE, WHITE


class Inimigo(Personagem):
    """Um monstro: anda à toa até o herói chegar perto e então vai atrás dele.

    Dá dano quando encosta no herói e vale pontos quando morre. Como na main, ainda
    não aparece no nível: criar os inimigos das letras do mapa é a T51.
    """

    def __init__(self, x, y, tamanho, cor, vida, velocidade, nome, dano_contato, pontos, raio_alerta):
        super().__init__(x, y, tamanho, cor, vida, velocidade)
        self.nome = nome
        self.dano_contato = dano_contato   # dano quando encosta no herói
        self.pontos = pontos               # quanto vale quando morre
        self.raio_alerta = raio_alerta     # a partir de quantos pixels começa a perseguir
        self.tempo_vagando = 1.5           # segundos andando para um lado antes de sortear outro
        self.tempo_sorteio = 0             # quanto falta para sortear de novo
        self.direcao_vagando = pygame.Vector2(0, 0)

    def atualizar(self, dt, heroi, mapa):
        """Persegue o herói se ele estiver perto; senão, vaga. Devolve os projéteis que criou."""
        caminho = heroi.posicao - self.posicao
        if 0 < caminho.length() <= self.raio_alerta:
            self.direcao = caminho.normalize()
            self.mover(self.direcao, dt, mapa)
        else:
            self.vagar(dt, mapa)
        return []                          # os inimigos comuns não atiram

    def vagar(self, dt, mapa):
        """Anda à toa: de tempos em tempos sorteia uma direção ou fica parado."""
        self.tempo_sorteio -= dt
        if self.tempo_sorteio <= 0:
            self.tempo_sorteio = self.tempo_vagando
            if random.random() < 0.3:      # 30% das vezes fica parado
                self.direcao_vagando = pygame.Vector2(0, 0)
            else:
                self.direcao_vagando = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
        if self.direcao_vagando.length() > 0:
            self.mover(self.direcao_vagando * 0.5, dt, mapa)   # vagando, anda na metade da velocidade


class Slime(Inimigo):
    """Lento e fraco: o inimigo do primeiro andar."""

    def __init__(self, x, y):
        super().__init__(x, y, 12, CYAN, 20, 30, "Slime", 10, 50, 80)


class Esqueleto(Inimigo):
    """Mais forte e mais rápido que o slime, e percebe o herói de mais longe."""

    def __init__(self, x, y):
        super().__init__(x, y, 12, WHITE, 40, 55, "Esqueleto", 15, 80, 112)
        self.tempo_vagando = 1


class Morcego(Inimigo):
    """Rápido e frágil. Por enquanto persegue reto como os outros: o zigue-zague
    ainda está no branch task-46.
    """

    def __init__(self, x, y):
        super().__init__(x, y, 12, PINK, 10, 90, "Morcego", 5, 70, 120)
        self.tempo_vagando = 1


class Dragao(Inimigo):
    """O chefe do Topo da Torre, maior que os outros. Por enquanto só tem os números:
    os ataques e o jeito de lutar do chefe ainda faltam.
    """

    def __init__(self, x, y):
        super().__init__(x, y, 24, PURPLE, 600, 45, "Dragão Ancião", 25, 2000, 240)
