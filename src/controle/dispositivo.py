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
    - apertou: frozenset[Botao]. Botões que desceram desde a leitura
      anterior, MESMO QUE JÁ TENHAM SIDO SOLTOS. A leitura acontece uma
      vez por tick (a cada 0,05 s); um toque rápido de espaço que começa
      e termina entre dois ticks ainda chega como ataque.

DispositivoEntrada (interface, typing.Protocol):
    - nome: str.
    - ler() -> EstadoEntrada: o ControladorHumano chama uma vez por tick.
      Devolve o estado e esquece os "apertou" já entregues.

    Quem olha o hardware a cada quadro e guarda os toques até o ler() é
    o próprio dispositivo (ver DispositivoFisico em
    entrada/gerenciador_dispositivos.py). O controlador não precisa
    saber disso.

Quem usa: ControladorHumano.
Implementam: DispositivoTeclado e DispositivoGamepad (entrada/).
"""
