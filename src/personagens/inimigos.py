"""Os inimigos do jogo: Slime, Esqueleto, Morcego e o chefe, o Dragão Ancião."""

import random
import pygame

from ui import carregar_imagem
from personagens.personagem import Personagem
from personagens.projetil import Projetil
from settings import CYAN, PINK, PURPLE, RED, WHITE


class Inimigo(Personagem):
    """Um monstro: anda à toa até o herói chegar perto e então vai atrás dele.

    Dá dano quando encosta no herói e vale pontos quando morre. Como na main, ainda
    não aparece no nível: criar os inimigos das letras do mapa é a T51.
    """

    def __init__(self, x, y, tamanho, cor, vida, velocidade, nome, dano_contato, pontos, raio_alerta):
        """Guarda o nome, o dano de contato, os pontos e o raio de alerta, e sorteia em que quadro da
        animação começa.
        """
        super().__init__(x, y, tamanho, cor, vida, velocidade)
        self.nome = nome
        self.dano_contato = dano_contato   # dano quando encosta no herói
        self.pontos = pontos               # quanto vale quando morre
        self.raio_alerta = raio_alerta     # a partir de quantos pixels começa a perseguir
        self.tempo_vagando = 1.5           # segundos andando para um lado antes de sortear outro
        self.tempo_sorteio = 0             # quanto falta para sortear de novo
        self.direcao_vagando = pygame.Vector2(0, 0)
        self.quadros = []                  # imagens da animação, em ordem (vazio: imagem parada)
        self.tempo_quadro = 0.15           # segundos em cada quadro
        self.tempo_animacao = random.uniform(0, 1)   # cada um começa num quadro, para não mexerem juntos

    def carregar_quadros(self, nome, ordem):
        """Carrega a animação: carregar_quadros("slime", [1, 2]) usa slime_1.png e slime_2.png.
        Se faltar algum PNG, fica sem animação (e sem imagem, desenha o quadrado).
        """
        quadros = []
        for numero in ordem:
            quadros.append(carregar_imagem(nome + "_" + str(numero) + ".png"))
        if None not in quadros:
            self.quadros = quadros
            self.imagem = quadros[0]

    def animar(self, dt):
        """Passa o tempo da animação e troca a imagem pelo quadro da vez."""
        if len(self.quadros) == 0:
            return
        self.tempo_animacao += dt
        self.imagem = self.quadros[int(self.tempo_animacao / self.tempo_quadro) % len(self.quadros)]

    def atualizar(self, dt, heroi, mapa):
        """Persegue o herói se ele estiver perto; senão, vaga. Devolve os projéteis que criou."""
        caminho = heroi.posicao - self.posicao
        if 0 < caminho.length() <= self.raio_alerta:
            self.direcao = caminho.normalize()
            self.mover(self.direcao, dt, mapa)
        else:
            self.vagar(dt, mapa)
        return []                          # os inimigos comuns não atiram

    def vagar(self, dt, mapa):
        """Anda à toa: de tempos em tempos sorteia uma direção ou fica parado."""
        self.tempo_sorteio -= dt
        if self.tempo_sorteio <= 0:
            self.tempo_sorteio = self.tempo_vagando
            if random.random() < 0.3:      # 30% das vezes fica parado
                self.direcao_vagando = pygame.Vector2(0, 0)
            else:
                self.direcao_vagando = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
        if self.direcao_vagando.length() > 0:
            self.mover(self.direcao_vagando * 0.5, dt, mapa)   # vagando, anda na metade da velocidade


class Slime(Inimigo):
    """Lento e fraco: o inimigo do primeiro andar."""

    def __init__(self, x, y):
        """Slime: 25 de vida, lento (60 px/s), quica no lugar."""
        super().__init__(x, y, 24, CYAN, 25, 60, "Slime", 10, 50, 160)
        self.carregar_quadros("slime", [1, 2, 1, 3])   # normal, achata, normal, estica: quica no lugar
        self.tempo_quadro = 0.2

class Esqueleto(Inimigo):
    """Mais forte e mais rápido que o slime, e percebe o herói de mais longe."""

    def __init__(self, x, y):
        """Esqueleto: 36 de vida, 110 px/s, percebe o herói a 224 px e anda trocando as pernas."""
        super().__init__(x, y, 24, WHITE, 36, 110, "Esqueleto", 15, 80, 224)
        self.resistencia = 0.3             # mais pesado que o slime e o morcego: voa um pouco menos
        self.tempo_vagando = 1
        self.carregar_quadros("esqueleto", [1, 2])     # anda trocando as pernas
        self.tempo_quadro = 0.25

class Morcego(Inimigo):
    """Rápido e frágil. Persegue em zigue-zague"""

    def __init__(self, x, y):
        """Morcego: 10 de vida, o mais rápido (180 px/s), bate as asas e guarda o lado do zigue-zague."""
        super().__init__(x, y, 24, PINK, 10, 180, "Morcego", 5, 70, 240)
        self.tempo_vagando = 1
        self.tempo_desvio = 0.4            # segundos desviando para o mesmo lado
        self.forca_desvio = 0.8            # quanto desvia: 0 iria reto até o herói
        self.lado = 1                      # 1 desvia para um lado, -1 para o outro
        self.falta_trocar = self.tempo_desvio
        self.carregar_quadros("morcego", [1, 2, 3, 2])  # asas em cima, no meio, embaixo, no meio
        self.tempo_quadro = 0.08
        
    def atualizar(self, dt, heroi, mapa):
        """Perto do herói, vai até ele desviando para um lado e para o outro (zigue-zague); longe, vaga
        como os outros.
        """
        caminho = heroi.posicao - self.posicao
        if caminho.length() == 0 or caminho.length() > self.raio_alerta:
            return super().atualizar(dt, heroi, mapa)
        self.falta_trocar -= dt
        if self.falta_trocar <= 0:
            self.lado = -self.lado         # troca o lado do desvio
            self.falta_trocar = self.tempo_desvio
        frente = caminho.normalize()
        lado = pygame.Vector2(-frente.y, frente.x) * self.lado * self.forca_desvio
        self.direcao = (frente + lado).normalize()
        self.mover(self.direcao, dt, mapa)
        return []


class Dragao(Inimigo):
    """O chefe do Topo da Torre, maior que os outros. 2 fases"""

    def __init__(self, x, y):
        """O chefe: 360 de vida, 48 px, quase não é empurrado; guarda as recargas do tiro, do anel de fogo
        e do cálculo do caminho.
        """
        super().__init__(x, y, 48, PURPLE, 360, 90, "Dragão Ancião", 25, 2000, 480)
        self.resistencia = 0.85            # o chefe quase não sai do lugar
        self.distancia_tiro = 128          # cospe fogo quando o herói está mais perto que isso
        self.tempo_tiro = 1                # segundos entre uma bola de fogo e outra
        self.tempo_anel = 3                # segundos entre um anel de fogo e outro (fase 2)
        self.recarga_tiro = 0
        self.recarga_anel = self.tempo_anel
        self.tempo_rota = 0.25             # segundos entre um cálculo do caminho e outro
        self.recarga_rota = 0
        self.passo = None                  # próximo ponto do caminho quando há parede no meio
        self.imagem = carregar_imagem("dragao.png")
        self.tempo_aviso = 0.5             # segundos piscando vermelho antes do anel sair

    def fase(self): #2 fases
        """1 enquanto tem mais da metade da vida; 2 depois disso."""
        if self.vida > self.vida_maxima / 2:
            return 1
        return 2

    def atualizar(self, dt, heroi, mapa):
        """Olha para o herói e anda até ele contornando as paredes. Fase 1: metade da velocidade. Fase 2:
        velocidade cheia e um anel de 12 bolas de fogo a cada tempo_anel segundos. Nas duas, cospe fogo
        quando o herói está perto. Devolve as bolas de fogo criadas.
        """
        self.recarga_tiro = max(0, self.recarga_tiro - dt)
        caminho = heroi.posicao - self.posicao
        if caminho.length() == 0:
            return []
        self.direcao = caminho.normalize()            # olha e atira sempre na direção do herói
        rumo = self.rumo(dt, heroi, mapa)              # mas anda contornando as paredes
        bolas = []
        if self.fase() == 1:
            self.mover(rumo * 0.5, dt, mapa)           # fase 1: metade da velocidade
        else:
            self.mover(rumo, dt, mapa)
            self.recarga_anel -= dt
            if self.recarga_anel <= 0:
                self.recarga_anel = self.tempo_anel
                for i in range(12):                       # uma bola a cada 30 graus
                    bolas.append(self.bola_de_fogo(self.direcao.rotate(i * 30), 200))
        if caminho.length() <= self.distancia_tiro and self.recarga_tiro == 0:
            self.recarga_tiro = self.tempo_tiro
            bolas.append(self.bola_de_fogo(self.direcao, 240))
        return bolas

    def rumo(self, dt, heroi, mapa):
        """Direção em que o Dragão anda. Com o caminho livre, vai reto no herói; com parede no
        meio, segue o mapa.proximo_passo(), recalculado a cada tempo_rota segundos, para não
        ficar empurrando a parede.
        """
        if self.cabe_no_caminho(heroi.posicao, mapa):
            self.passo = None
            return self.direcao
        self.recarga_rota -= dt
        chegou = self.passo is not None and (self.passo - self.posicao).length() < 4
        if self.recarga_rota <= 0 or chegou:
            self.recarga_rota = self.tempo_rota
            self.passo = mapa.proximo_passo(self.posicao, heroi.posicao, self.largura)
        if self.passo is None or (self.passo - self.posicao).length() == 0:
            return pygame.Vector2(0, 0)                # não tem como chegar mais perto: espera
        return (self.passo - self.posicao).normalize()

    def cabe_no_caminho(self, destino, mapa):
        """True se o corpo inteiro do Dragão passa em linha reta até destino (confere a cada 8 px)."""
        caminho = destino - self.posicao
        passos = int(caminho.length() // 8) + 1
        for i in range(passos + 1):
            corpo = self.retangulo()
            ponto = self.posicao + caminho * (i / passos)
            corpo.center = (round(ponto.x), round(ponto.y))
            if not mapa.area_livre(corpo):
                return False
        return True

    def bola_de_fogo(self, direcao, rapidez):
        """Cria uma bola de fogo do Dragão nessa direção e rapidez (dono "inimigo")."""
        return Projetil(self.posicao, direcao * rapidez, tamanho=16, cor=RED, dano=15, duracao=2, dono="inimigo",
                        imagem="bola_fogo.png")

    def avisando_anel(self): # avisa que o anel de fogo sera lançado
        """True no meio segundo antes do anel de fogo sair (só na fase 2)."""
        return self.fase() == 2 and self.recarga_anel <= self.tempo_aviso

    def piscando_vermelho(self): #pisca vermelho
        """Avisando o anel, fica vermelho num décimo de segundo e normal no outro."""
        return self.avisando_anel() and int(self.recarga_anel * 10) % 2 == 0

    def imagem_atual(self):
        """Antes do anel de fogo, pisca vermelho para o herói ter tempo de se afastar."""
        imagem = super().imagem_atual()
        if imagem is None or not self.piscando_vermelho():
            return imagem
        vermelha = imagem.copy()
        vermelha.fill((255, 80, 80), special_flags=pygame.BLEND_RGB_MULT)   # tira o verde e o azul
        vermelha.fill((90, 0, 0), special_flags=pygame.BLEND_RGB_ADD)       # e soma vermelho
        return vermelha

    def desenhar(self, superficie, camera):
        """Sem o PNG, o quadrado roxo também fica vermelho no aviso."""
        self.cor = PURPLE
        if self.piscando_vermelho():
            self.cor = RED
        super().desenhar(superficie, camera)
