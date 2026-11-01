"""Classe DispositivoGamepad: um controle (joystick) como dispositivo.

O que é:
    Um controle conectado ao PC. Implementa a mesma interface
    DispositivoFisico que o teclado (amostrar a cada quadro, ler a cada
    tick), então trocar teclado por controle é só entregar outro
    dispositivo ao ControladorHumano.

Atributos:
    - nome: str. Ex.: "gamepad_0".
    - indice: int. Índice do joystick no pygame.
    - joystick: pygame.joystick.Joystick.
    - zona_morta: float. Abaixo disso o analógico conta como parado (0.2).
    - botoes: dict[Botao, int]. Qual botão físico é ataque e qual é
      especial (vem de data/controles.json).
    - eixo, segurando, segurando_antes, apertou_guardado: iguais aos do
      DispositivoTeclado.

Métodos:
    - amostrar() -> None: a cada quadro, lê o analógico esquerdo (ou o
      direcional) e os botões, e guarda os botões que desceram. No
      analógico o eixo pode ser fracionário: meio analógico = meia
      velocidade.
    - ler() -> EstadoEntrada: a cada tick, no mesmo formato do teclado;
      esvazia os botões guardados.
    - limpar() -> None: esquece os botões guardados.
    - conectado() -> bool: False se o controle foi desligado no meio do jogo.

Quem usa: GerenciadorDispositivos.
Usa: controle/dispositivo.py.
"""
