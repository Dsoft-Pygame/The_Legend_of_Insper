"""Peças de interface usadas pelas telas: texto, caixa do nome e quadro do ranking."""
import pygame

from settings import DARK_GRAY, GRAY, WHITE, YELLOW

fontes = {}   # uma fonte por tamanho, criada uma vez só


def fonte(tamanho):
    if tamanho not in fontes:
        fontes[tamanho] = pygame.font.Font(None, tamanho)   # None = a fonte padrão do pygame
    return fontes[tamanho]


def desenhar_texto(superficie, texto, posicao, cor=WHITE, tamanho=16, centralizado=False):
    """Escreve o texto na tela e devolve o retângulo que ele ocupou."""
    imagem = fonte(tamanho).render(texto, False, cor)
    retangulo = imagem.get_rect()
    if centralizado:
        retangulo.center = posicao
    else:
        retangulo.topleft = posicao
    superficie.blit(imagem, retangulo)
    return retangulo


def desenhar_ranking(superficie, retangulo, partidas):
    """Quadro com as melhores partidas: posição, nome e pontos."""
    pygame.draw.rect(superficie, DARK_GRAY, retangulo)
    pygame.draw.rect(superficie, GRAY, retangulo, 1)
    desenhar_texto(superficie, "Ranking", (retangulo.centerx, retangulo.y + 9), YELLOW, 16, centralizado=True)
    if len(partidas) == 0:
        desenhar_texto(superficie, "Ninguém jogou", (retangulo.centerx, retangulo.y + 34), GRAY, 14,
                       centralizado=True)
        desenhar_texto(superficie, "ainda", (retangulo.centerx, retangulo.y + 46), GRAY, 14, centralizado=True)
    for i, partida in enumerate(partidas):
        y = retangulo.y + 20 + i * 12
        desenhar_texto(superficie, f"{i + 1}. {partida['nome'][:9]}", (retangulo.x + 4, y), WHITE, 14)
        pontos = str(partida["pontos"])
        largura = fonte(14).size(pontos)[0]
        desenhar_texto(superficie, pontos, (retangulo.right - 4 - largura, y), YELLOW, 14)


class CaixaTexto:
    """Campo onde o jogador digita o nome, com um cursor piscando no fim."""

    def __init__(self, retangulo, tamanho_maximo=12):
        self.retangulo = retangulo
        self.tamanho_maximo = tamanho_maximo
        self.texto = ""

    def digitar(self, letras):
        """Acrescenta as letras digitadas: só letras, números, espaço, - e _."""
        for letra in letras:
            if len(self.texto) < self.tamanho_maximo and (letra.isalnum() or letra in " -_"):
                self.texto += letra

    def apagar(self):
        self.texto = self.texto[:-1]

    def desenhar(self, superficie, cursor_visivel):
        pygame.draw.rect(superficie, DARK_GRAY, self.retangulo)
        pygame.draw.rect(superficie, WHITE, self.retangulo, 1)
        area = desenhar_texto(superficie, self.texto, (self.retangulo.x + 3, self.retangulo.y + 3))
        if cursor_visivel:
            x = self.retangulo.x + 3
            if self.texto != "":
                x = area.right + 1
            pygame.draw.line(superficie, YELLOW, (x, self.retangulo.y + 3), (x, self.retangulo.bottom - 4))
