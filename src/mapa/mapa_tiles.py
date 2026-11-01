"""Classe MapaTiles (implementa Mapa): uma grade de tiles 16x16.

O que é:
    O mapa "como nos Pokémon antigos": maior que a tela, feito de
    quadradinhos. Cada célula é chão, parede ou saída. É a única classe do
    jogo que sabe que existe uma grade (como o Tabuleiro da simulação).

Atributos:
    - tamanho_tile: int. 16 pixels.
    - celulas: list[list[str]]. Tipo de cada célula ("chao", "parede",
      "saida").
    - pontos: dict[str, list[pygame.Vector2]]. Surgimentos por marcador.
    - largura, altura: int. Em pixels (colunas e linhas vezes o tile).

Métodos (os da interface Mapa):
    - area_livre(caixa: pygame.Rect) -> bool: confere só as células que a
      caixa toca.
    - surgimentos(marcador: str) -> list[pygame.Vector2].
    - saida() -> pygame.Rect | None.
    - ladrilhos_em(area: pygame.Rect) -> Iterator[tuple[pygame.Rect, str]]:
      só as células dentro da área (a câmera), para não desenhar o mapa
      todo a cada quadro.
    - celula_em(posicao: pygame.Vector2) -> str: ajuda interna.

Quem cria: CarregadorTexto.
"""
