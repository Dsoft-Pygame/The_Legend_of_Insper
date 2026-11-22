"""O mapa de um andar, lido de um arquivo .txt em src/data/mapas/."""

import os
from collections import deque

import pygame

from settings import PASTA_MAPAS, TAMANHO_TILE


class Mapa:
    """Lê o .txt de um nível, onde cada letra é um tile: # parede, . chão, H herói, S saída,
    C chefe e qualquer outra letra é um inimigo (s slime, e esqueleto, m morcego).
    """

    def __init__(self, arquivo):
        """Lê o arquivo linha por linha e guarda as paredes, a saída, onde o herói começa, os inimigos e o
        chefe.
        """
        self.paredes = []                 # um pygame.Rect por parede
        self.saida = None                 # pygame.Rect do S
        self.inicio_heroi = (0, 0)        # centro do H
        self.inimigos = []                # (letra, x, y) de cada inimigo
        self.chefe = None                 # (x, y) do C, se o nível tiver chefe
        self.pontos_livres = {}           # tamanho -> pontos da grade onde cabe um corpo desse tamanho

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

    def linha_livre(self, inicio, fim):
        """True se dá para ir em linha reta de inicio até fim sem passar por parede
        (confere um ponto a cada 4 pixels do caminho).
        """
        caminho = pygame.Vector2(fim) - pygame.Vector2(inicio)
        passos = int(caminho.length() // 4) + 1
        for i in range(passos + 1):
            ponto = pygame.Vector2(inicio) + caminho * (i / passos)
            if not self.area_livre(pygame.Rect(round(ponto.x), round(ponto.y), 1, 1)):
                return False
        return True

    def livres(self, tamanho):
        """Os pontos de uma grade de 16 em 16 pixels onde cabe um corpo quadrado desse tamanho.
        Calcula uma vez por tamanho e guarda.
        """
        if tamanho not in self.pontos_livres:
            pontos = set()
            for x in range(0, self.largura, 16):
                for y in range(0, self.altura, 16):
                    corpo = pygame.Rect(0, 0, tamanho, tamanho)
                    corpo.center = (x, y)
                    if self.area_livre(corpo):
                        pontos.add((x, y))
            self.pontos_livres[tamanho] = pontos
        return self.pontos_livres[tamanho]

    def proximo_passo(self, origem, destino, tamanho):
        """Para onde um corpo desse tamanho deve andar para chegar perto de destino contornando
        as paredes. Faz uma busca em largura pela grade de 16 px e devolve o primeiro ponto do
        caminho até o ponto alcançável mais perto do destino (ou None se já está nele).
        """
        livres = self.livres(tamanho)
        inicio = (round(origem.x / 16) * 16, round(origem.y / 16) * 16)
        if inicio not in livres:                 # entre dois pontos: começa do livre mais perto
            vizinhos = [p for p in livres if abs(p[0] - inicio[0]) <= 16 and abs(p[1] - inicio[1]) <= 16]
            if len(vizinhos) == 0:
                return None
            inicio = min(vizinhos, key=lambda p: (p[0] - origem.x) ** 2 + (p[1] - origem.y) ** 2)
        veio_de = {inicio: None}
        fila = deque([inicio])
        melhor = inicio
        while len(fila) > 0:
            ponto = fila.popleft()
            if (ponto[0] - destino.x) ** 2 + (ponto[1] - destino.y) ** 2 < (melhor[0] - destino.x) ** 2 + (melhor[1] - destino.y) ** 2:
                melhor = ponto
            for dx, dy in ((16, 0), (-16, 0), (0, 16), (0, -16)):
                vizinho = (ponto[0] + dx, ponto[1] + dy)
                if vizinho in livres and vizinho not in veio_de:
                    veio_de[vizinho] = ponto
                    fila.append(vizinho)
        if melhor == inicio:
            return None
        passo = melhor
        while veio_de[passo] != inicio:          # volta pelo caminho até o primeiro passo
            passo = veio_de[passo]
        return pygame.Vector2(passo)
