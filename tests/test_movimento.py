import pygame
import pytest

from mapa.mapa_tiles import MapaTiles
from movimento.movimento import caixa_em
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
    corpo = CorpoDeTeste(22, 40)                  # encostado na parede da esquerda (caixa.left = 16)
    corpo.intencao = pygame.Vector2(-1, 1).normalize()
    MovimentoLivre().atualizar(corpo, sala(), 0.05)
    assert corpo.posicao.x == 22                  # não entrou na parede
    assert corpo.posicao.y > 40                   # mas desceu (deslizou)


def andar_ate_parar(corpo, mapa, direcao, ticks=40):
    movimento = MovimentoLivre()
    for _ in range(ticks):
        corpo.intencao = pygame.Vector2(direcao)
        if corpo.intencao.length() > 1:
            corpo.intencao = corpo.intencao.normalize()
        movimento.atualizar(corpo, mapa, 0.05)
    return caixa_em(corpo.posicao, corpo.tamanho)


@pytest.mark.parametrize("velocidade", [30, 70, 75, 100])
@pytest.mark.parametrize("x_inicial", [40, 40.3, 40.5, 41.7])
def test_encosta_na_parede_sem_sobrar_espaco(velocidade, x_inicial):
    # antes: o passo inteiro não cabia e o corpo parava a 1-3 px da parede
    for direcao, lado in [((-1, 0), "left"), ((1, 0), "right"), ((0, -1), "top"), ((0, 1), "bottom")]:
        corpo = CorpoDeTeste(x_inicial, x_inicial)
        corpo.velocidade = velocidade
        caixa = andar_ate_parar(corpo, sala(), direcao)
        parede = {"left": 16, "top": 16, "right": 64, "bottom": 64}[lado]
        assert getattr(caixa, lado) == parede


@pytest.mark.parametrize("velocidade", [70, 75, 100])
@pytest.mark.parametrize("direcao", [(1, 1), (-1, -1), (1, -1), (-1, 1)])
def test_quina_fecha_nos_dois_lados(velocidade, direcao):
    corpo = CorpoDeTeste(40.3, 41.7)
    corpo.velocidade = velocidade
    caixa = andar_ate_parar(corpo, sala(), direcao)
    assert caixa.left == 16 or caixa.right == 64
    assert caixa.top == 16 or caixa.bottom == 64
    assert corpo.posicao == pygame.Vector2(caixa.center)   # sem sobra de fração


def corredor():
    # corredor de 1 tile saindo para cima a partir da sala
    linhas = ["##.##", "##.##", "#...#", "#...#", "#####"]
    celulas = [["parede" if c == "#" else "chao" for c in linha] for linha in linhas]
    return MapaTiles(celulas, {}, 16)


@pytest.mark.parametrize("desvio", [-4, -2, 2, 4])
def test_contorna_quina_na_entrada_do_corredor(desvio):
    # herói 12 px num corredor de 16 px: desalinhado até 4 px, ainda entra
    corpo = CorpoDeTeste(40 + desvio, 40)
    caixa = andar_ate_parar(corpo, corredor(), (0, -1), ticks=20)
    assert caixa.top < 32                          # entrou no corredor
    assert 32 <= caixa.left and caixa.right <= 48


def test_nao_contorna_parede_lisa():
    corpo = CorpoDeTeste(40, 40)
    caixa = andar_ate_parar(corpo, sala(), (0, -1))
    assert caixa.top == 16 and caixa.centerx == 40  # só encostou, não escorregou de lado


def test_caixa_arredonda_meio_pixel_sempre_para_cima():
    tamanho = pygame.Vector2(12, 12)
    assert caixa_em(pygame.Vector2(22.5, 23.5), tamanho).center == (23, 24)


def test_registro():
    assert isinstance(criar_movimento("livre"), MovimentoLivre)
    with pytest.raises(ValueError):
        criar_movimento("voando")