"""Interfaces Corpo e Movimento (typing.Protocol): o jeito de andar.

O que é:
    O jeito como um personagem anda (livre, de tile em tile, com física,
    voando) fica numa estratégia separada. O Personagem guarda um
    Movimento, e dá para trocar sem reescrever o personagem: basta
    entregar outro, por exemplo um MovimentoGrade de 16 pixels.

    O Movimento não conhece o Personagem inteiro, só o Corpo (o pedaço de
    que precisa), e não conhece o formato do mapa: só pergunta ao Mapa se
    uma área está livre.

Corpo (interface):
    - posicao: pygame.Vector2. Centro, em pixels do mapa.
    - tamanho: pygame.Vector2.
    - velocidade: float. Pixels por segundo.
    - intencao: pygame.Vector2. O que mover() pediu neste tick, com
      tamanho de 0 a 1 (meio analógico = meia velocidade).

Movimento (interface):
    - atualizar(corpo: Corpo, mapa: Mapa, dt: float) -> None: move o corpo
      de acordo com a intenção, sem atravessar o que o mapa diz que é
      sólido, e zera a intenção.

Implementações: MovimentoLivre (padrão) e MovimentoGrade.
Quem usa: Personagem (guarda), Nivel (chama na etapa mover_personagens).
"""
from __future__ import annotations
import math
from typing import TYPE_CHECKING, Protocol
import pygame



if TYPE_CHECKING:
    from mapa.mapa import Mapa

class Corpo(Protocol):
    posicao: pygame.Vector2
    tamanho: pygame.Vector2
    velocidade: float
    intencao: pygame.Vector2

class Movimento(Protocol):
    def atualizar(self, corpo: Corpo, mapa: Mapa, dt: float) -> None:
        ...

# Fora da classe Movimento
def pixel(valor: float) -> int:
    # Arredonda o .5 sempre para cima. O round() do Python arredonda o .5
    # para o número par (round(22.5) = 22, round(23.5) = 24), o que fazia a
    # caixa cair 1 px para lados diferentes conforme a posição.
    return math.floor(valor + 0.5)

def caixa_em(posicao: pygame.Vector2, tamanho: pygame.Vector2) -> pygame.Rect:
    caixa = pygame.Rect(0, 0, int(tamanho.x), int(tamanho.y))
    caixa.center = (pixel(posicao.x), pixel(posicao.y))
    return caixa
