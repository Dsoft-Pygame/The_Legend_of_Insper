"""Classes Avistado e Visao: o que um personagem enxerga num tick.

O que é:
    O equivalente da VisaoAnimal da simulação lobo-coelho. O Nivel monta
    uma Visao para cada personagem a cada tick (Nivel.observar) e entrega
    ao controlador. A IA decide olhando SÓ para isso: nunca recebe o
    Personagem, o Nivel ou o Mundo, então não consegue alterar nada.

Avistado (dataclass congelada):
    - id: EntidadeId.
    - lado: Lado.
    - posicao: pygame.Vector2 (cópia).
    - vida, vida_maxima: int.
    - chefe: bool.

Visao (dataclass congelada):
    - tick: int. Número do tick (entra na semente da IA).
    - dt: float. Duração do tick, em segundos.
    - eu: Avistado. O próprio personagem.
    - direcao_olhar: pygame.Vector2.
    - pode_atacar, pode_especial: bool. Sem recarga agora.
    - avistados: tuple[Avistado, ...]. Os outros personagens dentro do
      raio de visão.
    - mapa: Mapa. Para perguntar se uma área está livre (a interface Mapa
      só tem perguntas, nada que altere o mapa).

Métodos:
    - mais_proximo(lado: Lado) -> Avistado | None.
    - do_lado(lado: Lado) -> list[Avistado].

Quem cria: Nivel.observar.
Quem usa: Controlador e ia/.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame

from personagens.tipos import EntidadeId, Lado

if TYPE_CHECKING:
    from mapa.mapa import Mapa


@dataclass(frozen=True)
class Avistado:
    id: EntidadeId
    lado: Lado
    posicao: pygame.Vector2
    vida: int
    vida_maxima: int
    chefe: bool


@dataclass(frozen=True)
class Visao:
    tick: int
    dt: float
    eu: Avistado
    direcao_olhar: pygame.Vector2
    pode_atacar: bool
    pode_especial: bool
    avistados: tuple[Avistado, ...]
    mapa: Mapa

    def do_lado(self, lado: Lado) -> list[Avistado]:
        return [a for a in self.avistados if a.lado == lado]

    def mais_proximo(self, lado: Lado) -> Avistado | None:
        candidatos = self.do_lado(lado)
        if not candidatos:
            return None
        return min(candidatos, key=lambda a: a.posicao.distance_to(self.eu.posicao))
