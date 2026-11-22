"""Os heróis que o jogador escolhe: Mago, Arqueiro e Bárbaro."""

import pygame

from personagens.personagem import Personagem
from personagens.projetil import Golpe, Projetil
from settings import BLUE, GREEN, ORANGE, RED, WHITE
from ui import carregar_imagem

class Heroi(Personagem):
    """O personagem do jogador: anda com WASD, ataca com ESPAÇO e usa o especial com o SHIFT esquerdo.

    Cada classe filha muda os números e troca os métodos atacar e especial.
    """

    def __init__(self, x, y, cor, vida, velocidade, nome, descricao):
        """Guarda o nome, a descrição e os tempos de ataque e de especial. Cada classe filha troca os
        números.
        """
        super().__init__(x, y, 24, cor, vida, velocidade)   # 24 px: cabe folgado num corredor de 32
        self.nome = nome
        self.descricao = descricao
        self.tempo_invulneravel = 0.8
        self.dano = 0                      # dano do ataque normal (aparece no cartão da classe)
        self.tempo_ataque = 0.5            # segundos entre um ataque e outro
        self.tempo_especial = 8            # segundos entre um especial e outro (cada classe tem o seu)
        self.duracao_especial = 1          # segundos que os projéteis do especial ficam na tela
        self.empurrao_ataque = 0           # knockback dos ataques, em pixels por segundo (cada classe tem o seu)
        self.recarga_ataque = 0            # quanto falta para poder atacar de novo
        self.recarga_especial = 0

    def atualizar(self, dt, mapa):
        """Anda com WASD (na diagonal, com a mesma velocidade) e diminui as recargas e o tempo piscando."""
        teclas = pygame.key.get_pressed()
        direcao = pygame.Vector2(0, 0)
        if teclas[pygame.K_a]:
            direcao.x -= 1
        if teclas[pygame.K_d]:
            direcao.x += 1
        if teclas[pygame.K_w]:
            direcao.y -= 1
        if teclas[pygame.K_s]:
            direcao.y += 1
        if direcao.length() > 0:
            self.direcao = direcao.normalize()   # na diagonal não fica mais rápido
            self.mover(self.direcao, dt, mapa)
        self.recarga_ataque = max(0, self.recarga_ataque - dt)
        self.recarga_especial = max(0, self.recarga_especial - dt)
        self.invulneravel = max(0, self.invulneravel - dt)

    def usar_ataque(self):
        """A TelaJogo chama quando aperta ESPAÇO. Devolve a lista de projéteis criados."""
        if self.recarga_ataque > 0:
            return []
        self.recarga_ataque = self.tempo_ataque
        return self.atacar()

    def usar_especial(self):
        """A TelaJogo chama quando aperta o SHIFT esquerdo."""
        if self.recarga_especial > 0:
            return []
        self.recarga_especial = self.tempo_especial
        return self.especial()

    def curar(self, quantidade):
        """Devolve vida, sem passar da vida máxima."""
        self.vida = min(self.vida_maxima, self.vida + quantidade)

    def especial_pronto(self):
        """True quando o especial já recarregou (o HUD mostra ESPECIAL PRONTO)."""
        return self.recarga_especial == 0

    def carga_especial(self):
        """Quanto o especial já recarregou, de 0 (acabou de usar) até 1 (pronto)."""
        return 1 - self.recarga_especial / self.tempo_especial

    def atacar(self):
        """O ataque normal. Devolve a lista de projéteis; cada classe filha troca este método."""
        return []                          # cada classe troca este método

    def especial(self):
        """O ataque especial. Devolve a lista de projéteis; cada classe filha troca este método."""
        return []                          # e este também


class Mago(Heroi):
    """Bola de fogo lenta e forte. Especial: anel com 8 bolas de fogo."""

    def __init__(self, x, y):
        """Mago: 60 de vida, 120 px/s, 25 de dano, especial a cada 9 s. O desenho olha para a esquerda."""
        super().__init__(x, y, BLUE, 60, 120, "Mago", "Frágil, mas com dano alto à distância.")
        self.dano = 25
        self.tempo_ataque = 0.6
        self.tempo_especial = 9
        self.duracao_especial = 1
        self.empurrao_ataque = 300         # bola de fogo pesada: empurra bem
        self.imagem = carregar_imagem("mago.png")
        self.desenho_olha_esquerda = True  # o mago.png foi desenhado olhando para a esquerda

    def atacar(self):
        """Uma bola de fogo na direção em que o Mago olha."""
        velocidade = self.direcao * 180
        bola = Projetil(self.posicao, velocidade, tamanho=16, cor=RED, dano=self.dano, duracao=1.5, dono="heroi",
                        imagem="bola_fogo.png", empurrao=self.empurrao_ataque)
        return [bola]

    def especial(self):
        """Oito bolas de fogo em anel, uma a cada 45 graus."""
        bolas = []
        for i in range(8):                 # uma bola a cada 45 graus
            velocidade = self.direcao.rotate(i * 45) * 180
            bola = Projetil(self.posicao, velocidade, tamanho=16, cor=RED, dano=20, duracao=self.duracao_especial,
                            dono="heroi", imagem="bola_fogo.png", empurrao=self.empurrao_ataque)
            bolas.append(bola)
        return bolas


class Arqueiro(Heroi):
    """Flecha rápida. Especial: cinco flechas em leque, com a menor recarga das classes."""

    def __init__(self, x, y):
        """Arqueiro: 80 de vida, 200 px/s, 10 de dano, especial a cada 5 s."""
        super().__init__(x, y, GREEN, 80, 200, "Arqueiro", "Ágil, ataca rápido de longe.")
        self.dano = 10
        self.tempo_ataque = 0.3
        self.tempo_especial = 5
        self.duracao_especial = 1.2        # as flechas do especial vão mais longe que as normais
        self.empurrao_ataque = 144         # flecha leve: empurra pouco
        self.imagem = carregar_imagem("arqueiro.png")

    def atacar(self):
        """Uma flecha rápida na direção em que o Arqueiro olha."""
        velocidade = self.direcao * 400
        flecha = Projetil(self.posicao, velocidade, tamanho=8, cor=WHITE, dano=self.dano, duracao=1, dono="heroi",
                          imagem="flecha.png", empurrao=self.empurrao_ataque)
        return [flecha]

    def especial(self):
        """Cinco flechas em leque, de 12 em 12 graus."""
        flechas = []
        for angulo in (-24, -12, 0, 12, 24):
            velocidade = self.direcao.rotate(angulo) * 400
            flecha = Projetil(self.posicao, velocidade, tamanho=8, cor=WHITE, dano=15,
                              duracao=self.duracao_especial, dono="heroi", imagem="flecha.png",
                              empurrao=self.empurrao_ataque)
            flechas.append(flecha)
        return flechas


class Barbaro(Heroi):
    """Machadada logo na frente. Especial: giro que acerta todos em volta."""

    def __init__(self, x, y):
        """Bárbaro: 160 de vida, 150 px/s, 40 de dano, especial a cada 7 s. Carrega os quadros da machadada
        e do giro.
        """
        super().__init__(x, y, ORANGE, 160, 150, "Bárbaro", "Resistente, luta de perto.")
        self.dano = 40
        self.tempo_ataque = 0.5
        self.tempo_especial = 7
        self.duracao_especial = 0.3        # o giro fica pouco tempo na tela
        self.empurrao_ataque = 456         # machadada: a que empurra mais
        self.imagem = carregar_imagem("barbaro.png")
        self.quadros_corte = [carregar_imagem("corte_1.png"), carregar_imagem("corte_2.png"),
                              carregar_imagem("corte_3.png")]
        self.quadros_giro = [carregar_imagem("giro_1.png"), carregar_imagem("giro_2.png"),
                             carregar_imagem("giro_3.png"), carregar_imagem("giro_4.png")]
        self.tempo_corte = 0.2             # segundos da animação da machadada
        self.animacao = None               # "corte", "giro" ou None
        self.falta_animacao = 0            # segundos que faltam da animação
        self.duracao_animacao = 1

    def atacar(self):
        """Uma machadada logo na frente do Bárbaro, que para no primeiro inimigo, e começa a animação do
        corte.
        """
        centro = self.posicao + self.direcao * 30   # metade do herói (12) + metade do golpe (18)
        self.animar("corte", self.tempo_corte)
        return [Golpe(centro, tamanho=36, dano=self.dano, duracao=0.1, atravessa=False,
                      origem=self.posicao, empurrao=self.empurrao_ataque)]

    def especial(self):
        """Um giro que acerta todos até 56 px em volta e empurra mais longe, e começa a animação do giro."""
        tamanho = 24 + 2 * 56                       # o herói (24) mais 56 px de cada lado
        self.animar("giro", self.duracao_especial)
        return [Golpe(self.posicao, tamanho=tamanho, dano=25, duracao=self.duracao_especial,
                      atravessa=True, origem=self.posicao,
                      empurrao=self.empurrao_ataque * 1.2)]   # o giro joga mais longe

    def animar(self, nome, duracao):
        """Começa a animação "corte" ou "giro", que dura duracao segundos."""
        self.animacao = nome
        self.falta_animacao = duracao
        self.duracao_animacao = duracao

    def atualizar(self, dt, mapa):
        """Faz o que todo herói faz e passa o tempo da animação do golpe."""
        super().atualizar(dt, mapa)
        self.falta_animacao = max(0, self.falta_animacao - dt)
        if self.falta_animacao == 0:
            self.animacao = None

    def quadro(self, quadros):
        """O quadro da animação da vez, pelo tempo que já passou."""
        passou = 1 - self.falta_animacao / self.duracao_animacao      # de 0 a 1
        return quadros[min(len(quadros) - 1, int(passou * len(quadros)))]

    def imagem_atual(self):
        """Girando, o Bárbaro vira de um lado para o outro bem rápido."""
        imagem = super().imagem_atual()
        if imagem is not None and self.animacao == "giro" and int(self.falta_animacao / 0.05) % 2 == 0:
            imagem = pygame.transform.flip(imagem, True, False)
        return imagem

    def desenhar(self, superficie, camera):
        """O herói com a animação do golpe: o giro por baixo dele e o corte na frente,
        virado para onde ele olha. Na machadada ele também dá um passinho para a frente.
        """
        centro = camera.para_tela(self.retangulo()).center
        if self.animacao == "giro" and None not in self.quadros_giro:
            efeito = self.quadro(self.quadros_giro)
            superficie.blit(efeito, efeito.get_rect(center=centro))
        posicao = pygame.Vector2(self.posicao)
        if self.animacao == "corte":
            self.posicao = self.posicao + self.direcao * 3
        super().desenhar(superficie, camera)
        self.posicao = posicao
        if self.animacao == "corte" and None not in self.quadros_corte:
            angulo = pygame.Vector2(1, 0).angle_to(self.direcao)
            efeito = pygame.transform.rotate(self.quadro(self.quadros_corte), -angulo)
            superficie.blit(efeito, efeito.get_rect(center=centro))
