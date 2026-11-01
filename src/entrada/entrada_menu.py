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
