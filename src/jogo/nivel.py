import pygame

from jogo.mapa import Mapa
from settings import BLACK, BROWN, DARK_GRAY, GRAY, YELLOW


class Nivel:
    """Um nível em andamento: o mapa, o herói, os inimigos e os projéteis.

    A cada quadro faz todo mundo andar, resolve os golpes e tira quem morreu.
    """

    def __init__(self, nome, arquivo, heroi):
        self.nome = nome
        self.mapa = Mapa(arquivo)
        self.heroi = heroi
        self.heroi.posicao = pygame.Vector2(self.mapa.inicio_heroi)
        self.inimigos = []                # como na main, começa vazio: criar os inimigos do mapa é a T51
        self.projeteis = []
        self.tempo = 0                    # segundos neste nível (a saída pisca com ele)

    def atualizar(self, dt):
        self.tempo += dt
        self.heroi.atualizar(dt, self.mapa)          # 1. o herói anda
        for inimigo in self.inimigos:                # 2. cada inimigo pensa e anda
            self.projeteis.extend(inimigo.atualizar(dt, self.heroi, self.mapa))
        self.mover_projeteis(dt)                     # 3. os projéteis andam
        self.aplicar_acertos()                       # 4. projétil que encosta dá dano
        self.aplicar_contato()                       # 5. inimigo encostado no herói dá dano
        self.remover_mortos()                        # 6. quem morreu sai do nível

    def mover_projeteis(self, dt):
        """Os projéteis andam e somem os que bateram na parede ou acabaram o tempo."""
        restantes = []
        for projetil in self.projeteis:
            projetil.atualizar(dt)
            if not projetil.acabou(self.mapa):
                restantes.append(projetil)
        self.projeteis = restantes

    def aplicar_acertos(self):
        """Projétil do herói dá dano nos inimigos, e projétil de inimigo dá dano no herói.

        Cada projétil acerta cada alvo uma vez só. O que não atravessa some no primeiro acerto.
        """
        restantes = []
        for projetil in self.projeteis:
            alvos = self.inimigos
            if projetil.dono == "inimigo":
                alvos = [self.heroi]
            sumiu = False
            for alvo in alvos:
                if not sumiu and projetil.pode_acertar(alvo):
                    alvo.receber_dano(projetil.dano)
                    projetil.ja_acertou.append(alvo)
                    if not projetil.atravessa:
                        sumiu = True          # flecha e bola de fogo param no primeiro que acertam
            if not sumiu:
                restantes.append(projetil)
        self.projeteis = restantes

    def aplicar_contato(self):
        """Inimigo encostado no herói dá dano. Depois de um golpe o herói fica piscando
        (invulnerável), então o dano não se repete a cada quadro.
        """
        for inimigo in self.inimigos:
            if inimigo.esta_vivo() and inimigo.retangulo().colliderect(self.heroi.retangulo()):
                self.heroi.receber_dano(inimigo.dano_contato)

    def remover_mortos(self):
        """Os inimigos sem vida saem do nível. Somar os pontos deles é a T51."""
        vivos = []
        for inimigo in self.inimigos:
            if inimigo.esta_vivo():
                vivos.append(inimigo)
        self.inimigos = vivos

    def esta_limpo(self):
        """Sem inimigos, a saída abre."""
        return len(self.inimigos) == 0

    def heroi_na_saida(self):
        """True quando o herói encosta na saída aberta. Passar de nível com isso é a T51."""
        if self.mapa.saida is None or not self.esta_limpo():
            return False
        return self.heroi.retangulo().colliderect(self.mapa.saida)

    def desenhar(self, superficie, camera):
        superficie.fill(BLACK)
        chao = pygame.Rect(0, 0, self.mapa.largura, self.mapa.altura)
        pygame.draw.rect(superficie, DARK_GRAY, camera.para_tela(chao))
        for parede in self.mapa.paredes:
            if camera.esta_visivel(parede):
                pygame.draw.rect(superficie, GRAY, camera.para_tela(parede))

        if self.mapa.saida is not None:
            cor_saida = BROWN
            if self.esta_limpo() and int(self.tempo * 4) % 2 == 0:
                cor_saida = YELLOW                   # aberta, ela pisca
            pygame.draw.rect(superficie, cor_saida, camera.para_tela(self.mapa.saida))

        for inimigo in self.inimigos:
            inimigo.desenhar(superficie, camera)
        for projetil in self.projeteis:
            projetil.desenhar(superficie, camera)
        self.heroi.desenhar(superficie, camera)
