"""Classe CartaoClasse: o cartão de uma classe na tela de escolha.

Atributos:
    - classe: ClasseHeroi. Os dados da classe (vêm de data/classes.json).
    - retangulo: pygame.Rect. Posição e tamanho do cartão.

Métodos:
    - desenhar(superficie: pygame.Surface, aparencias: Aparencias,
      selecionado: bool) -> None: desenha a imagem (pela chave de
      aparência), o nome e os atributos (vida, velocidade, dano do
      ataque). Com selecionado=True, a borda fica destacada.

Usada em: TelaClasses.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from render.aparencias import desenhar_visual
from settings import DARK_GRAY, GRAY, WHITE, YELLOW
from telas import tela
from ui.texto import desenhar_texto


if TYPE_CHECKING:
    from personagens.classe_heroi import ClasseHeroi
    from render.aparencias import Aparencias

class CartaoClasse: # o cartão de uma classe na tela de escolha
    def __init__(self, classe: ClasseHeroi, retangulo: pygame.Rect) -> None:
        self.classe = classe
        self.retangulo = retangulo

    def desenhar(self, superficie: pygame.Surface, aparencias: Aparencias,selecionado: bool) -> None:
        # desenha a imagem, o nome e os atributos e se foi escolhido ou não
        r=self.retangulo
        pygame.draw.rect(superficie, DARK_GRAY,r) #fundo do cartão
        pygame.draw.rect(superficie, YELLOW if selecionado else GRAY,r,2 if selecionado else 1) #borda do cartão
        icone=pygame.Rect(0,0,16,16)
        icone.center=(r.centerx,r.y + 16)
        desenhar_texto(superficie, self.classe.nome, (r.centerx, r.y + 32), YELLOW if selecionado else WHITE, 16, centralizado=True)
        
        fonte=pygame.font.Font(None, 14)
        linhas = [
            f"Vida: {self.classe.vida_maxima}",
            f"Velocidade: {int(self.classe.velocidade)}",
            f"Dano: {self.classe.ataque.get('dano',0)}"
        ]
        for i, texto in enumerate(linhas):
            imagem_texto = fonte.render(texto, True, (255, 255, 255))
            posicao = (r.x + 6, r.y + 46 + i * 12)
            tela.blit(imagem_texto, posicao)