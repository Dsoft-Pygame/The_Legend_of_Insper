import pygame

from controle.controlador_ia import ControladorIA
from jogo.catalogo import Catalogo
from jogo.fabrica import Fabrica
from personagens.tipos import Lado


def test_fabrica_monta_heroi_e_monstro():
    fabrica = Fabrica(Catalogo.carregar(), semente=1)
    mago = fabrica.criar_heroi("mago", pygame.Vector2(10, 20))
    assert mago.lado == Lado.HEROIS and mago.vida == 60 and mago.posicao == pygame.Vector2(10, 20)
    assert mago.pode_atacar() and mago.pode_especial()
    slime, controlador = fabrica.criar_monstro("slime", pygame.Vector2(50, 50))
    assert slime.lado == Lado.MONSTROS and slime.pontos == 50 and slime.dano_contato == 10
    assert isinstance(controlador, ControladorIA)
    dragao, _ = fabrica.criar_monstro("dragao", pygame.Vector2(50, 50))
    assert dragao.chefe and dragao.tamanho.x > slime.tamanho.x