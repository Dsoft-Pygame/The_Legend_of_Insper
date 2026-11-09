"""Classe DecisaoPerseguir: vaga até ver um herói, então vai atrás dele.

O que é:
    A IA dos inimigos comuns (Slime, Esqueleto). Antes era o método
    Inimigo.pensar(jogador); agora é um sistema de decisão separado, que
    serve para qualquer personagem, inclusive um herói no piloto automático.

Parâmetros (vêm do campo "decisao" em data/inimigos.json):
    - raio_alerta: float. A partir de quantos pixels começa a perseguir.
    - distancia_ataque: float. Perto assim, pede Atacar() (se o personagem
      não tiver ataque, o dano é só por contato).
    - tempo_vagando: float. Segundos andando numa direção antes de sortear
      outra.

Memória:
    - direcao_vagando: pygame.Vector2.
    - tempo_restante: float.

Métodos:
    - decidir(visao: Visao, gerador: random.Random) -> list[Comando]:
        1. procura o herói mais próximo (visao.mais_proximo(Lado.HEROIS));
        2. se ele estiver dentro do raio_alerta, Mover na direção dele e,
           se estiver perto, Atacar;
        3. senão, vaga: segue na direção sorteada ou fica parado.
      Com vários heróis (co-op), persegue o mais próximo.

Quem usa: ControladorIA (pelo nome "perseguir" no registro).
Usa: personagens/visao.py, controle/comandos.py.
"""


import random

import pygame

from controle.comandos import Atacar, Comando, Mover
from personagens.visao import Visao

CHANCE_FICAR_PARADO = 0.3           # 30% das vezes, vagar = ficar parado
FRACAO_VELOCIDADE_VAGANDO = 0.5     # vagando, anda na metade da velocidade


class DecisaoPerseguir:
    def __init__(self, raio_alerta: float, distancia_ataque: float = 0,
                 tempo_vagando: float = 1.5) -> None:
        self.raio_alerta = raio_alerta
        self.distancia_ataque = distancia_ataque
        self.tempo_vagando = tempo_vagando
        self.direcao_vagando = pygame.Vector2(0, 0)
        self.tempo_restante = 0.0

    def decidir(self, visao: Visao, gerador: random.Random) -> list[Comando]:
        alvo = visao.mais_proximo(visao.eu.lado.oposto())
        if alvo is not None:
            caminho = alvo.posicao - visao.eu.posicao
            distancia = caminho.length()
            if distancia <= self.raio_alerta:
                comandos: list[Comando] = []
                if distancia > 0:
                    direcao = caminho.normalize()
                    comandos.append(Mover((direcao.x, direcao.y)))
                if (self.distancia_ataque > 0 and distancia <= self.distancia_ataque
                        and visao.pode_atacar):
                    comandos.append(Atacar())
                return comandos
        return self.vagar(visao, gerador)

    def vagar(self, visao: Visao, gerador: random.Random) -> list[Comando]:
        self.tempo_restante -= visao.dt
        if self.tempo_restante <= 0:
            self.tempo_restante = self.tempo_vagando
            if gerador.random() < CHANCE_FICAR_PARADO:
                self.direcao_vagando = pygame.Vector2(0, 0)
            else:
                angulo = gerador.uniform(0, 360)
                self.direcao_vagando = pygame.Vector2(1, 0).rotate(angulo) * FRACAO_VELOCIDADE_VAGANDO
        if self.direcao_vagando.length() == 0:
            return []
        return [Mover((self.direcao_vagando.x, self.direcao_vagando.y))]
