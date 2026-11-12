import pygame

from personagens.entidade import Entidade

QUINA = 4   # pixels que o personagem desvia sozinho para entrar numa porta estreita


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
        """Anda um eixo de cada vez: o eixo que entraria na parede não anda.

        Andando reto contra a quina de uma porta, escorrega para o lado, como o
        MovimentoLivre da main, para não precisar acertar a porta no pixel.
        """
        passo = direcao * self.velocidade * dt
        andou_x = self.andar(pygame.Vector2(passo.x, 0), mapa)
        andou_y = self.andar(pygame.Vector2(0, passo.y), mapa)
        if not andou_x and passo.y == 0:
            self.contornar_quina(pygame.Vector2(passo.x, 0), pygame.Vector2(0, 1), mapa)
        if not andou_y and passo.x == 0:
            self.contornar_quina(pygame.Vector2(0, passo.y), pygame.Vector2(1, 0), mapa)

    def cabe(self, posicao, mapa):
        """True se o personagem cabe nessa posição sem entrar na parede."""
        retangulo = self.retangulo()
        retangulo.center = (round(posicao.x), round(posicao.y))
        return mapa.area_livre(retangulo)

    def andar(self, deslocamento, mapa):
        """Anda o deslocamento se couber. Devolve True se andou."""
        if not self.cabe(self.posicao + deslocamento, mapa):
            return False
        self.posicao += deslocamento
        return True

    def contornar_quina(self, frente, lado, mapa):
        """Bateu andando reto: procura o menor desvio para o lado, até QUINA pixels, que
        deixa dar o passo em frente, e escorrega para lá (no máximo um passo por quadro).
        """
        for desvio in range(1, QUINA + 1):
            for sentido in (-1, 1):
                if self.cabe(self.posicao + frente + lado * sentido * desvio, mapa):
                    self.andar(lado * sentido * min(desvio, frente.length()), mapa)
                    return

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
