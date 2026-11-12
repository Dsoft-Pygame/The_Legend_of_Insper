import pygame

from personagens.entidade import Entidade


class Personagem(Entidade):
    """Tudo que tem vida e anda pelo mapa sem atravessar parede (heróis e inimigos)."""

    def __init__(self, x, y, tamanho, cor, vida, velocidade):
        super().__init__(x, y, tamanho, tamanho, cor)
        self.vida = vida
        self.vida_maxima = vida
        self.velocidade = velocidade              # pixels por segundo
        self.direcao = pygame.Vector2(1, 0)       # para onde está olhando
        self.invulneravel = 0                     # segundos piscando depois de levar dano
        self.tempo_invulneravel = 0               # o herói usa 0.8

    def mover(self, direcao, dt, mapa):
        """Anda um eixo de cada vez: se entrou na parede, desfaz só aquele eixo."""
        passo = direcao * self.velocidade * dt
        self.posicao.x += passo.x
        if not mapa.area_livre(self.retangulo()):
            self.posicao.x -= passo.x
        self.posicao.y += passo.y
        if not mapa.area_livre(self.retangulo()):
            self.posicao.y -= passo.y

    def esta_vivo(self):
        return self.vida > 0

    def receber_dano(self, dano):
        """Tira vida, a não ser que ainda esteja piscando do último golpe."""
        if self.invulneravel > 0:
            return
        self.vida = max(0, self.vida - dano)
        self.invulneravel = self.tempo_invulneravel

    def desenhar(self, superficie, camera):
        if self.invulneravel > 0 and int(self.invulneravel * 10) % 2 == 0:
            return                                # pisca enquanto está invulnerável
        super().desenhar(superficie, camera)
