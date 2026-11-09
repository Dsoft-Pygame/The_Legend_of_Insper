import pygame

from controle.controlador import Controlador
from jogo.catalogo import Catalogo
from jogo.fabrica import Fabrica
from jogo.mundo import Heroi, Mundo


class Parado(Controlador):
    def gerar_comandos(self, visao):
        return []


def criar_mundo(classe="mago", controlador=None):
    catalogo = Catalogo.carregar()
    fabrica = Fabrica(catalogo, semente=1)
    personagem = fabrica.criar_heroi(classe, pygame.Vector2(0, 0))
    heroi = Heroi(1, "Ana", personagem, controlador or Parado())
    return Mundo(catalogo.temas[catalogo.tema_padrao], fabrica, [heroi])


def test_comeca_no_primeiro_nivel_com_o_heroi_no_H():
    mundo = criar_mundo()
    assert mundo.nivel_atual.numero == 1
    heroi = mundo.herois[0].personagem
    assert heroi.posicao == mundo.nivel_atual.mapa.surgimentos("heroi")[0]


def test_passo_fixo():
    mundo = criar_mundo()
    mundo.tempo_avancar(1 / 60)
    assert mundo.tick == 0                          # 1 quadro: ainda não deu um tick
    mundo.tempo_avancar(1 / 60)
    mundo.tempo_avancar(1 / 60)
    assert mundo.tick == 1                          # 3 quadros = 1 tick
    mundo.tempo_avancar(1.0)                        # travou 1 s: no máximo 0,25 s = 5 ticks
    assert mundo.tick == 6
    assert 0 <= mundo.fracao_tick() < 1
