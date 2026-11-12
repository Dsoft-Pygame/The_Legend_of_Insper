import random

import pygame
import pytest

from controle.comandos import Atacar, Mover
from controle.controlador_ia import ControladorIA
from ia.decisao_perseguir import DecisaoPerseguir
from ia.registro import criar_decisao
from personagens.tipos import Lado
from personagens.visao import Avistado, Visao
from ia.decisao_zigue_zague import DecisaoZigueZague



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


def test_perseguir_vai_na_direcao_do_heroi():
    decisao = DecisaoPerseguir(raio_alerta=80)
    v = visao(avistado(1, Lado.MONSTROS, 0, 0), [avistado(2, Lado.HEROIS, 50, 0)])
    assert decisao.decidir(v, random.Random(1)) == [Mover((1.0, 0.0))]


def test_perseguir_ataca_quando_perto():
    decisao = DecisaoPerseguir(raio_alerta=80, distancia_ataque=30)
    v = visao(avistado(1, Lado.MONSTROS, 0, 0), [avistado(2, Lado.HEROIS, 20, 0)])
    assert Atacar() in decisao.decidir(v, random.Random(1))


def test_perseguir_longe_vaga_igual_com_a_mesma_semente():
    v = visao(avistado(1, Lado.MONSTROS, 0, 0), [avistado(2, Lado.HEROIS, 500, 0)])
    a = DecisaoPerseguir(raio_alerta=80).decidir(v, random.Random(42))
    b = DecisaoPerseguir(raio_alerta=80).decidir(v, random.Random(42))
    assert a == b
    for comando in a:
        assert isinstance(comando, Mover)


def test_registro_de_ia():
    assert isinstance(criar_decisao({"tipo": "perseguir", "raio_alerta": 80}), DecisaoPerseguir)
    with pytest.raises(ValueError):
        criar_decisao({"tipo": "persegir"})


def test_zigue_zague_desvia_para_o_lado():
    decisao = DecisaoZigueZague(raio_alerta=120, periodo=0.4, amplitude=0.8)
    v = visao(avistado(1, Lado.MONSTROS, 0, 0), [avistado(2, Lado.HEROIS, 100, 0)])
    (comando,) = decisao.decidir(v, random.Random(1))
    x, y = comando.direcao
    assert x > 0 and y != 0