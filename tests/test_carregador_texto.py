import pygame
import pytest

from mapa.carregador_texto import CarregadorTexto
from mapa.registro import criar_carregador


def test_carrega_o_mapa_do_nivel_1():
    mapa = CarregadorTexto().carregar("mapas/torre_1.txt")
    assert mapa.largura > 240 and mapa.altura > 160      # maior que a tela
    assert len(mapa.surgimentos("heroi")) >= 1
    assert len(mapa.surgimentos("inimigo")) >= 6
    assert mapa.saida() is not None


def test_marcadores_viram_chao_e_surgimento(tmp_path):
    (tmp_path / "mini.txt").write_text("####\n#HI#\n####\n", encoding="utf-8")
    mapa = CarregadorTexto(tmp_path).carregar("mini.txt")
    assert mapa.surgimentos("heroi") == [pygame.Vector2(24, 24)]
    assert mapa.surgimentos("inimigo") == [pygame.Vector2(40, 24)]
    assert mapa.celula_em(pygame.Vector2(24, 24)) == "chao"


def test_linha_de_tamanho_diferente_da_erro(tmp_path):
    (tmp_path / "torto.txt").write_text("####\n#..\n####\n", encoding="utf-8")
    with pytest.raises(ValueError, match="linha 2"):
        CarregadorTexto(tmp_path).carregar("torto.txt")


def test_caractere_desconhecido_da_erro(tmp_path):
    (tmp_path / "x.txt").write_text("####\n#.X#\n####\n", encoding="utf-8")
    with pytest.raises(ValueError, match="'X'"):
        CarregadorTexto(tmp_path).carregar("x.txt")


def test_registro():
    assert isinstance(criar_carregador("texto"), CarregadorTexto)
    with pytest.raises(ValueError):
        criar_carregador("tiled")
