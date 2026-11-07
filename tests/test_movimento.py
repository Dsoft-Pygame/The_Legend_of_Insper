import pygame
import pytest

from mapa.mapa_tiles import MapaTiles
from movimento.movimento_livre import MovimentoLivre
from movimento.registro import criar_movimento


class CorpoDeTeste:
    def __init__(self, x, y):
        self.posicao = pygame.Vector2(x, y)
        self.tamanho = pygame.Vector2(12, 12)
        self.velocidade = 80.0
        self.intencao = pygame.Vector2(0, 0)


def sala():
    # 5x5 tiles, paredes em volta
    linhas = ["#####", "#...#", "#...#", "#...#", "#####"]
    celulas = [["parede" if c == "#" else "chao" for c in linha] for linha in linhas]
    return MapaTiles(celulas, {}, 16)


def test_anda_intencao_vezes_velocidade_vezes_dt():
    corpo = CorpoDeTeste(40, 40)
    corpo.intencao = pygame.Vector2(1, 0)
    MovimentoLivre().atualizar(corpo, sala(), 0.05)
    assert corpo.posicao == pygame.Vector2(44, 40)   # 80 px/s * 0,05 s = 4 px


def test_zera_a_intencao_depois_de_andar():
    corpo = CorpoDeTeste(40, 40)
    corpo.intencao = pygame.Vector2(1, 0)
    MovimentoLivre().atualizar(corpo, sala(), 0.05)
    assert corpo.intencao == pygame.Vector2(0, 0)


def test_nao_atravessa_parede_e_desliza():
    corpo = CorpoDeTeste(24, 40)                  # encostado na parede da esquerda
    corpo.intencao = pygame.Vector2(-1, 1).normalize()
    MovimentoLivre().atualizar(corpo, sala(), 0.05)
    assert corpo.posicao.x == 24                  # não entrou na parede
    assert corpo.posicao.y > 40                   # mas desceu (deslizou)


def test_registro():
    assert isinstance(criar_movimento("livre"), MovimentoLivre)
    with pytest.raises(ValueError):
        criar_movimento("voando")