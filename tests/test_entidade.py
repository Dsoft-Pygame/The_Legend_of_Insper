import pygame
from personagens.entidade import Entidade


def test_caixa_fica_centrada_na_posicao():
    e = Entidade(pygame.Vector2(100, 50), pygame.Vector2(12, 12), "slime")
    assert e.caixa.center == (100, 50)
    assert e.caixa.size == (12, 12)


def test_guardar_posicao_copia_e_nao_compartilha():
    e = Entidade(pygame.Vector2(10, 10), pygame.Vector2(12, 12), "slime")
    e.posicao.x += 4
    e.guardar_posicao()
    e.posicao.x += 4
    assert e.posicao_anterior == pygame.Vector2(14, 10)
    assert e.posicao == pygame.Vector2(18, 10)


def test_colocar_em_muda_as_duas_posicoes():
    e = Entidade(pygame.Vector2(10, 10), pygame.Vector2(12, 12), "slime")
    e.colocar_em(pygame.Vector2(200, 80))
    assert e.posicao == e.posicao_anterior == pygame.Vector2(200, 80)