"""Classe CarregadorTexto (implementa CarregadorMapa): mapa escrito à mão.

O que é:
    Lê um arquivo de texto de data/mapas/ em que cada caractere é um tile
    e devolve um MapaTiles:
        #  parede
        .  chão
        H  onde os heróis aparecem (o P1 no primeiro H, o P2 no segundo,
           ou ao lado do primeiro se só houver um)
        I  onde um inimigo pode aparecer
        C  onde o chefe aparece
        S  saída
    Os marcadores H, I e C viram chão depois de lidos.

Métodos:
    - carregar(origem: str) -> Mapa: lê data/<origem>. Linhas de tamanhos
      diferentes ou caractere desconhecido geram erro com o número da linha.

Trocar por mapas do Tiled depois = um CarregadorTiled novo, sem mudar o
resto do jogo.

Quem usa: Mundo (pelo registro de mapas).
"""
from pathlib import Path

import pygame

from mapa.mapa_tiles import MapaTiles
from settings import PASTA_DATA, TAMANHO_TILE

CELULAS = {"#": "parede", ".": "chao", "S": "saida", "H": "chao", "I": "chao", "C": "chao"}
MARCADORES = {"H": "heroi", "I": "inimigo", "C": "chefe"}


class CarregadorTexto:
    def __init__(self, pasta_dados: Path = PASTA_DATA) -> None:
        self.pasta_dados = pasta_dados

    def carregar(self, origem: str) -> MapaTiles:
        texto = (self.pasta_dados / origem).read_text(encoding="utf-8")
        linhas = [linha.rstrip() for linha in texto.splitlines()]
        linhas = [linha for linha in linhas if linha]
        largura = len(linhas[0])
        celulas: list[list[str]] = []
        pontos: dict[str, list[pygame.Vector2]] = {"heroi": [], "inimigo": [], "chefe": []}
        for numero_linha, linha in enumerate(linhas):
            if len(linha) != largura:
                raise ValueError(f"{origem}: linha {numero_linha + 1} tem {len(linha)} caracteres, "
                                 f"mas a primeira tem {largura}")
            fileira: list[str] = []
            for coluna, caractere in enumerate(linha):
                if caractere not in CELULAS:
                    raise ValueError(f"{origem}: linha {numero_linha + 1}, coluna {coluna + 1}: "
                                     f"caractere '{caractere}' desconhecido")
                fileira.append(CELULAS[caractere])
                if caractere in MARCADORES:
                    centro = pygame.Vector2(coluna * TAMANHO_TILE + TAMANHO_TILE // 2,
                                            numero_linha * TAMANHO_TILE + TAMANHO_TILE // 2)
                    pontos[MARCADORES[caractere]].append(centro)
            celulas.append(fileira)
        return MapaTiles(celulas, pontos, TAMANHO_TILE)
