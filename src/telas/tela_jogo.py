import pygame

from jogo.camera import Camera
from jogo.nivel import Nivel
from jogo.pontuacao import Pontuacao
from settings import ALTURA_TELA, GREEN, LARGURA_TELA, NIVEIS, RED, WHITE, YELLOW
from telas.tela import Tela
from ui import desenhar_barra, desenhar_texto, fonte


class TelaJogo(Tela):
    """Onde se joga: carrega o nível, passa os ataques para o herói e faz a câmera seguir,
    e leva para o próximo nível quando o herói chega na saída.
    """

    def __init__(self, aplicacao):
        super().__init__(aplicacao)
        self.heroi = aplicacao.heroi
        self.pontuacao = Pontuacao()      # os pontos da partida inteira
        self.indice_nivel = 0                      # posição na lista NIVEIS do settings.py
        self.pausado = False            
        self.tempo = 0                    # segundos de partida (dá o bônus de tempo)
        self.carregar_nivel()

    def carregar_nivel(self):
        """Monta o nível atual e uma câmera do tamanho do mapa dele."""
        nome, arquivo = NIVEIS[self.indice_nivel]
        self.nivel = Nivel(nome, arquivo, self.heroi, self.pontuacao, self.aplicacao.som)
        self.camera = Camera(self.nivel.mapa.largura, self.nivel.mapa.altura)
        self.aviso_nivel = 2              # segundos com o nome do nível no meio da tela
        if self.nivel.chefe is not None:
            self.aplicacao.som.tocar_musica("chefe")
        else:
            self.aplicacao.som.tocar_musica("torre")   # do Térreo para a Biblioteca não reinicia

    def tratar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key == pygame.K_ESCAPE:
            self.pausado = not self.pausado          # ESC pausa e ESC de novo continua
            self.aplicacao.som.pausar_musica(self.pausado)
        elif self.pausado:
            return                                   # pausado, as outras teclas não fazem nada
        elif evento.key == pygame.K_SPACE:
            self.atacar(self.heroi.usar_ataque())
        elif evento.key == pygame.K_LSHIFT:
            self.atacar(self.heroi.usar_especial())

    def atacar(self, projeteis):
        """Põe os projéteis do ataque no nível. Lista vazia quer dizer que ainda estava recarregando."""
        if len(projeteis) > 0:
            self.nivel.projeteis.extend(projeteis)
            self.aplicacao.som.tocar("ataque")

    def atualizar(self, dt):
        if self.pausado:
            return                                   # nada anda: nem o tempo da partida
        self.tempo += dt
        self.aviso_nivel = max(0, self.aviso_nivel - dt)
        self.nivel.atualizar(dt)
        self.camera.seguir(self.heroi.posicao)
        tem_proximo = self.indice_nivel + 1 < len(NIVEIS)
        if self.nivel.heroi_na_saida() and tem_proximo:
            self.passar_de_nivel()
        if not self.heroi.esta_vivo():
            self.terminar(False)                     # derrota: a vida acabou
        elif self.nivel.chefe is not None and not self.nivel.chefe.esta_vivo():
            self.terminar(True)                      # vitória: o chefe caiu

    def passar_de_nivel(self):
        """Soma os pontos do nível e carrega o próximo. O herói continua com a vida que sobrou."""
        self.pontuacao.nivel_concluido(self.nivel.nome)
        self.aplicacao.som.tocar("porta")
        self.indice_nivel += 1
        self.carregar_nivel()

    def terminar(self, venceu):
        """Fim da partida: aplica o bônus, guarda o resultado na Aplicacao e vai para o resultado."""
        if not venceu:
            self.aplicacao.som.tocar("heroi_derrotado")
        vida_restante = self.heroi.vida / self.heroi.vida_maxima      # de 0 a 1
        self.pontuacao.aplicar_bonus(venceu, self.tempo, vida_restante)
        self.aplicacao.pontuacao = self.pontuacao
        self.aplicacao.venceu = venceu
        self.aplicacao.trocar_tela("resultado")

    def desenhar(self, superficie):
        self.nivel.desenhar(superficie, self.camera)
        self.desenhar_hud(superficie)
        if self.pausado:
            self.desenhar_pausa(superficie)
        elif self.aviso_nivel > 0:
            desenhar_texto(superficie, self.nivel.nome, (LARGURA_TELA // 2, ALTURA_TELA // 2), YELLOW, 48,
                           centralizado=True)

    def desenhar_pausa(self, superficie):
        """Escurece o jogo e escreve PAUSADO no meio."""
        sombra = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)   # superfície com transparência
        sombra.fill((0, 0, 0, 160))                  # preto com 160 de 255 de opacidade
        superficie.blit(sombra, (0, 0))
        meio = (LARGURA_TELA // 2, ALTURA_TELA // 2)
        desenhar_texto(superficie, "PAUSADO", meio, WHITE, 48, centralizado=True)
        desenhar_texto(superficie, "ESC continua", (meio[0], meio[1] + 32), WHITE, 28, centralizado=True)

    def desenhar_hud(self, superficie):
        """O que fica parado por cima do jogo: vida, nível, pontos, saída e a vida do chefe."""
        heroi = self.heroi
        desenhar_texto(superficie, self.aplicacao.nome_jogador, (6, 6), WHITE, 24)
        cor = GREEN
        if heroi.vida < heroi.vida_maxima * 0.3:
            cor = RED                                # pouca vida: a barra fica vermelha
        desenhar_barra(superficie, pygame.Rect(6, 26, 100, 8), heroi.vida, heroi.vida_maxima, cor)

        desenhar_texto(superficie, self.nivel.nome, (LARGURA_TELA // 2, 14), WHITE, 28, centralizado=True)
        texto = f"{self.pontuacao.total} pts"
        largura = fonte(28).size(texto)[0]
        desenhar_texto(superficie, texto, (LARGURA_TELA - 6 - largura, 6), YELLOW, 28)

        if self.nivel.mapa.saida is not None and self.nivel.esta_limpo():
            desenhar_texto(superficie, "Saída aberta!", (LARGURA_TELA // 2, 40), YELLOW, 28, centralizado=True)

        chefe = self.nivel.chefe
        if chefe is not None and chefe.esta_vivo():
            desenhar_texto(superficie, chefe.nome, (LARGURA_TELA // 2, 280), WHITE, 24, centralizado=True)
            desenhar_barra(superficie, pygame.Rect(80, 292, 320, 12), chefe.vida, chefe.vida_maxima, RED)