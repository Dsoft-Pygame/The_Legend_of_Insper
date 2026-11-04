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
import pygame
import math
from typing import Sequence
from settings import LARGURA_TELA, ALTURA_TELA


def limitar(valor: float, maximo: float) -> float:
    if maximo < 0:
        return maximo / 2
    return max(0.0, min(valor, maximo))

class Camera:
    def __init__(self, largura: int= LARGURA_TELA, altura: int= ALTURA_TELA): # define tamanho e posição da camera
        self.x = 0.0
        self.y = 0.0
        # tamanho do recorte (a tela do jogo, 240x160)
        self.largura = largura
        self.altura = altura
        # tamanho do mapa completo, para não mostrar nada fora do mapa
        self.largura_mapa = 0
        self.altura_mapa = 0

    def mudar_mapa(self, largura: int, altura: int): #tamanho do mapa completo
        self.largura_mapa = largura
        self.altura_mapa = altura

    def seguir(self, alvos: Sequence[pygame.Vector2]) -> None: # segue o ponto medio dos alvos, sejam eles quantos forem
        if not alvos:
            return

        centro = pygame.Vector2(0, 0)
        for alvo in alvos:
            centro += alvo
        centro /= len(alvos)

        self.x = centro.x - self.largura / 2
        self.y = centro.y - self.altura / 2
        # Impede que a câmera ultrapasse as bordas do mapa.
        self.x = limitar(self.x, self.largura_mapa - self.largura)
        self.y = limitar(self.y, self.altura_mapa - self.altura)

    def para_tela(self, caixa: pygame.Rect) -> pygame.Rect: #gera o novo retangulo da camera, evita que a camera fiquei no meio de 2 pixeis
        return caixa.move(-round(self.x), -round(self.y))
    
    def area_visivel(self) -> pygame.Rect:
        return pygame.Rect(math.floor(self.x), math.floor(self.y), self.largura + 1, self.altura + 1)
    
    def esta_visivel(self, caixa: pygame.Rect) -> bool:
        return self.area_visivel().colliderect(caixa)