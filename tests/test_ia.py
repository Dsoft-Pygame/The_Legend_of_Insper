import random

import pygame

from controle.comandos import Mover
from controle.controlador_ia import ControladorIA
from personagens.tipos import Lado
from personagens.visao import Avistado, Visao


def avistado(id, lado, x, y, vida=100, vida_maxima=100, chefe=False):
    return Avistado(id=id, lado=lado, posicao=pygame.Vector2(x, y), vida=vida,
                    vida_maxima=vida_maxima, chefe=chefe)


def visao(eu, outros=(), tick=0, pode_atacar=True, pode_especial=True):
    return Visao(tick=tick, dt=0.05, eu=eu, direcao_olhar=pygame.Vector2(1, 0),
                 pode_atacar=pode_atacar, pode_especial=pode_especial,
                 avistados=tuple(outros), mapa=None)


def test_controlador_ia_e_deterministico():
    class Sorteio:
        def decidir(self, visao, gerador):
            return [Mover((gerador.random(), 0.0))]

    v = visao(avistado(7, Lado.MONSTROS, 0, 0), tick=3)
    assert ControladorIA(Sorteio(), semente=10).gerar_comandos(v) == ControladorIA(Sorteio(), semente=10).gerar_comandos(v)
    assert ControladorIA(Sorteio(), semente=10).gerar_comandos(v) != ControladorIA(Sorteio(), semente=11).gerar_comandos(v)
