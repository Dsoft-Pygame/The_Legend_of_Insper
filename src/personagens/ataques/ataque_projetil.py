"""Classe AtaqueProjetil: atira um ou mais projéteis.

O que é:
    Cobre todos os ataques à distância, só mudando os parâmetros:
        - flecha do arqueiro: quantidade 1, abertura 0;
        - tiro triplo do arqueiro: quantidade 3, abertura 30 graus;
        - bola de fogo do mago: quantidade 1, velocidade baixa, dano alto;
        - anel de fogo do mago e tiros do chefe: quantidade 12,
          abertura 360 graus.

Parâmetros (vêm de data/classes.json ou data/inimigos.json):
    - recarga: float.
    - dano: int.
    - velocidade: float. Pixels por segundo.
    - duracao: float. Segundos até o projétil sumir.
    - quantidade: int.
    - abertura: float. Ângulo total do leque, em graus, centrado na
      direção do olhar.
    - tamanho: int. Lado da caixa do projétil, em pixels.
    - aparencia: str. Chave para o render ("flecha", "bola_fogo").

Métodos:
    - executar(atacante: Personagem) -> list[Projetil].

Quem usa: Fabrica (pelo tipo "projetil" no registro).
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from personagens.projetil import Projetil
if TYPE_CHECKING:
    from personagens.personagem import Personagem


class AtaqueProjetil:
    def __init__(self, recarga: float, dano: int, velocidade: float, duracao: float,
             quantidade: int = 1, abertura: float = 0, tamanho: int = 4,
             aparencia: str = "flecha") -> None:
        self.recarga = recarga
        self.dano = dano
        self.velocidade = velocidade
        self.duracao = duracao
        self.quantidade = quantidade
        self.abertura = abertura
        self.tamanho = tamanho
        self.aparencia = aparencia

    def angulos(self) -> list[float]:
        if self.quantidade <= 1:
            return [0.0]

        if self.abertura >= 360:
            return [i * 360 / self.quantidade
                    for i in range(self.quantidade)]

        passo = self.abertura / (self.quantidade - 1)
        return [-self.abertura / 2 + i * passo
            for i in range(self.quantidade)]

    def executar(self,atacante: Personagem) -> list[Projetil]:
        direcao = pygame.Vector2(atacante.direcao_olhar)
        if direcao.length() == 0:
            direcao = pygame.Vector2(1,0)
        direcao=direcao.normalize()

        projeteis =[]
        for angulo in self.angulos():
            projetil = Projetil(lado=atacante.lado, dono=atacante.id, posicao=pygame.Vector2(atacante.posicao), tamanho=pygame.Vector2(self.tamanho, self.tamanho), aparencia=self.aparencia, velocidade=direcao.rotate(angulo) * self.velocidade, dano=self.dano, duracao=self.duracao)
            projeteis.append(projetil)

        return projeteis