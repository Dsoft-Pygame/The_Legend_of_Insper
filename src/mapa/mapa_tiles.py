"""Classe MapaTiles (implementa Mapa): uma grade de tiles 16x16.

O que é:
    O mapa "como nos Pokémon antigos": maior que a tela, feito de
    quadradinhos. Cada célula é chão, parede ou saída. É a única classe do
    jogo que sabe que existe uma grade (como o Tabuleiro da simulação).

Atributos:
    - tamanho_tile: int. 16 pixels.
    - celulas: list[list[str]]. Tipo de cada célula ("chao", "parede",
      "saida").
    - pontos: dict[str, list[pygame.Vector2]]. Surgimentos por marcador.
    - largura, altura: int. Em pixels (colunas e linhas vezes o tile).

Métodos (os da interface Mapa):
    - area_livre(caixa: pygame.Rect) -> bool: confere só as células que a
      caixa toca.
    - surgimentos(marcador: str) -> list[pygame.Vector2].
    - saida() -> pygame.Rect | None.
    - ladrilhos_em(area: pygame.Rect) -> Iterator[tuple[pygame.Rect, str]]:
      só as células dentro da área (a câmera), para não desenhar o mapa
      todo a cada quadro.
    - celula_em(posicao: pygame.Vector2) -> str: ajuda interna.

Quem cria: CarregadorTexto.
"""
from typing import Iterator

import pygame

from settings import TAMANHO_TILE


class MapaTiles:
    def __init__(self, celulas: list[list[str]], pontos: dict[str, list[pygame.Vector2]], 
    tamanho_tile: int = TAMANHO_TILE) -> None:
        self.tamanho_tile = tamanho_tile
        self.celulas = celulas
        self.pontos = pontos
        self.colunas = len(celulas[0])
        self.linhas = len(celulas)
        self.largura = self.colunas * tamanho_tile
        self.altura = self.linhas * tamanho_tile

    def celula_em(self, posicao: pygame.Vector2) -> str:
        coluna = int(posicao.x // self.tamanho_tile)
        linha = int(posicao.y // self.tamanho_tile)
        if 0 <= coluna < self.colunas and 0 <= linha < self.linhas:
            return self.celulas[linha][coluna]
        return "parede"

    def area_livre(self, caixa: pygame.Rect) -> bool:
        if caixa.left < 0 or caixa.top < 0 or caixa.right > self.largura or caixa.bottom > self.altura:
            return False
        t = self.tamanho_tile
        for linha in range(caixa.top // t, (caixa.bottom - 1) // t + 1):
            for coluna in range(caixa.left // t, (caixa.right - 1) // t + 1):
                if self.celulas[linha][coluna] == "parede":
                    return False
        return True

    def surgimentos(self, marcador: str) -> list[pygame.Vector2]:
        return [pygame.Vector2(p) for p in self.pontos.get(marcador, [])]

    def saida(self) -> pygame.Rect | None:
        t = self.tamanho_tile
        for linha, fileira in enumerate(self.celulas):
            for coluna, celula in enumerate(fileira):
                if celula == "saida":
                    return pygame.Rect(coluna * t, linha * t, t, t)
        return None

    def ladrilhos_em(self, area: pygame.Rect) -> Iterator[tuple[pygame.Rect, str]]:
        t = self.tamanho_tile
        coluna_inicio = max(0, area.left // t)
        coluna_fim = min(self.colunas - 1, (area.right - 1) // t)
        linha_inicio = max(0, area.top // t)
        linha_fim = min(self.linhas - 1, (area.bottom - 1) // t)
        for linha in range(linha_inicio, linha_fim + 1):
            for coluna in range(coluna_inicio, coluna_fim + 1):
                yield pygame.Rect(coluna * t, linha * t, t, t), self.celulas[linha][coluna]