import pygame

from personagens.projetil import Projetil
from personagens.tipos import Lado


def test_projetil_anda_e_acaba():
    p = Projetil(Lado.HEROIS, 1, pygame.Vector2(0, 0), pygame.Vector2(4, 4), "flecha",
                 pygame.Vector2(100, 0), dano=10, duracao=0.1)
    p.avancar(0.05)
    assert p.posicao == pygame.Vector2(5, 0) and not p.acabou()
    p.avancar(0.05)
    assert p.acabou()