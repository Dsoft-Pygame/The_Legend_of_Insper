"""Classe AtaqueGolpe: golpe corpo a corpo numa área.

O que é:
    Cria um Projetil parado (velocidade zero) que dura uma fração de
    segundo:
        - golpe de machado do bárbaro: forma "frente", uma área pequena na
          frente de quem atacou;
        - giro do bárbaro: forma "volta", uma área em volta dele que
          atravessa (acerta todo mundo dentro).

Parâmetros (vêm de data/classes.json ou data/inimigos.json):
    - recarga: float.
    - dano: int.
    - alcance: int. Tamanho da área, em pixels.
    - forma: str. "frente" ou "volta".
    - duracao: float.
    - aparencia: str.

Métodos:
    - executar(atacante: Personagem) -> list[Projetil].

Quem usa: Fabrica (pelo tipo "golpe" no registro).
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from personagens.projetil import Projetil
if TYPE_CHECKING:
    from personagens.personagem import Personagem



class AtaqueGolpe:
    def __init__(self, recarga: float, dano: int, alcance: int, forma: str = "frente",
             duracao: float = 0.1, aparencia: str = "golpe") -> None:
        self.recarga = recarga
        self.dano = dano
        self.alcance = alcance
        self.forma = forma
        self.duracao = duracao
        self.aparencia = aparencia

    def executar(self, atacante: Personagem) -> list[Projetil]:
        if self.forma == 'frente':
            direcao =  pygame.Vector2(atacante.direcao_olhar)
            if direcao.length == 0:
                direcao = pygame.Vector2(1,0)
            direcao = direcao.normalize()

            centro = atacante.posicao + direcao * (atacante.tamanho.x / 2 + self.alcance / 2) # da onde o ataque vai sair
            tamanho = pygame.Vector2(self.alcance, self.alcance)
            atravessa = False

        else: # Cria uma área de ataque em volta do personagem
            centro = pygame.Vector2(atacante.posicao)
            tamanho = atacante.tamanho + pygame.Vector2(self.alcance * 2, self.alcance * 2)
            atravessa = True

        return [
            Projetil(lado=atacante.lado, dono=atacante.id, posicao=centro, tamanho=tamanho, aparencia=self.aparencia, velocidade=pygame.Vector2(0, 0), dano=self.dano, duracao=self.duracao, atravessa=atravessa
            )
        ]