import pygame

from mapa.mapa_tiles import MapaTiles


def criar_mapa():
    # 4 colunas x 3 linhas:  # . . S
    #                        # . . .
    #                        # # # #
    celulas = [
        ["parede", "chao", "chao", "saida"],
        ["parede", "chao", "chao", "chao"],
        ["parede", "parede", "parede", "parede"],
    ]
    pontos = {"heroi": [pygame.Vector2(24, 8)], "inimigo": [], "chefe": []}
    return MapaTiles(celulas, pontos, 16)


def test_tamanho_em_pixels():
    mapa = criar_mapa()
    assert mapa.largura == 64
    assert mapa.altura == 48


def test_area_livre():
    mapa = criar_mapa()
    assert mapa.area_livre(pygame.Rect(18, 2, 12, 12))       # todo no chão
    assert not mapa.area_livre(pygame.Rect(10, 2, 12, 12))   # encosta na parede da esquerda
    assert not mapa.area_livre(pygame.Rect(18, 26, 12, 12))  # encosta na parede de baixo
    assert not mapa.area_livre(pygame.Rect(-2, 2, 12, 12))   # sai do mapa
    assert mapa.area_livre(pygame.Rect(50, 2, 12, 12))       # a saída não é sólida


def test_surgimentos_devolve_copias():
    mapa = criar_mapa()
    pontos = mapa.surgimentos("heroi")
    assert pontos == [pygame.Vector2(24, 8)]
    pontos[0].x = 999
    assert mapa.surgimentos("heroi") == [pygame.Vector2(24, 8)]
    assert mapa.surgimentos("nada") == []


def test_saida():
    assert criar_mapa().saida() == pygame.Rect(48, 0, 16, 16)


def test_ladrilhos_em_so_devolve_a_area_pedida():
    ladrilhos = list(criar_mapa().ladrilhos_em(pygame.Rect(0, 0, 32, 16)))
    assert ladrilhos == [(pygame.Rect(0, 0, 16, 16), "parede"), (pygame.Rect(16, 0, 16, 16), "chao")]


def test_celula_em():
    mapa = criar_mapa()
    assert mapa.celula_em(pygame.Vector2(20, 20)) == "chao"
    assert mapa.celula_em(pygame.Vector2(-5, 20)) == "parede"