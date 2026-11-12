import pygame

from personagens.herois import Arqueiro, Barbaro, Mago
from settings import ALTURA_TELA, BLACK, DARK_GRAY, GRAY, LARGURA_TELA, WHITE, YELLOW
from telas.tela import Tela
from ui import desenhar_texto


class TelaClasses(Tela):
    """Escolha da classe: um cartão para cada herói, com nome, vida, velocidade e dano."""

    def __init__(self, aplicacao):
        super().__init__(aplicacao)
        self.herois = [Mago(0, 0), Arqueiro(0, 0), Barbaro(0, 0)]   # o Nivel põe o escolhido no lugar
        self.selecionado = 0

    def tratar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key in (pygame.K_LEFT, pygame.K_a):
            self.selecionado = (self.selecionado - 1) % len(self.herois)   # o % dá a volta
        elif evento.key in (pygame.K_RIGHT, pygame.K_d):
            self.selecionado = (self.selecionado + 1) % len(self.herois)
        elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.aplicacao.heroi = self.herois[self.selecionado]
            self.aplicacao.trocar_tela("jogo")
        elif evento.key == pygame.K_ESCAPE:
            self.aplicacao.trocar_tela("inicial")

    def desenhar(self, superficie):
        superficie.fill(BLACK)
        desenhar_texto(superficie, "Escolha sua classe", (LARGURA_TELA // 2, 10), YELLOW, 18, centralizado=True)
        for i, heroi in enumerate(self.herois):
            cartao = pygame.Rect(6 + i * 78, 22, 72, 90)
            self.desenhar_cartao(superficie, heroi, cartao, i == self.selecionado)
        descricao = self.herois[self.selecionado].descricao
        desenhar_texto(superficie, descricao, (LARGURA_TELA // 2, 124), WHITE, 14, centralizado=True)
        desenhar_texto(superficie, "ENTER escolhe   ESC volta", (LARGURA_TELA // 2, ALTURA_TELA - 12), GRAY, 14,
                       centralizado=True)

    def desenhar_cartao(self, superficie, heroi, cartao, selecionado):
        cor = WHITE
        borda = GRAY
        grossura = 1
        if selecionado:
            cor = YELLOW
            borda = YELLOW
            grossura = 2
        pygame.draw.rect(superficie, DARK_GRAY, cartao)
        pygame.draw.rect(superficie, borda, cartao, grossura)
        icone = pygame.Rect(0, 0, 16, 16)
        icone.center = (cartao.centerx, cartao.y + 16)
        pygame.draw.rect(superficie, heroi.cor, icone)
        desenhar_texto(superficie, heroi.nome, (cartao.centerx, cartao.y + 32), cor, 16, centralizado=True)
        desenhar_texto(superficie, f"Vida: {heroi.vida_maxima}", (cartao.x + 6, cartao.y + 46), WHITE, 14)
        desenhar_texto(superficie, f"Vel: {heroi.velocidade}", (cartao.x + 6, cartao.y + 58), WHITE, 14)
        desenhar_texto(superficie, f"Dano: {heroi.dano}", (cartao.x + 6, cartao.y + 70), WHITE, 14)
