"""Classe ControladorHumano (herda de Controlador): um jogador de verdade.

O que é:
    Transforma o que um dispositivo de entrada diz em comandos. Serve para
    teclado e para controle, porque a diferença entre os dois já fica no
    dispositivo (entrada/). Por isso não existem um controlador de teclado
    e outro de gamepad: os dois teriam o mesmo código.

Atributos:
    - dispositivo: DispositivoEntrada. O teclado (uma parte dele) ou o
      controle deste jogador.

Métodos:
    - gerar_comandos(visao: Visao) -> list[Comando]: chamado uma vez por
      tick. Lê o dispositivo (dispositivo.ler()) e:
        * eixo diferente de (0, 0) -> Mover(eixo);
        * apertou ATAQUE -> Atacar() (vale também um toque rápido que
          já foi solto antes do tick: o dispositivo guardou);
        * apertou ESPECIAL -> Especial().
      Ignora a visão.

Quem cria: TelaJogo (um por jogador da Sessao).
Quem usa: Nivel.
Usa: controle/dispositivo.py, controle/comandos.py.
"""


from controle.comandos import Atacar, Comando, Especial, Mover
from controle.controlador import Controlador
from controle.dispositivo import Botao, DispositivoEntrada
from personagens.visao import Visao


class ControladorHumano(Controlador):
    def __init__(self, dispositivo: DispositivoEntrada) -> None:
        self.dispositivo = dispositivo

    def gerar_comandos(self, visao: Visao) -> list[Comando]:
        estado = self.dispositivo.ler()
        comandos: list[Comando] = []

        if estado.eixo != (0, 0):
            comandos.append(Mover(estado.eixo))

        if Botao.ATAQUE in estado.apertou:
            comandos.append(Atacar())

        if Botao.ESPECIAL in estado.apertou:
            comandos.append(Especial())

        return comandos