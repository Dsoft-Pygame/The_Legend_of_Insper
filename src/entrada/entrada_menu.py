"""AcaoMenu, EntradaMenu e EntradaQuadro: o que sai da camada de entrada.

O que é:
    Dados simples (enum e dataclasses congeladas), sem pygame. É isso que
    as telas recebem no lugar dos eventos crus do pygame. Assim uma tela
    funciona igual com teclado ou com controle.

AcaoMenu (enum):
    CIMA, BAIXO, ESQUERDA, DIREITA, CONFIRMAR, VOLTAR, APAGAR.

EntradaMenu (dataclass congelada):
    - acoes: tuple[tuple[AcaoMenu, str], ...]. Ações de menu deste quadro,
      em ordem. Cada uma vem com o nome do dispositivo que apertou
      ("teclado", "gamepad_0"...). Hoje as telas só olham a ação; o nome
      serve para o co-op saber qual jogador apertou.
    - texto: str. Letras digitadas neste quadro (pode ser "").

EntradaQuadro (dataclass congelada):
    - fechar: bool. A janela foi fechada.
    - menu: EntradaMenu.
    - controles_ligados: tuple[int, ...]. Joysticks conectados agora.
    - controles_desligados: tuple[int, ...]. Joysticks desconectados agora.

Quem cria: LeitorEntrada.
Quem usa: Aplicacao, GerenciadorDispositivos, telas/.
"""
from dataclasses import dataclass, field
from enum import Enum, auto

class AcaoMenu(Enum):
    CIMA = auto()
    BAIXO = auto()
    ESQUERDA = auto()
    DIREITA = auto()
    CONFIRMAR = auto()
    VOLTAR = auto()
    APAGAR = auto()


@dataclass(frozen=True)
class EntradaMenu:
    acoes: tuple[tuple[AcaoMenu, str], ...] = ()   # (ação, nome do dispositivo), em ordem
    texto: str = ""                                 # letras digitadas neste quadro

    def tem(self, acao: AcaoMenu) -> bool:
        return any(a == acao for a, _ in self.acoes)

    def dispositivo_de(self, acao: AcaoMenu) -> str | None:
        for a, dispositivo in self.acoes:
            if a == acao:
                return dispositivo
        return None


@dataclass(frozen=True)
class EntradaQuadro:
    fechar: bool = False
    menu: EntradaMenu = field(default_factory=EntradaMenu)
    controles_ligados: tuple[int, ...] = ()
    controles_desligados: tuple[int, ...] = ()