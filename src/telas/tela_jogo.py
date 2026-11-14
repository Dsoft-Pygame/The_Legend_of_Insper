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
        self.indice_nivel = 0                      # posição na lista NIVEIS do settings.py
        self.pausado = False            
        self.carregar_nivel()

    def carregar_nivel(self):
        """Monta o nível atual e uma câmera do tamanho do mapa dele."""
        nome, arquivo = NIVEIS[self.indice_nivel]
        self.nivel = Nivel(nome, arquivo, self.heroi)
        self.camera = Camera(self.nivel.mapa.largura, self.nivel.mapa.altura)
        self.aviso_nivel = 2              # segundos com o nome do nível no meio da tela

    def tratar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key == pygame.K_ESCAPE:
            self.pausado = not self.pausado          # ESC pausa e ESC de novo continua
        elif self.pausado:
            return                                   # pausado, as outras teclas não fazem nada
        elif evento.key == pygame.K_SPACE:
            self.nivel.projeteis.extend(self.heroi.usar_ataque())
        elif evento.key == pygame.K_LSHIFT:
            self.nivel.projeteis.extend(self.heroi.usar_especial())

    def atualizar(self, dt):
        if self.pausado:
            return                                   # nada anda: nem o tempo da partida
        self.aviso_nivel = max(0, self.aviso_nivel - dt)
        self.nivel.atualizar(dt)
        self.camera.seguir(self.heroi.posicao)

    def desenhar(self, superficie):
        self.nivel.desenhar(superficie, self.camera)
        if self.pausado:
            self.desenhar_pausa(superficie)
        elif self.aviso_nivel > 0:
            desenhar_texto(superficie, self.nivel.nome, (LARGURA_TELA // 2, ALTURA_TELA // 2), YELLOW, 24,
                           centralizado=True)

    def desenhar_pausa(self, superficie):
        """Escurece o jogo e escreve PAUSADO no meio."""
        sombra = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)   # superfície com transparência
        sombra.fill((0, 0, 0, 160))                  # preto com 160 de 255 de opacidade
        superficie.blit(sombra, (0, 0))
        meio = (LARGURA_TELA // 2, ALTURA_TELA // 2)
        desenhar_texto(superficie, "PAUSADO", meio, WHITE, 24, centralizado=True)
        desenhar_texto(superficie, "ESC continua", (meio[0], meio[1] + 16), WHITE, 14, centralizado=True)
