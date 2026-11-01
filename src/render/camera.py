"""Classe Camera: mostra só o pedaço do nível em volta dos heróis.

O que é:
    Os níveis são maiores que a tela, como nos Pokémon antigos. A tela
    mostra só um "recorte" do mapa, e esse recorte acompanha os heróis
    enquanto eles andam. A Camera é quem sabe onde esse recorte está.

    Fica no render, e não no jogo: é só um jeito de olhar, e a partida
    funciona igual sem câmera nenhuma.

Atributos:
    - x, y: float. Canto superior esquerdo do recorte, em pixels do mapa.
    - largura, altura: int. Tamanho do recorte (a tela do jogo, 240x160).
    - largura_mapa, altura_mapa: int. Para não mostrar nada fora do mapa.

Métodos:
    - seguir(alvos: Sequence[pygame.Vector2]) -> None: centraliza o recorte
      no ponto médio dos alvos (os heróis vivos; com um jogador, é ele).
      Os alvos são as posições de desenho (já interpoladas), então a
      câmera anda lisa a 60 quadros por segundo, e não aos pulos de 20.
      Perto das bordas do mapa, a câmera para e quem anda na tela é o herói.
    - para_tela(caixa: pygame.Rect) -> pygame.Rect: posição no mapa menos
      x, y da câmera, arredondados para pixel inteiro (senão os ladrilhos
      tremem quando a câmera está entre dois pixels).
    - area_visivel() -> pygame.Rect: o recorte, em pixels do mapa (para
      pedir ao Mapa só os ladrilhos visíveis).
    - esta_visivel(caixa: pygame.Rect) -> bool: para não desenhar o que
      está fora da tela.
    - mudar_mapa(largura: int, altura: int) -> None: ao trocar de nível,
      porque cada nível pode ter um tamanho diferente.

Co-op: com dois heróis longe um do outro, a câmera fica no meio. Se um dia
precisar de tela dividida, são duas Cameras e dois desenhos, sem mudar
nada no jogo.

O HUD não usa a câmera: ele fica sempre no mesmo lugar da tela.

Quem usa: RenderizadorNivel.
"""
