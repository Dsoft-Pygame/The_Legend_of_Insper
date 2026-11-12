"""Classe DecisaoZigueZague: vai na direção do herói, desviando de lado.

O que é:
    A IA do Morcego (rápido, pouca vida, voa em zigue-zague). Vai para o
    herói mais próximo, mas soma à direção um desvio para o lado que troca
    de sinal de tempos em tempos.

Parâmetros (vêm do campo "decisao" em data/inimigos.json):
    - raio_alerta: float.
    - periodo: float. Segundos entre uma troca de lado e outra.
    - amplitude: float. Quanto desvia (0 = reto, 1 = 45 graus).

Memória:
    - lado_atual: int. +1 ou -1.
    - tempo_restante: float.

Métodos:
    - decidir(visao: Visao, gerador: random.Random) -> list[Comando].
      Sem herói à vista, vaga como a DecisaoPerseguir.

Quem usa: ControladorIA (pelo nome "zigue_zague" no registro).
Usa: personagens/visao.py, controle/comandos.py.
"""

import random
import pygame
from controle.comandos import Comando, Mover
from ia.decisao_perseguir import DecisaoPerseguir
from personagens.visao import Visao



class DecisaoZigueZague:
    def __init__(
        self,
        raio_alerta: float,
        periodo: float = 0.4,
        amplitude: float = 0.8
    ) -> None:
        self.raio_alerta = raio_alerta
        self.periodo = periodo
        self.amplitude = amplitude

        self.lado_atual = 1
        self.tempo_restante = periodo
        self.vagando = DecisaoPerseguir(
            raio_alerta=0,
            tempo_vagando=1.0
        )

    def decidir(self, visao: Visao, gerador: random.Random) -> list[Comando]:
        alvo = visao.mais_proximo(visao.eu.lado.oposto())

        # Sem alvo próximo, anda sem perseguir
        if alvo is None or (
            alvo.posicao.distance_to(visao.eu.posicao) > self.raio_alerta
        ):
            return self.vagando.vagar(visao, gerador)

        caminho = alvo.posicao - visao.eu.posicao
        if caminho.length() == 0:
            return []

        # Troca o lado do desvio a cada período
        self.tempo_restante -= visao.dt
        if self.tempo_restante <= 0:
            self.lado_atual *= -1
            self.tempo_restante = self.periodo

        frente = caminho.normalize()
        lado = (
            pygame.Vector2(-frente.y, frente.x)
            * self.lado_atual
            * self.amplitude
        )

        direcao = (frente + lado).normalize()
        return [Mover((direcao.x, direcao.y))]