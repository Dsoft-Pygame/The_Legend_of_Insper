"""Tela de controles: mostra as teclas do jogo depois de escolher a classe, antes da partida começar."""

import pygame

from settings import ALTURA_TELA, BLACK, GRAY, LARGURA_TELA, WHITE, YELLOW
from telas.tela import Tela
from ui import desenhar_texto

CONTROLES = [
    ("W A S D", "andar"),
    ("ESPAÇO", "atacar"),
    ("SHIFT", "especial"),
    ("ESC", "pausar"),
    ("F11", "tela cheia"),
]


class TelaControles(Tela):
    """Aparece logo depois de escolher a classe: mostra as teclas para quem nunca jogou."""

    def __init__(self, aplicacao):
        """Guarda o herói escolhido na TelaClasses e zera o tempo usado para piscar o aviso."""
        super().__init__(aplicacao)
        self.heroi = aplicacao.heroi          # o herói escolhido na TelaClasses
        self.tempo = 0                        # para o "ENTER começa" piscar

    def tratar_evento(self, evento):
        """Enter (ou Espaço) começa a partida; Esc volta para a escolha de classe."""
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self.aplicacao.som.tocar("menu_confirmar")
            self.aplicacao.trocar_tela("jogo")
        elif evento.key == pygame.K_ESCAPE:
            self.aplicacao.trocar_tela("classes")   # volta para trocar de classe

    def atualizar(self, dt):
        """Só conta o tempo, para o "ENTER começa" piscar."""
        self.tempo += dt

    def desenhar(self, superficie):
        """Desenha o título, a classe escolhida, a lista de teclas e o aviso piscando no rodapé."""
        superficie.fill(BLACK)
        meio = LARGURA_TELA // 2
        desenhar_texto(superficie, "Controles", (meio, 24), YELLOW, 40, centralizado=True)
        desenhar_texto(superficie, "Você é o " + self.heroi.nome, (meio, 56), WHITE, 28, centralizado=True)
        for i, (tecla, acao) in enumerate(CONTROLES):
            y = 90 + i * 32
            desenhar_texto(superficie, tecla, (170, y), YELLOW, 32, centralizado=True)
            desenhar_texto(superficie, acao, (250, y - 10), WHITE, 28)
        if int(self.tempo * 2) % 2 == 0:              # pisca: aparece meio segundo, some meio segundo
            desenhar_texto(superficie, "ENTER começa   ESC volta", (meio, ALTURA_TELA - 24), GRAY, 28,
                           centralizado=True)