import pygame

from jogo.ranking import Ranking
from settings import ALTURA_TELA, ESCALA, FPS, LARGURA_TELA, TITULO
from telas.tela_classes import TelaClasses
from telas.tela_inicial import TelaInicial
from telas.tela_jogo import TelaJogo
from telas.tela_resultado import TelaResultado


class Aplicacao:
    """Abre a janela, roda o loop e troca de tela. Guarda o que passa de uma tela
    para outra: o nome do jogador, o herói escolhido, a pontuação e o ranking.
    """

    def __init__(self):
        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA_TELA * ESCALA, ALTURA_TELA * ESCALA))
        pygame.display.set_caption(TITULO)
        self.tela_jogo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))   # tudo é desenhado aqui e depois ampliado
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.nome_jogador = ""
        self.heroi = None                 # escolhido na TelaClasses
        self.pontuacao = None             # criada na TelaJogo
        self.venceu = False
        self.ranking = Ranking()
        self.tela_atual = None
        self.trocar_tela("inicial")

    def trocar_tela(self, nome):
        if nome == "inicial":
            self.tela_atual = TelaInicial(self)
        elif nome == "classes":
            self.tela_atual = TelaClasses(self)
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
                else:
                    self.tela_atual.tratar_evento(evento)
            self.tela_atual.atualizar(dt)
            self.tela_atual.desenhar(self.tela_jogo)
            pygame.transform.scale(self.tela_jogo, self.janela.get_size(), self.janela)
            pygame.display.flip()
        pygame.quit()
