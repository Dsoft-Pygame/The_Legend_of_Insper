"""Classes Sessao e PerfilJogador: quem está jogando agora.

O que é:
    A Sessao substitui as antigas variáveis "nome_jogador" e
    "classe_escolhida" da Aplicacao. Em vez de um jogador fixo, ela guarda
    uma LISTA de perfis. Hoje a lista tem um perfil só; o co-op local é
    colocar um segundo perfil, sem mudar nenhuma outra classe.

PerfilJogador (dataclass):
    - numero: int. 1 para o P1, 2 para o P2...
    - nome: str. Digitado na TelaInicial.
    - dispositivo: str. Nome do dispositivo de entrada desse jogador
      ("teclado_wasd", "teclado_setas", "gamepad_0"...).
    - classe: str | None. Chave da classe em data/classes.json ("mago",
      "arqueiro", "barbaro"); None até a TelaClasses.

Sessao:
    Atributos:
        - jogadores: list[PerfilJogador].
        - tema: str. Chave do tema em data/temas.json.
        - pontuacao: Pontuacao | None. A da partida atual (uma só no co-op).
        - venceu: bool. Resultado da última partida.

    Métodos:
        - adicionar_jogador(nome: str, dispositivo: str) -> PerfilJogador.
        - buscar(numero: int) -> PerfilJogador | None.
        - limpar() -> None: começa uma sessão nova.

Quem usa: Aplicacao, TelaInicial, TelaClasses, TelaJogo, TelaResultado.
Usa: jogo/pontuacao.py.
"""


from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jogo.pontuacao import Pontuacao


@dataclass
class PerfilJogador:
    numero: int
    nome: str
    dispositivo: str
    classe: str | None = None


class Sessao:
    def __init__(self) -> None:
        self.jogadores: list[PerfilJogador] = []
        self.tema: str = ""
        self.pontuacao: Pontuacao | None = None
        self.venceu: bool = False
        self.tempo_partida: float = 0.0
        self.vida_restante: float = 0.0

    def adicionar_jogador(self, nome: str, dispositivo: str) -> PerfilJogador:
        numero = len(self.jogadores) + 1
        perfil = PerfilJogador(numero=numero, nome=nome, dispositivo=dispositivo)
        self.jogadores.append(perfil)
        return perfil

    def buscar(self, numero: int) -> PerfilJogador | None:
        for perfil in self.jogadores:
            if perfil.numero == numero:
                return perfil
        return None

    def limpar(self) -> None:
        self.jogadores = []
        self.pontuacao = None
        self.venceu = False
        self.tempo_partida = 0.0
        self.vida_restante = 0.0