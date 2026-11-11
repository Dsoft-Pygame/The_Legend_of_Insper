"""Classe Fabrica: monta personagens e controladores a partir dos dados.

O que é:
    O único lugar que junta as peças: definição dos dados + Movimento +
    Ataques + sistema de decisão. Ninguém mais precisa saber como um slime
    é montado. Um inimigo novo que reaproveita peças existentes não mexe
    aqui, só no JSON.

Atributos:
    - catalogo: Catalogo. Definições lidas de data/.
    - semente: int. Passada para cada ControladorIA.

Métodos:
    - criar_heroi(classe: str, posicao: pygame.Vector2) -> Personagem:
      monta o Personagem do lado HEROIS com a ClasseHeroi escolhida. O
      controlador do herói não é criado aqui: quem cria é a TelaJogo,
      porque depende do dispositivo de cada jogador.
    - criar_monstro(tipo: str, posicao: pygame.Vector2)
      -> tuple[Personagem, Controlador]: monta o Personagem do lado
      MONSTROS e o ControladorIA com o sistema de decisão do JSON.

Quem usa: Mundo e TelaJogo.
Usa: jogo/catalogo.py, movimento/registro.py,
personagens/ataques/registro.py, ia/registro.py,
controle/controlador_ia.py.
"""


from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from movimento.registro import criar_movimento
from personagens.personagem import Personagem
from personagens.tipos import Lado
from personagens.ataques.registro import criar_ataque
from controle.controlador_ia import ControladorIA
from ia.registro import criar_decisao

if TYPE_CHECKING:
    from jogo.catalogo import Catalogo
    from controle.controlador import Controlador

TAMANHO_PERSONAGEM = (12, 12)       # um pouco menor que o tile (16): passa em corredor de 1 tile
TAMANHO_CHEFE = (24, 24)
TEMPO_INVULNERAVEL_HEROI = 0.8      # segundos piscando depois de levar dano


class Fabrica:
    def __init__(self, catalogo: Catalogo, semente: int = 0) -> None:
        self.catalogo = catalogo
        self.semente = semente

    def criar_heroi(self, classe: str, posicao: pygame.Vector2) -> Personagem:
        definicao = self.catalogo.classes[classe]
        return Personagem(
            lado=Lado.HEROIS, nome=definicao.nome, posicao=posicao,
            tamanho=pygame.Vector2(TAMANHO_PERSONAGEM), aparencia=definicao.aparencia,
            vida_maxima=definicao.vida_maxima, velocidade=definicao.velocidade,
            movimento=criar_movimento(definicao.movimento),           # T22
            tempo_invulneravel=TEMPO_INVULNERAVEL_HEROI, 
            ataque=criar_ataque(definicao.ataque), ataque_especial=criar_ataque(definicao.especial)
        )

    def criar_monstro(self, tipo: str, posicao: pygame.Vector2) -> tuple[Personagem, Controlador]:
        definicao = self.catalogo.inimigos[tipo]
        tamanho = TAMANHO_CHEFE if definicao.chefe else TAMANHO_PERSONAGEM
        personagem = Personagem(
            lado=Lado.MONSTROS, nome=definicao.nome, posicao=posicao,
            tamanho=pygame.Vector2(tamanho), aparencia=definicao.aparencia,
            vida_maxima=definicao.vida, velocidade=definicao.velocidade,
            movimento=criar_movimento(definicao.movimento),
            ataque=criar_ataque(definicao.ataque), ataque_especial=criar_ataque(definicao.especial),
            dano_contato=definicao.dano_contato, pontos=definicao.pontos, chefe=definicao.chefe)
        controlador = ControladorIA(criar_decisao(definicao.decisao), self.semente)
        return personagem, controlador 