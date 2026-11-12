import pygame

from settings import ALTURA_TELA, BLACK, GRAY, GREEN, LARGURA_TELA, RED, WHITE, YELLOW
from telas.tela import Tela
from ui import desenhar_texto


class TelaResultado(Tela):
    """Fim da partida: salva no ranking e mostra o resultado, os pontos e a posição."""

    def __init__(self, aplicacao):
        super().__init__(aplicacao)
        self.venceu = aplicacao.venceu
        self.pontos = aplicacao.pontuacao.total
        self.posicao = aplicacao.ranking.adicionar(aplicacao.nome_jogador, aplicacao.heroi.nome,
                                                   self.pontos, self.venceu)

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.aplicacao.trocar_tela("inicial")

    def desenhar(self, superficie):
        superficie.fill(BLACK)
        meio = LARGURA_TELA // 2
        if self.venceu:
            desenhar_texto(superficie, "VITÓRIA!", (meio, 34), GREEN, 28, centralizado=True)
        else:
            desenhar_texto(superficie, "DERROTA", (meio, 34), RED, 28, centralizado=True)
        jogador = f"{self.aplicacao.nome_jogador} ({self.aplicacao.heroi.nome})"
        desenhar_texto(superficie, jogador, (meio, 62), WHITE, 16, centralizado=True)
        desenhar_texto(superficie, f"Pontos: {self.pontos}", (meio, 84), YELLOW, 18, centralizado=True)
        desenhar_texto(superficie, f"Posição no ranking: {self.posicao}º", (meio, 104), WHITE, 14, centralizado=True)
        desenhar_texto(superficie, "ENTER volta", (meio, ALTURA_TELA - 14), GRAY, 14, centralizado=True)
