import pygame

from settings import ALTURA_TELA, BLACK, GRAY, LARGURA_TELA, YELLOW
from telas.tela import Tela
from ui import desenhar_texto


class TelaResultado(Tela):
    """Fim da partida. Por enquanto só mostra FIM, e o jogo ainda não chega aqui."""

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.aplicacao.trocar_tela("inicial")

    def desenhar(self, superficie):
        superficie.fill(BLACK)
        meio = (LARGURA_TELA // 2, ALTURA_TELA // 2)
        desenhar_texto(superficie, "FIM", meio, YELLOW, 22, centralizado=True)
        desenhar_texto(superficie, "ENTER volta", (meio[0], meio[1] + 24), GRAY, centralizado=True)
