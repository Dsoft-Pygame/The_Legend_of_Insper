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

class Camera:
    def __init__(self, largura: int, altura: int, largura_mapa: int, altura_mapa: int, ): # define tamanho e posição da camera
        if largura <= 0 or altura <= 0:
            raise ValueError("O tamanho da câmera deve ser positivo.")

        self.largura = largura
        self.altura = altura

        self.x = 0.0
        self.y = 0.0

        self.mudar_mapa(largura_mapa, altura_mapa)

    def seguir(self, alvos): # camera segue os herois
        if not alvos:
            return

        centro_x = sum(alvo.x for alvo in alvos) / len(alvos)
        centro_y = sum(alvo.y for alvo in alvos) / len(alvos)

        self.x = centro_x - self.largura / 2
        self.y = centro_y - self.altura / 2

        self._limitar_ao_mapa()

    def para_tela(self, caixa: pygame.Rect) -> pygame.Rect:
        """Converte para a tela sem modificar a caixa original."""
        return caixa.move(-round(self.x), -round(self.y))

    def area_visivel(self) -> pygame.Rect:
        """Retorna o recorte em coordenadas do mapa."""
        return pygame.Rect(
            round(self.x),
            round(self.y),
            self.largura,
            self.altura,
        )

    def esta_visivel(self, caixa: pygame.Rect) -> bool:
        """Verifica se alguma parte da caixa aparece no recorte."""
        return self.area_visivel().colliderect(caixa)

    def mudar_mapa(self, largura: int, altura: int) -> None:
        """Atualiza as dimensões do mapa e reajusta a câmera."""
        if largura <= 0 or altura <= 0:
            raise ValueError("O tamanho do mapa deve ser positivo.")

        self.largura_mapa = largura
        self.altura_mapa = altura

        self._limitar_ao_mapa()

    def _limitar_ao_mapa(self): #trava a camera ao chegar na borda do mapa
        limite_x = max(0, self.largura_mapa - self.largura)
        limite_y = max(0, self.altura_mapa - self.altura)

        self.x = max(0.0, min(self.x, float(limite_x)))
        self.y = max(0.0, min(self.y, float(limite_y)))