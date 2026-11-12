import pygame


class Entidade:
    """Tudo que aparece no mapa: tem posição, tamanho e cor, e sabe se desenhar."""

    def __init__(self, x, y, largura, altura, cor):
        self.posicao = pygame.Vector2(x, y)   # centro, em pixels do mapa
        self.largura = largura
        self.altura = altura
        self.cor = cor

    def retangulo(self):
        """O retângulo de colisão, em volta da posição."""
        retangulo = pygame.Rect(0, 0, self.largura, self.altura)
        retangulo.center = (round(self.posicao.x), round(self.posicao.y))
        return retangulo

    def desenhar(self, superficie, camera):
        pygame.draw.rect(superficie, self.cor, camera.para_tela(self.retangulo()))
