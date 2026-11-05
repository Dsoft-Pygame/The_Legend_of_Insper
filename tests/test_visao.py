import pygame

from personagens.tipos import Lado
from personagens.visao import Avistado, Visao


def avistado(id, lado, x, y):
    return Avistado(id=id, lado=lado, posicao=pygame.Vector2(x, y), vida=10, vida_maxima=10, chefe=False)


def test_mais_proximo_e_do_lado():
    eu = avistado(1, Lado.MONSTROS, 0, 0)
    outros = (avistado(2, Lado.HEROIS, 50, 0), avistado(3, Lado.HEROIS, 20, 0), avistado(4, Lado.MONSTROS, 5, 0))
    visao = Visao(tick=0, dt=0.05, eu=eu, direcao_olhar=pygame.Vector2(1, 0), pode_atacar=True,
                  pode_especial=False, avistados=outros, mapa=None)
    assert visao.mais_proximo(Lado.HEROIS).id == 3
    assert [a.id for a in visao.do_lado(Lado.MONSTROS)] == [4]


def test_ninguem_a_vista():
    eu = avistado(1, Lado.MONSTROS, 0, 0)
    visao = Visao(tick=0, dt=0.05, eu=eu, direcao_olhar=pygame.Vector2(1, 0), pode_atacar=True,
                  pode_especial=False, avistados=(), mapa=None)
    assert visao.mais_proximo(Lado.HEROIS) is None
