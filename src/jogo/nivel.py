import pygame

from jogo.mapa import Mapa
from settings import BLACK, BROWN, DARK_GRAY, GRAY, YELLOW


class Nivel:
    """Um nível em andamento: o mapa, o herói e os projéteis.

    A cada quadro faz todo mundo andar e tira os projéteis que acabaram.
    """

    def __init__(self, nome, arquivo, heroi):
        self.nome = nome
        self.mapa = Mapa(arquivo)
        self.heroi = heroi
        self.heroi.posicao = pygame.Vector2(self.mapa.inicio_heroi)
        self.inimigos = []                # os inimigos entram na próxima etapa
        self.projeteis = []
        self.tempo = 0                    # segundos neste nível (a saída pisca com ele)

    def atualizar(self, dt):
        self.tempo += dt
        self.heroi.atualizar(dt, self.mapa)          # 1. o herói anda

        restantes = []                               # 2. os projéteis andam
        for projetil in self.projeteis:
            projetil.atualizar(dt)
            if not projetil.acabou(self.mapa):       # somem na parede ou no fim do tempo
                restantes.append(projetil)
        self.projeteis = restantes

    def esta_limpo(self):
        """Sem inimigos, a saída abre."""
        return len(self.inimigos) == 0

    def desenhar(self, superficie, camera):
        superficie.fill(BLACK)
        chao = pygame.Rect(0, 0, self.mapa.largura, self.mapa.altura)
        pygame.draw.rect(superficie, DARK_GRAY, camera.para_tela(chao))
        for parede in self.mapa.paredes:
            if camera.esta_visivel(parede):
                pygame.draw.rect(superficie, GRAY, camera.para_tela(parede))

        if self.mapa.saida is not None:
            cor_saida = BROWN
            if self.esta_limpo() and int(self.tempo * 4) % 2 == 0:
                cor_saida = YELLOW                   # aberta, ela pisca
            pygame.draw.rect(superficie, cor_saida, camera.para_tela(self.mapa.saida))

        for projetil in self.projeteis:
            projetil.desenhar(superficie, camera)
        self.heroi.desenhar(superficie, camera)
