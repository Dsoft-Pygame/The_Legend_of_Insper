"""Ator, Comando e os comandos Mover, Atacar e Especial.

O que é:
    Um comando é um PEDIDO de ação guardado como dado, como a struct Acao
    da simulação lobo-coelho. Controladores (humano ou IA) criam comandos,
    a FilaComandos guarda e o Nivel aplica no personagem. O personagem não
    sabe quem pediu: jogador, IA, replay ou rede.

    Cada comando sabe se aplicar (método aplicar), então um comando novo
    não exige mexer num "switch" central como o executar_acoes da simulação.

Ator (interface, typing.Protocol):
    O que um comando pode pedir. O Personagem satisfaz essa interface sem
    importar nada daqui.
    - mover(direcao: pygame.Vector2) -> None
    - atacar() -> None
    - especial() -> None

Comando (interface, typing.Protocol):
    - aplicar(ator: Ator) -> None

Comandos (dataclasses congeladas, só com campos simples, fáceis de salvar
num replay ou mandar pela rede):
    - Mover(direcao: tuple[float, float]): chama ator.mover(direcao).
      O tamanho da direção (0 a 1) é a fração da velocidade.
    - Atacar(): chama ator.atacar().
    - Especial(): chama ator.especial().

Uma ação nova (ex.: Esquivar) = um comando novo aqui, o método no
Personagem e um Botao novo em dispositivo.py.

Quem usa: ControladorHumano, ControladorIA, ia/, FilaComandos, Nivel.
"""


from dataclasses import dataclass
from typing import Protocol

import pygame


class Ator(Protocol):
    def mover(self, direcao: pygame.Vector2) -> None: ...
    def atacar(self) -> None: ...
    def especial(self) -> None: ...


class Comando(Protocol):
    def aplicar(self, ator: Ator) -> None: ...


@dataclass(frozen=True)
class Mover:
    direcao: tuple[float, float]

    def aplicar(self, ator: Ator) -> None:
        ator.mover(pygame.Vector2(self.direcao))


@dataclass(frozen=True)
class Atacar:
    def aplicar(self, ator: Ator) -> None:
        ator.atacar()


@dataclass(frozen=True)
class Especial:
    def aplicar(self, ator: Ator) -> None:
        ator.especial() 
        