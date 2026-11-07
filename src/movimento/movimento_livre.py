"""Classe MovimentoLivre: top-down contínuo, em qualquer direção.

O que é:
    O movimento padrão. Anda intencao * velocidade * dt pixels por tick.
    Move primeiro no eixo x e depois no y, cada um conferindo
    mapa.area_livre(caixa). Assim, encostado numa parede, o personagem
    desliza ao longo dela em vez de travar.

Métodos:
    - atualizar(corpo: Corpo, mapa: Mapa, dt: float) -> None.

Quem usa: personagens com "movimento": "livre" (pelo registro).
"""
from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from movimento.movimento import Corpo, caixa_em



if TYPE_CHECKING:
    from mapa.mapa import Mapa

class MovimentoLivre:
    def atualizar(self, corpo: Corpo, mapa: Mapa, dt: float) -> None:
        deslocamento = corpo.intencao * corpo.velocidade * dt

        nova = corpo.posicao.copy() # Tenta mover no eixo x
        nova.x += deslocamento.x
        if mapa.area_livre(caixa_em(nova, corpo.tamanho)):
            corpo.posicao.x = nova.x

        nova = corpo.posicao.copy() # Tenta mover no eixo y
        nova.y += deslocamento.y
        if mapa.area_livre(caixa_em(nova, corpo.tamanho)):
            corpo.posicao.y = nova.y

        corpo.intencao = pygame.Vector2(0, 0) # Zera a intenção para o próximo tick