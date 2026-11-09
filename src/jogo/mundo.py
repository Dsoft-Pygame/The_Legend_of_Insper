"""Classe Mundo: a partida inteira, com os níveis em sequência.

O que é:
    O Mundo controla a partida: monta os níveis do tema, um de cada vez,
    leva os heróis de um nível para o outro e decide vitória e derrota.
    A TelaJogo só conversa com o Mundo, nunca direto com um Nivel.

    O Mundo não desenha e não conhece a câmera (isso é do render). Ele
    também não sabe quantos jogadores existem: recebe uma lista de heróis.

Heroi (dataclass):
    - numero: int. 1 para o P1, 2 para o P2...
    - nome: str. Nome do jogador.
    - personagem: Personagem.
    - controlador: Controlador. Normalmente um ControladorHumano.

ResumoPartida (dataclass congelada), o que o HUD recebe:
    - herois: tuple[tuple[str, int, int], ...]. Nome, vida e vida máxima
      de cada herói.
    - pontos: int.
    - nome_nivel: str.
    - chefe: tuple[str, int, int] | None. Nome, vida e vida máxima.
    - saida_aberta: bool.

Atributos:
    - tema: DefinicaoTema. Vem do Catalogo (data/temas.json).
    - fabrica: Fabrica. Cria os inimigos de cada nível.
    - herois: list[Heroi]. Passam de nível com a vida que sobrou.
    - indice_nivel: int.
    - nivel_atual: Nivel.
    - pontuacao: Pontuacao. Uma por partida (somada por todos no co-op).
    - tick: int. Quantos ticks já se passaram.
    - tempo_acumulado: float. Tempo real que sobrou e ainda não virou tick.
    - TICKS_POR_SEGUNDO: int. 20. A lógica roda a 20 ticks por segundo,
      enquanto a tela desenha a 60 quadros por segundo (3 quadros por
      tick). Trocar para 30 é mudar só esta constante: tudo que anda ou
      conta tempo usa dt.
    - PASSO: float. Duração fixa de um tick (1 / TICKS_POR_SEGUNDO = 0,05 s).
    - venceu: bool. True quando um chefe cai.

Métodos:
    - tempo_avancar(dt: float) -> None: passo fixo com acumulador, como o
      Simulacao::tempo_avancar: soma dt (no máximo 0,25 s por quadro, ou
      seja, até 5 ticks seguidos) e roda tick_atualizar quantas vezes
      couber. Cada tick representa sempre o mesmo tempo, em PC rápido ou
      lento. Na maioria dos quadros (2 de cada 3, a 60 fps) não roda
      nenhum tick: só a tela é redesenhada.
    - fracao_tick() -> float: tempo_acumulado / PASSO, de 0 a 1. Quanto do
      próximo tick já passou. O render usa para desenhar cada entidade no
      meio do caminho entre a posição do tick anterior e a do atual.
    - tick_atualizar() -> None: roda nivel_atual.tick_atualizar(PASSO, tick)
      e aplica as regras com os eventos que voltaram:
        * PersonagemDerrotado de monstro: soma os pontos dele;
        * PersonagemDerrotado de chefe: soma os pontos do chefe e venceu;
        * HeroiNaSaida: soma os pontos do nível e chama proximo_nivel();
        * todos os heróis derrotados: derrota.
    - proximo_nivel() -> None: carrega o mapa do próximo nível (com o
      carregador que o tema indica), coloca os heróis nos surgimentos
      (colocar_em, para não deslizarem pela tela) e cria os inimigos e o
      chefe pela Fabrica.
    - terminou() -> bool: venceu, ou todos os heróis caíram.
    - resumo() -> ResumoPartida: dados prontos para o HUD.

Quem usa: TelaJogo.
Usa: jogo/nivel.py, jogo/fabrica.py, jogo/pontuacao.py, jogo/eventos.py,
mapa/registro.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame

from jogo.nivel import Nivel
from mapa.registro import criar_carregador

if TYPE_CHECKING:
    from controle.controlador import Controlador
    from jogo.catalogo import DefinicaoTema
    from jogo.fabrica import Fabrica
    from personagens.personagem import Personagem

RAIO_VISAO_HEROI = 160


@dataclass
class Heroi:
    numero: int                 # 1 = P1, 2 = P2
    nome: str                   # o nome que o jogador digitou
    personagem: Personagem
    controlador: Controlador


class Mundo:
    TICKS_POR_SEGUNDO = 20
    PASSO = 1 / TICKS_POR_SEGUNDO          # 0,05 s
    TEMPO_MAXIMO_POR_QUADRO = 0.25

    def __init__(self, tema: DefinicaoTema, fabrica: Fabrica, herois: list[Heroi]) -> None:
        self.tema = tema
        self.fabrica = fabrica
        self.herois = herois
        self.indice_nivel = -1
        self.nivel_atual: Nivel | None = None
        self.tick = 0
        self.tempo_acumulado = 0.0
        self.venceu = False
        self.proximo_nivel()                # monta o nível 1

    def tempo_avancar(self, dt: float) -> None:
        # passo fixo com acumulador: roda quantos ticks de PASSO couberem
        self.tempo_acumulado += min(dt, self.TEMPO_MAXIMO_POR_QUADRO)
        while self.tempo_acumulado >= self.PASSO and not self.terminou():
            self.tick_atualizar()
            self.tempo_acumulado -= self.PASSO

    def fracao_tick(self) -> float:
        return min(1.0, self.tempo_acumulado / self.PASSO)

    def tick_atualizar(self) -> None:
        eventos = self.nivel_atual.tick_atualizar(self.PASSO, self.tick)
        self.tick += 1
        # regras com os eventos: T51

    def proximo_nivel(self) -> None:
        if self.indice_nivel + 1 >= len(self.tema.niveis):
            self.venceu = True
            return
        self.indice_nivel += 1
        definicao = self.tema.niveis[self.indice_nivel]
        mapa = criar_carregador(definicao.carregador).carregar(definicao.mapa)
        nivel = Nivel(definicao.nome, self.indice_nivel + 1, mapa)

        pontos = mapa.surgimentos("heroi")
        for i, heroi in enumerate(self.herois):
            if not heroi.personagem.esta_vivo:
                continue
            posicao = pontos[i] if i < len(pontos) else pontos[0] + pygame.Vector2(16 * i, 0)
            heroi.personagem.colocar_em(posicao)
            nivel.adicionar(heroi.personagem, heroi.controlador, RAIO_VISAO_HEROI)

        # inimigos e chefe: T51
        self.nivel_atual = nivel

    def terminou(self) -> bool:
        return self.venceu          # "ou todos os heróis caíram": T51
