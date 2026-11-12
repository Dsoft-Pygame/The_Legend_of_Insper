import pygame

from jogo.camera import Camera
from jogo.nivel import Nivel
from settings import ALTURA_TELA, LARGURA_TELA, NIVEIS, YELLOW
from telas.tela import Tela
from ui import desenhar_texto


class TelaJogo(Tela):
    """Onde se joga: carrega o nível, passa os ataques para o herói e faz a câmera seguir."""

    def __init__(self, aplicacao):
        super().__init__(aplicacao)
        self.heroi = aplicacao.heroi
        self.indice_nivel = 0             # posição na lista NIVEIS do settings.py
        self.carregar_nivel()

    def carregar_nivel(self):
        """Monta o nível atual e uma câmera do tamanho do mapa dele."""
        nome, arquivo = NIVEIS[self.indice_nivel]
        self.nivel = Nivel(nome, arquivo, self.heroi)
        self.camera = Camera(self.nivel.mapa.largura, self.nivel.mapa.altura)
        self.aviso_nivel = 2              # segundos com o nome do nível no meio da tela

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                self.nivel.projeteis.extend(self.heroi.usar_ataque())
            elif evento.key == pygame.K_LSHIFT:
                self.nivel.projeteis.extend(self.heroi.usar_especial())

    def atualizar(self, dt):
        self.aviso_nivel = max(0, self.aviso_nivel - dt)
        self.nivel.atualizar(dt)
        self.camera.seguir(self.heroi.posicao)

    def desenhar(self, superficie):
        self.nivel.desenhar(superficie, self.camera)
        if self.aviso_nivel > 0:
            desenhar_texto(superficie, self.nivel.nome, (LARGURA_TELA // 2, ALTURA_TELA // 2), YELLOW, 24,
                           centralizado=True)
