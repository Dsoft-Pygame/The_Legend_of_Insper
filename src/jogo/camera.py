import pygame

from settings import ALTURA_TELA, LARGURA_TELA


class Camera:
    """O pedaço do mapa que aparece na tela: segue o herói e para nas bordas do mapa."""

    def __init__(self, largura_mapa, altura_mapa):
        self.x = 0                        # canto de cima à esquerda do recorte, em pixels do mapa
        self.y = 0
        self.largura_mapa = largura_mapa
        self.altura_mapa = altura_mapa

    def seguir(self, posicao):
        """Põe a posição no meio da tela, sem mostrar nada fora do mapa."""
        self.x = self.limitar(posicao.x - LARGURA_TELA / 2, self.largura_mapa - LARGURA_TELA)
        self.y = self.limitar(posicao.y - ALTURA_TELA / 2, self.altura_mapa - ALTURA_TELA)

    def limitar(self, valor, maximo):
        if maximo < 0:                    # mapa menor que a tela: fica centralizado
            return maximo / 2
        return max(0, min(valor, maximo))

    def para_tela(self, retangulo):
        """Leva um retângulo do mapa para o lugar dele na tela."""
        return retangulo.move(-round(self.x), -round(self.y))

    def esta_visivel(self, retangulo):
        return self.para_tela(retangulo).colliderect(pygame.Rect(0, 0, LARGURA_TELA, ALTURA_TELA))
