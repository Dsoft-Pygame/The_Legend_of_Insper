"""Classe TelaResultado (herda de Tela): o fim da partida.

O que aparece:
    - VITÓRIA ou DERROTA.
    - Nome e classe de cada jogador da Sessao.
    - Os pontos da partida (inimigos, níveis, chefe, bônus) e o total.
    - Em que posição ficou no ranking e o ranking ao lado.

O que faz:
    - ao_entrar(): aplica os bônus finais na Pontuacao e salva a partida
      no Ranking. Sempre salva, ganhando ou perdendo. Libera os
      dispositivos dos jogadores.
    - tratar_entrada(entrada: EntradaMenu): CONFIRMAR volta para
      TelaInicial.
    - atualizar(dt): se ninguém apertar nada por alguns segundos, volta
      sozinha (para o próximo visitante da feira).

Usa: jogo/ranking.py, jogo/pontuacao.py, ui/painel_ranking.py,
aplicacao/sessao.py.
"""
import pygame

from entrada.entrada_menu import AcaoMenu, EntradaMenu
from settings import ALTURA_TELA, BLACK, GRAY, LARGURA_TELA, YELLOW
from telas.tela import Tela
from ui.texto import desenhar_texto


class TelaResultado(Tela):
    def tratar_entrada(self, entrada: EntradaMenu) -> None:
        if entrada.tem(AcaoMenu.CONFIRMAR):
            from telas.tela_inicial import TelaInicial  # aqui dentro: evita o import circular
            self.aplicacao.trocar_tela(TelaInicial(self.aplicacao))

    def atualizar(self, dt: float) -> None:
        pass

    def desenhar(self, superficie: pygame.Surface) -> None:
        superficie.fill(BLACK)
        desenhar_texto(superficie, "FIM", (LARGURA_TELA // 2, ALTURA_TELA // 2),
                       YELLOW, 22, centralizado=True)
        desenhar_texto(superficie, "ENTER volta", (LARGURA_TELA // 2, ALTURA_TELA // 2 + 24),
                       GRAY, centralizado=True)
