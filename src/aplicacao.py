import pygame

from jogo.ranking import Ranking
from settings import ALTURA_TELA, ESCALA, FPS, LARGURA_TELA, TELA_CHEIA, TITULO
from sons import Som
from telas.tela_classes import TelaClasses
from telas.tela_inicial import TelaInicial
from telas.tela_jogo import TelaJogo
from telas.tela_resultado import TelaResultado
from telas.tela_controles import TelaControles


class Aplicacao:
    """Abre a janela, roda o loop e troca de tela. Guarda o que passa de uma tela
    para outra: o herói escolhido e o ranking.
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITULO)
        self.tela_cheia = TELA_CHEIA
        self.abrir_janela()
        self.tela_jogo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))   # tudo é desenhado aqui e depois ampliado
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.som = Som()                  # as telas tocam com self.aplicacao.som.tocar("...")
        self.nome_jogador = ""            # digitado na TelaInicial
        self.heroi = None                 # escolhido na TelaClasses
        self.pontuacao = None             # os pontos da partida que acabou (a TelaJogo guarda aqui)
        self.venceu = False
        self.ranking = Ranking()          # lido do arquivo ao abrir o jogo, como na main
        self.tela_atual = None
        self.trocar_tela("inicial")

    def abrir_janela(self):
        """Abre a janela em tela cheia ou do tamanho normal e calcula onde o jogo fica nela.

        Em tela cheia o jogo é ampliado pelo maior número inteiro que cabe no monitor (assim os
        pixels continuam quadradinhos) e fica no meio; o resto da tela fica preto.
        """
        if self.tela_cheia:
            self.janela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)   # (0, 0) = o tamanho do monitor
        else:
            self.janela = pygame.display.set_mode((LARGURA_TELA * ESCALA, ALTURA_TELA * ESCALA))
        largura, altura = self.janela.get_size()
        escala = max(1, min(largura // LARGURA_TELA, altura // ALTURA_TELA))
        self.area_jogo = pygame.Rect(0, 0, LARGURA_TELA * escala, ALTURA_TELA * escala)
        self.area_jogo.center = (largura // 2, altura // 2)

    def trocar_tela(self, nome):
        if nome == "inicial":
            self.tela_atual = TelaInicial(self)
        elif nome == "classes":
            self.tela_atual = TelaClasses(self)
        elif nome == "controles":
            self.tela_atual = TelaControles(self)
        elif nome == "jogo":
            self.tela_atual = TelaJogo(self)
        elif nome == "resultado":
            self.tela_atual = TelaResultado(self)


    def executar(self):
        while self.rodando:
            dt = min(self.relogio.tick(FPS) / 1000, 0.05)   # segundos desde o quadro anterior
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
                    self.tela_cheia = not self.tela_cheia      # F11 entra e sai da tela cheia
                    self.abrir_janela()
                else:
                    self.tela_atual.tratar_evento(evento)
            self.tela_atual.atualizar(dt)
            self.tela_atual.desenhar(self.tela_jogo)
            self.janela.fill((0, 0, 0))                      # as tarjas pretas em volta
            ampliada = pygame.transform.scale(self.tela_jogo, self.area_jogo.size)
            self.janela.blit(ampliada, self.area_jogo)
            pygame.display.flip()
        pygame.quit()
