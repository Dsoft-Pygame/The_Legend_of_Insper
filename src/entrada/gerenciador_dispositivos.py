"""DispositivoFisico e GerenciadorDispositivos: teclados e controles.

DispositivoFisico (interface, typing.Protocol):
    A interface DispositivoEntrada (controle/dispositivo.py) mais dois
    métodos que só a camada de entrada usa:
        - amostrar() -> None: olha o hardware agora. Chamado a cada
          quadro (60 vezes por segundo). Guarda os botões que desceram
          até o próximo ler().
        - limpar() -> None: esquece os botões guardados.
    O ControladorHumano continua vendo só ler(), uma vez por tick
    (20 vezes por segundo).

GerenciadorDispositivos:
    O que é:
        Guarda todos os dispositivos disponíveis e diz qual está livre
        para um jogador novo. É o que deixa o co-op local pronto: cada
        PerfilJogador da Sessao guarda o nome de um dispositivo, e a
        TelaJogo pede o dispositivo por esse nome.

        Ao abrir o jogo, cria os teclados de data/controles.json
        ("teclado_wasd" e "teclado_setas") e um DispositivoGamepad para
        cada controle conectado. Controles ligados ou desligados no meio
        do jogo chegam pelo EntradaQuadro.

    Atributos:
        - dispositivos: dict[str, DispositivoFisico]. Por nome.
        - em_uso: set[str]. Nomes já entregues a algum jogador.

    Métodos:
        - atualizar(entrada: EntradaQuadro) -> None: cria ou remove gamepads.
        - amostrar() -> None: chama amostrar() de todos os dispositivos.
          A Aplicacao chama a cada quadro, logo depois de ler_quadro().
        - livres() -> list[str]: nomes dos dispositivos sem dono.
        - reservar(nome: str) -> DispositivoEntrada: marca como em uso,
          chama limpar() (o toque que confirmou o menu não vira ataque) e
          devolve.
        - liberar(nome: str) -> None: devolve ao fim da partida.
        - buscar(nome: str) -> DispositivoEntrada | None.

Quem usa: Aplicacao (cria, atualiza e amostra a cada quadro), TelaInicial
(escolhe o dispositivo de cada jogador), TelaJogo (pede o dispositivo).
Usa: entrada/teclado.py, entrada/gamepad.py, controle/dispositivo.py,
data/controles.json.
"""
from typing import Protocol

from controle.dispositivo import DispositivoEntrada
from entrada.entrada_menu import EntradaQuadro
from entrada.teclado import DispositivoTeclado


class DispositivoFisico(DispositivoEntrada, Protocol):
 
    def amostrar(self) -> None: ... # mesmas funções do dispositivo teclado
    def limpar(self) -> None: ...

class GerenciadorDispositivos: # para receber alem do wasd, setinas, gampads e outros controladores
    def __init__(self, controles: dict) -> None:
        self.dispositivos = {}
        self.em_uso = set()
        self.config_gamepad ={}
        for nome, config in controles.items():
            if config["tipo"] == "teclado":
                self.dispositivos[nome] = DispositivoTeclado.de_config(nome, config)
            if config["tipo"] == "gamepad":
                self.config_gamepad = config


    def atualizar(self, entrada: EntradaQuadro) -> None: # controles ligados ou desligados
        pass #ainda sem função específica, mas futuramente vai atualizar os dispositivos conectados
    
    def amostrar(self) -> None:
        for dispositivo in self.dispositivos.values():
            dispositivo.amostrar()
        
    def livres(self) -> list[str]:
        nomes = []
        for nome in self.dispositivos.keys():
            if nome not in self.em_uso:
                nomes.append(nome)
        return nomes
    
    def reservar(self, nome: str) -> DispositivoEntrada:
        dispositivo = self.dispositivos[nome]
        self.em_uso.add(nome)
        dispositivo.limpar() #o toque que confirmou o menu não vira ataque
        return dispositivo
    
    def liberar(self, nome: str) -> None:
        self.em_uso.discard(nome) #discard e não remove, caso o nome não esteja no set, nunca se sabe né

    def buscar(self, nome: str) -> DispositivoEntrada | None:
        if nome in self.dispositivos:
            return self.dispositivos[nome]
        else:
            return None
        