import pygame

from settings import ALTURA_TELA, BLACK, GRAY, LARGURA_TELA, RED, WHITE, YELLOW
from telas.tela import Tela
from ui import CaixaTexto, desenhar_ranking, desenhar_texto


class TelaInicial(Tela):
    """Primeira tela: o jogador digita o nome e vê o ranking ao lado."""

    def __init__(self, aplicacao):
        super().__init__(aplicacao)
        self.caixa_nome = CaixaTexto(pygame.Rect(10, 52, 104, 16))
        self.tempo = 0                    # para o cursor piscar
        self.aviso = 0                    # segundos mostrando "Digite seu nome"

    def tratar_evento(self, evento):
        if evento.type == pygame.TEXTINPUT:
            self.caixa_nome.digitar(evento.text)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                self.caixa_nome.apagar()
            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                nome = self.caixa_nome.texto.strip()
                if nome == "":
                    self.aviso = 2
                else:
                    self.aplicacao.nome_jogador = nome
                    self.aplicacao.trocar_tela("classes")

    def atualizar(self, dt):
        self.tempo += dt
        self.aviso = max(0, self.aviso - dt)

    def desenhar(self, superficie):
        superficie.fill(BLACK)
        desenhar_texto(superficie, "The Legend of Insper", (LARGURA_TELA // 2, 16), YELLOW, 22, centralizado=True)
        desenhar_texto(superficie, "Seu nome:", (10, 40), WHITE, 14)
        cursor_visivel = int(self.tempo * 2) % 2 == 0
        self.caixa_nome.desenhar(superficie, cursor_visivel)
        if self.aviso > 0:
            desenhar_texto(superficie, "Digite seu nome", (10, 74), RED, 14)
        desenhar_ranking(superficie, pygame.Rect(124, 34, 108, 84), self.aplicacao.ranking.melhores(5))
        desenhar_texto(superficie, "ENTER para jogar", (LARGURA_TELA // 2, ALTURA_TELA - 14), GRAY, 14,
                       centralizado=True)
