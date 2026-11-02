"""Interfaces Mapa e CarregadorMapa (typing.Protocol): a estrutura do nível.

O que é:
    Tudo que o resto do jogo sabe sobre o mapa passa por estas perguntas.
    Personagens, movimento, IA e combate não sabem se o mapa é uma grade
    de tiles, um desenho do Tiled ou algo gerado na hora. Trocar o sistema
    de mapa inteiro = escrever outro Mapa e outro CarregadorMapa.

Mapa (interface; todos os métodos só leem):
    - largura, altura: int. Tamanho em pixels.
    - area_livre(caixa: pygame.Rect) -> bool: True se a caixa não encosta
      em nada sólido nem sai do mapa. É a colisão do jogo inteiro.
    - surgimentos(marcador: str) -> list[pygame.Vector2]: onde as coisas
      aparecem ("heroi", "inimigo", "chefe").
    - saida() -> pygame.Rect | None: a porta ou escada do nível.
    - ladrilhos_em(area: pygame.Rect) -> Iterator[tuple[pygame.Rect, str]]:
      as partes do mapa dentro dessa área, cada uma com uma chave de
      aparência ("chao", "parede"). Só o render usa.

CarregadorMapa (interface):
    - carregar(origem: str) -> Mapa: lê, gera ou monta o mapa. A origem é
      o que o tema diz (ex.: "mapas/nivel_1.txt").

Implementações: MapaTiles, criado pelo CarregadorTexto.
Quem usa: Nivel, Mundo, movimento/, ia/ (pela Visao), jogo/combate.py e
render/.
"""

from typing import Iterator, Protocol
import pygame

class Mapa(Protocol):
  largura: int  # em pixels
  altura: int # em pixels

  def area_livre(self, caixa: pygame.Rect) -> bool: ...

  def surgimentos(self, marcador: str) -> list[pygame.Vector2]: ...

  def saida(self) -> pygame.Rect | None: ...

  def ladrilhos_em(self, area: pygame.Rect) -> Iterator[tuple[pygame.Rect, str]]: ...

class CarregadorMapa(Protocol):
  def carregar(self, origem: str) -> Mapa: ...
