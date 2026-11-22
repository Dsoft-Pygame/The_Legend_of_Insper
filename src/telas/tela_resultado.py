"""Tela do fim da partida: resultado, pontos e ranking."""

import pygame

from settings import BLACK, GRAY, GREEN, RED, WHITE, YELLOW
from telas.tela import Tela
from ui import desenhar_ranking, desenhar_texto

TEMPO_VOLTAR_SOZINHA = 20   # segundos parada até voltar sozinha para o início (para o próximo jogador)


class TelaResultado(Tela):
    """Fim da partida: vitória ou derrota, o extrato dos pontos e o ranking com a partida em destaque.

    Ganhando ou perdendo, a partida é salva no ranking assim que a tela abre.
    """

    def __init__(self, aplicacao):
        """Toca a música do resultado e salva a partida no ranking, guardando a posição dela."""
        super().__init__(aplicacao)
        aplicacao.som.tocar_musica("resultado")
        self.tempo_parada = 0
        pontos = aplicacao.pontuacao.total
        self.posicao = aplicacao.ranking.adicionar(aplicacao.nome_jogador, aplicacao.heroi.nome, pontos,
                                                   aplicacao.venceu)

    def tratar_evento(self, evento):
        """Enter volta para a tela inicial."""
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.aplicacao.trocar_tela("inicial")

    def atualizar(self, dt):
        """Volta sozinha para a tela inicial depois de TEMPO_VOLTAR_SOZINHA segundos parada."""
        self.tempo_parada += dt
        if self.tempo_parada >= TEMPO_VOLTAR_SOZINHA:
            self.aplicacao.trocar_tela("inicial")

    def desenhar(self, superficie):
        """Desenha vitória ou derrota, o extrato dos pontos, a posição e o ranking com a partida em
        destaque.
        """
        superficie.fill(BLACK)
        pontuacao = self.aplicacao.pontuacao
        titulo = "DERROTA"
        cor = RED
        if self.aplicacao.venceu:
            titulo = "VITÓRIA!"
            cor = GREEN
        desenhar_texto(superficie, titulo, (144, 24), cor, 48, centralizado=True)

        nome = f"{self.aplicacao.nome_jogador} ({self.aplicacao.heroi.nome})"
        desenhar_texto(superficie, nome, (12, 56), WHITE, 24)
        y = 80
        texto = f"Inimigos: {pontuacao.inimigos_derrotados} +{pontuacao.pontos_inimigos}"
        desenhar_texto(superficie, texto, (12, y), WHITE, 24)
        for linha in pontuacao.extrato:          # "Térreo concluído +500", os bônus...
            y += 20
            desenhar_texto(superficie, linha, (12, y), WHITE, 24)
        desenhar_texto(superficie, f"TOTAL: {pontuacao.total}", (12, y + 28), YELLOW, 36)

        desenhar_texto(superficie, f"Sua posição: {self.posicao}", (12, 268), YELLOW, 28)
        desenhar_texto(superficie, "ENTER volta", (12, 292), GRAY, 28)

        destaque = None
        if self.posicao <= 10:
            destaque = self.posicao - 1          # a linha desta partida, se ela está entre as 10
        quadro = pygame.Rect(276, 16, 192, 288)
        desenhar_ranking(superficie, quadro, self.aplicacao.ranking.melhores(10), destaque)
