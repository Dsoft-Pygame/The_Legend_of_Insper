"""Classe Controlador (base abstrata, abc.ABC): quem manda num personagem.

O que é:
    O molde de tudo que pode controlar um personagem. O Nivel guarda um
    controlador para cada personagem (por id) e, a cada tick, pede os
    comandos dele. Trocar quem controla um personagem é só trocar o
    controlador com nivel.trocar_controlador(id, novo_controlador):
        - um herói com ControladorIA vira piloto automático;
        - um slime com ControladorHumano passa a ser jogado por alguém.
    O personagem não muda em nada.

Métodos:
    - gerar_comandos(visao: Visao) -> list[Comando] (abstrato): o que o
      personagem deve fazer neste tick. A Visao é o retrato do que o
      personagem enxerga; o controlador humano ignora, a IA usa.

Herdam dela: ControladorHumano e ControladorIA.
Possíveis no futuro: ControladorReplay (devolve comandos gravados) e
ControladorRede (comandos vindos de outro PC).
"""


from abc import ABC, abstractmethod

from controle.comandos import Comando
from personagens.visao import Visao


class Controlador(ABC):
    @abstractmethod
    def gerar_comandos(self, visao: Visao) -> list[Comando]: ...