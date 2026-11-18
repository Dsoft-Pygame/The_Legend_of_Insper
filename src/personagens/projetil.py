import pygame

from personagens.entidade import Entidade
from settings import YELLOW
from ui import carregar_imagem


class Projetil(Entidade):
    """Tudo que voa e dá dano, como flecha e bola de fogo. Some na parede ou quando o tempo acaba."""

    def __init__(self, posicao, velocidade, tamanho, cor, dano, duracao, dono, imagem=None, empurrao=0):
        super().__init__(posicao.x, posicao.y, tamanho, tamanho, cor)
        if imagem is not None:
            self.imagem = carregar_imagem(imagem)       # o desenho aponta para a direita
        self.velocidade = pygame.Vector2(velocidade)   # direção e rapidez, em pixels por segundo
        self.dano = dano
        self.duracao = duracao                         # segundos até sumir
        self.dono = dono                               # "heroi" ou "inimigo": não acerta o próprio lado
        self.atravessa = False                         # True: acerta todos que encostar
        self.ja_acertou = []                           # quem já levou dano deste projétil
        self.empurrao = empurrao                       # força do knockback, em pixels por segundo

    def atualizar(self, dt):
        self.posicao += self.velocidade * dt
        self.duracao -= dt

    def acabou(self, mapa):
        return self.duracao <= 0 or self.bateu_na_parede(mapa)

    def pode_acertar(self, alvo, mapa):
        """True se encostou num alvo vivo que ainda não levou dano deste projétil."""
        return (alvo.esta_vivo() and alvo not in self.ja_acertou
                and self.retangulo().colliderect(alvo.retangulo()))

    def bateu_na_parede(self, mapa):
        return not mapa.area_livre(self.retangulo())

    def direcao_empurrao(self, alvo):
        """Para onde o alvo é empurrado: para o lado em que o projétil está voando."""
        if self.velocidade.length() == 0:
            return pygame.Vector2(0, 0)
        return self.velocidade.normalize()

    def imagem_atual(self):
        """Gira o desenho para o lado em que o projétil está voando."""
        imagem = super().imagem_atual()
        if imagem is None or self.velocidade.length() == 0:
            return imagem
        angulo = pygame.Vector2(1, 0).angle_to(self.velocidade)
        return pygame.transform.rotate(imagem, -angulo)   # o rotate gira ao contrário do eixo y da tela


class Golpe(Projetil):
    """Golpe corpo a corpo: fica parado e some sozinho. Com atravessa=True acerta todos
    na área; sem, para no primeiro que acerta.
    """

    def __init__(self, posicao, tamanho, dano, duracao, atravessa, origem, empurrao=0):
        super().__init__(posicao, (0, 0), tamanho, YELLOW, dano, duracao, "heroi", empurrao=empurrao)
        self.atravessa = atravessa
        self.origem = pygame.Vector2(origem)           # de onde o golpe saiu (o centro do herói)

    def pode_acertar(self, alvo, mapa):
        """Além de encostar, o alvo tem que estar do mesmo lado da parede que o herói:
        o golpe não atravessa parede.
        """
        return super().pode_acertar(alvo, mapa) and mapa.linha_livre(self.origem, alvo.posicao)

    def direcao_empurrao(self, alvo):
        """O golpe parado empurra para longe do herói que bateu."""
        caminho = alvo.posicao - self.origem
        if caminho.length() == 0:
            return pygame.Vector2(0, 0)
        return caminho.normalize()

    def bateu_na_parede(self, mapa):
        return False                                   # pode encostar na parede sem sumir
