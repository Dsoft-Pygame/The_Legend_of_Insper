"""Botao, EstadoEntrada e a interface DispositivoEntrada.

O que é:
    O que um ControladorHumano precisa saber de um dispositivo, sem saber
    se é teclado, controle ou outra coisa. A interface fica aqui, do lado
    de quem usa, e as implementações ficam em entrada/, do lado do pygame.
    Assim a dependência continua apontando para baixo: entrada/ conhece
    controle/, mas controle/ não conhece entrada/ nem o pygame.

Botao (enum):
    ATAQUE, ESPECIAL. Um botão novo (ex.: ESQUIVAR) entra aqui.

EstadoEntrada (dataclass congelada):
    - eixo: tuple[float, float]. Direção de -1 a 1 em x e em y.
    - segurando: frozenset[Botao]. Botões apertados agora.
    - apertou: frozenset[Botao]. Botões que desceram nesta leitura.

DispositivoEntrada (interface, typing.Protocol):
    - nome: str.
    - ler() -> EstadoEntrada.

Quem usa: ControladorHumano.
Implementam: DispositivoTeclado e DispositivoGamepad (entrada/).
"""
