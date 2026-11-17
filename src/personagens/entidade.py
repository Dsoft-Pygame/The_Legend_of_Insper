import pygame


class Entidade:
    """Tudo que aparece no mapa: tem posição, tamanho e cor, e sabe se desenhar."""

    def __init__(self, x, y, largura, altura, cor):
        self.posicao = pygame.Vector2(x, y)   # centro, em pixels do mapa
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.imagem = None                    # sem imagem, desenha um retângulo com a cor

    def retangulo(self):
        """O retângulo de colisão, em volta da posição."""
        retangulo = pygame.Rect(0, 0, self.largura, self.altura)
        retangulo.center = (round(self.posicao.x), round(self.posicao.y))
        return retangulo

    def imagem_atual(self):
        """A imagem que aparece agora. As classes filhas trocam este método para virar ou animar."""
        return self.imagem

    def desenhar(self, superficie, camera):
        retangulo = camera.para_tela(self.retangulo())
        imagem = self.imagem_atual()
        
        if imagem is None:
            pygame.draw.rect(superficie, self.cor, retangulo)
        else:
            superficie.blit(imagem, imagem.get_rect(center=retangulo.center))   # imagem no meio do retângulo