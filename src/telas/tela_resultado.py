import pygame

from settings import BLACK, GRAY, GREEN, LARGURA_TELA, RED, WHITE
from telas.tela import Tela
from ui import desenhar_texto


class TelaResultado(Tela):
    """Fim da partida: VITÓRIA ou DERROTA e os pontos. Enter volta para a tela inicial."""

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.aplicacao.trocar_tela("inicial")

    def desenhar(self, superficie):
        superficie.fill(BLACK)
        meio = LARGURA_TELA // 2
        titulo = "DERROTA"
        cor = RED
        if self.aplicacao.venceu:
            titulo = "VITÓRIA!"
            cor = GREEN
        desenhar_texto(superficie, titulo, (meio, 40), cor, 24, centralizado=True)
        pontos = self.aplicacao.pontuacao.total
        desenhar_texto(superficie, f"Pontos: {pontos}", (meio, 80), WHITE, 18, centralizado=True)
        desenhar_texto(superficie, "ENTER volta", (meio, 120), GRAY, centralizado=True)
