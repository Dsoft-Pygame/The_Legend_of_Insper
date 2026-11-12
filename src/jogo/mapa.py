import os

import pygame

from settings import PASTA_MAPAS, TAMANHO_TILE


class Mapa:
    """Lê o .txt de um nível, onde cada letra é um tile: # parede, . chão, H herói, S saída,
    C chefe e qualquer outra letra é um inimigo (s slime, e esqueleto, m morcego).
    """

    def __init__(self, arquivo):
        self.paredes = []                 # um pygame.Rect por parede
        self.saida = None                 # pygame.Rect do S
        self.inicio_heroi = (0, 0)        # centro do H
        self.inimigos = []                # (letra, x, y) de cada inimigo
        self.chefe = None                 # (x, y) do C, se o nível tiver chefe

        linhas = []
        with open(os.path.join(PASTA_MAPAS, arquivo), encoding="utf-8") as texto:
            for linha in texto:
                if linha.strip() != "":   # pula linhas em branco
                    linhas.append(linha.rstrip())
        self.largura = len(linhas[0]) * TAMANHO_TILE   # em pixels
        self.altura = len(linhas) * TAMANHO_TILE

        for numero_linha, linha in enumerate(linhas):
            for numero_coluna, letra in enumerate(linha):
                tile = pygame.Rect(numero_coluna * TAMANHO_TILE, numero_linha * TAMANHO_TILE,
                                   TAMANHO_TILE, TAMANHO_TILE)
                if letra == "#":
                    self.paredes.append(tile)
                elif letra == "S":
                    self.saida = tile
                elif letra == "H":
                    self.inicio_heroi = tile.center
                elif letra == "C":
                    self.chefe = tile.center
                elif letra != ".":
                    self.inimigos.append((letra, tile.centerx, tile.centery))

    def area_livre(self, retangulo):
        """True se o retângulo está dentro do mapa e não encosta em nenhuma parede."""
        dentro = (retangulo.left >= 0 and retangulo.top >= 0
                  and retangulo.right <= self.largura and retangulo.bottom <= self.altura)
        return dentro and retangulo.collidelist(self.paredes) == -1
