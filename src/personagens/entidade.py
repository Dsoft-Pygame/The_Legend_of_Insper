"""Classe Entidade: a base de tudo que existe dentro de um nível.

O que é:
    Personagens e projéteis têm coisas em comum: um id, uma posição no
    mapa e um tamanho. Isso fica aqui e as outras herdam.

    A Entidade NÃO tem imagem e NÃO se desenha. Ela guarda só uma chave de
    aparência ("slime", "mago", "flecha"); quem transforma essa chave em
    cor ou sprite é o render (render/aparencias.py). Assim dá para trocar
    toda a arte sem mexer em nenhuma entidade.

Atributos:
    - id: EntidadeId.
    - posicao: pygame.Vector2. Centro, em pixels do mapa (não da tela).
    - posicao_anterior: pygame.Vector2. Onde estava no fim do tick
      anterior. A lógica roda a 20 ticks por segundo e a tela a 60; o
      render desenha entre posicao_anterior e posicao para o movimento
      ficar liso nos 3 quadros de cada tick.
    - tamanho: pygame.Vector2. Largura e altura da caixa de colisão.
    - aparencia: str. Chave para o render.

Métodos:
    - guardar_posicao() -> None: copia posicao para posicao_anterior. O
      Nivel chama para todas as entidades no começo de cada tick.
    - colocar_em(posicao: pygame.Vector2) -> None: muda posicao e
      posicao_anterior juntas. Usado ao nascer e ao começar um nível
      novo, para o render não desenhar a entidade deslizando do lugar
      antigo até o novo.

Propriedades:
    - caixa -> pygame.Rect: retângulo de colisão montado a partir de
      posicao e tamanho (sempre a posição do tick, nunca a interpolada).

Herdam dela: Personagem e Projetil.
"""

import pygame
from movimento.movimento import caixa_em
from personagens.tipos import EntidadeId



class Entidade:
  
  def __init__(self, posicao: pygame.Vector2, tamanho: pygame.Vector2, aparencia: str):
    self.id: EntidadeId = 0                          # o Nivel dá o id de verdade
    self.posicao = pygame.Vector2(posicao)           # cópia
    self.posicao_anterior = pygame.Vector2(posicao)  # OUTRA cópia, separada
    self.tamanho = pygame.Vector2(tamanho)
    self.aparencia = aparencia                       # ex.: "slime"
  
  def guardar_posicao(self) -> None:
    self.posicao_anterior = pygame.Vector2(self.posicao)

  def colocar_em(self, posicao: pygame.Vector2) -> None: # teleporta para a nova posição
    self.posicao = pygame.Vector2(posicao)
    self.posicao_anterior = pygame.Vector2(posicao)

  @property
  def caixa(self) -> pygame.Rect: # retangulo de colisão (o mesmo que o movimento usa)
    return caixa_em(self.posicao, self.tamanho)