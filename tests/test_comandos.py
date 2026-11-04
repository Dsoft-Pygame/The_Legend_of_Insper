import pygame

from controle.comandos import Atacar, Especial, Mover


class AtorDeTeste:
    """Um "personagem de mentira": só anota o que pediram para ele."""

    def __init__(self):
        self.pedidos = []

    def mover(self, direcao):
        self.pedidos.append(("mover", direcao))

    def atacar(self):
        self.pedidos.append(("atacar",))

    def especial(self):
        self.pedidos.append(("especial",))


def test_cada_comando_chama_a_acao_certa():
    ator = AtorDeTeste()
    Mover((1, 0)).aplicar(ator)
    Atacar().aplicar(ator)
    Especial().aplicar(ator)
    assert ator.pedidos == [("mover", pygame.Vector2(1, 0)), ("atacar",), ("especial",)]


def test_comandos_sao_dados_comparaveis():
    assert Mover((1, 0)) == Mover((1, 0))
    assert Atacar() == Atacar()