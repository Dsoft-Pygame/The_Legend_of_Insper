"""Interface SistemaDecisao (typing.Protocol): o "cérebro" de um inimigo.

O que é:
    O equivalente do SistemaDecisao da simulação lobo-coelho. A entidade
    (Personagem) fica em personagens/; o que ela decide fazer fica aqui,
    em arquivos separados.

    Regras para todo sistema de decisão:
        - recebe só a Visao (um retrato, só leitura), nunca o Personagem,
          o Nivel ou o Mundo;
        - devolve uma lista de comandos (Mover, Atacar, Especial) e não
          altera nada do mundo;
        - pode ter memória própria (para onde está vagando, há quanto tempo
          mudou de direção), porque cada inimigo tem a sua instância;
        - toda sorte vem do gerador recebido, nunca do módulo random
          global, para a partida ser reproduzível.

Métodos:
    - decidir(visao: Visao, gerador: random.Random) -> list[Comando].

Implementações: DecisaoPerseguir, DecisaoZigueZague e DecisaoChefe.
Quem usa: ControladorIA.
"""


import random
from typing import Protocol

from controle.comandos import Comando
from personagens.visao import Visao


class SistemaDecisao(Protocol):
    def decidir(self, visao: Visao, gerador: random.Random) -> list[Comando]: ...
