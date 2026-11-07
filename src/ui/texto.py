"""Ajudantes de texto: fontes reaproveitadas e uma função para escrever na tela.

Usado por todas as telas e pelas peças de ui/ (caixa de texto, HUD, ranking).
"""
import pygame

from settings import WHITE

_fontes: dict[int, pygame.font.Font] = {}


def fonte(tamanho: int) -> pygame.font.Font:
    if tamanho not in _fontes:
        _fontes[tamanho] = pygame.font.Font(None, tamanho)   # None = a fonte padrão do pygame
    return _fontes[tamanho]


def desenhar_texto(superficie: pygame.Surface, texto: str, posicao: tuple[int, int],
                   cor: tuple[int, int, int] = WHITE, tamanho: int = 16,
                   centralizado: bool = False) -> pygame.Rect:
    imagem = fonte(tamanho).render(texto, False, cor)
    retangulo = imagem.get_rect()
    if centralizado:
        retangulo.center = posicao
    else:
        retangulo.topleft = posicao
    superficie.blit(imagem, retangulo)
    return retangulo
