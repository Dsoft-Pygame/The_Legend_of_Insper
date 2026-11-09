"""Classe ControladorIA (herda de Controlador): a IA no lugar do jogador.

O que é:
    Liga um sistema de decisão (ia/) a um personagem. Cada inimigo tem o
    seu ControladorIA com a sua própria instância de sistema de decisão.
    Os comandos saem pela mesma interface e vão para a mesma fila que os
    do jogador.

    Como na simulação lobo-coelho, a sorte é determinística: a cada tick o
    controlador cria um random.Random com a semente
    "semente:tick:id do personagem". A mesma partida, com os mesmos
    comandos dos jogadores, sempre dá o mesmo resultado (bom para replay e
    para achar bugs).

Atributos:
    - sistema: SistemaDecisao. Quem decide de verdade.
    - semente: int. Semente da partida.

Métodos:
    - gerar_comandos(visao: Visao) -> list[Comando]: cria o gerador do
      tick e devolve sistema.decidir(visao, gerador).

Quem cria: Fabrica.
Quem usa: Nivel.
Usa: ia/sistema_decisao.py, controle/comandos.py.
"""


import random

from controle.comandos import Comando
from controle.controlador import Controlador
from ia.sistema_decisao import SistemaDecisao
from personagens.visao import Visao


class ControladorIA(Controlador):
    def __init__(self, sistema: SistemaDecisao, semente: int) -> None:
        self.sistema = sistema
        self.semente = semente

    def gerar_comandos(self, visao: Visao) -> list[Comando]:
        gerador = random.Random(f"{self.semente}:{visao.tick}:{visao.eu.id}")
        return self.sistema.decidir(visao, gerador)
