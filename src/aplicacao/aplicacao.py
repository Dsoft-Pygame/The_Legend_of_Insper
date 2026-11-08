"""Classe Aplicacao: o "motor" que mantém o jogo rodando.

O que é:
    Existe uma única Aplicacao durante todo o programa. Ela abre a janela,
    roda o loop principal e sabe qual tela está aparecendo agora. Também
    guarda a Sessao, com os jogadores que passam de uma tela para outra
    (o nome digitado na primeira tela é usado na última).

    Ela não lê teclado nem eventos do pygame: quem faz isso é o
    LeitorEntrada (entrada/), e a Aplicacao só repassa o resultado.

    A Aplicacao só conhece QUADROS (60 por segundo). Ela não sabe o que é
    um tick: quem transforma tempo real em ticks de lógica é o Mundo,
    dentro da TelaJogo. Os menus usam dt direto, sem ticks.

Atributos (o que ela guarda):
    - QUADROS_POR_SEGUNDO: int. 60. Quantas vezes por segundo a tela é
      desenhada.
    - janela: pygame.Surface. A janela do pygame.
    - tela_jogo: pygame.Surface. Superfície pequena (resolução de GBA,
      240x160) onde tudo é desenhado antes de ser ampliado para a janela.
    - relogio: pygame.time.Clock. Segura o loop em QUADROS_POR_SEGUNDO.
    - catalogo: Catalogo. Todo o conteúdo de data/, lido uma vez.
    - leitor_entrada: LeitorEntrada. O único que conversa com pygame.event.
    - dispositivos: GerenciadorDispositivos. Teclados e controles.
    - ranking: Ranking. Criado uma vez e usado pelas telas.
    - sessao: Sessao. Os jogadores da partida (uma lista, pronta para co-op).
    - tela_atual: Tela. A tela ativa (TelaInicial, TelaJogo...).

Métodos (o que ela faz):
    - executar() -> None: loop principal. A cada quadro:
        1. entrada = leitor_entrada.ler_quadro(); se entrada.fechar, sai;
        2. dispositivos.atualizar(entrada), para controles ligados ou
           desligados, e dispositivos.amostrar(), para cada dispositivo
           olhar teclas e botões neste quadro (um toque rápido entre dois
           ticks não se perde);
        3. tela_atual.tratar_entrada(entrada.menu);
        4. tela_atual.atualizar(dt), com dt = relogio.tick(60) / 1000, em
           segundos desde o último quadro;
        5. tela_atual.desenhar(tela_jogo), amplia para a janela e mostra.
    - trocar_tela(nova_tela: Tela) -> None: chama ao_sair da tela antiga,
      ao_entrar da nova e troca.

Quem usa: main.py.
Usa: entrada/, telas/, aplicacao/sessao.py, jogo/catalogo.py,
jogo/ranking.py.
"""
from __future__ import annotations

import pygame

from aplicacao.sessao import Sessao
from entrada.gerenciador_dispositivos import GerenciadorDispositivos
from entrada.leitor_entrada import LeitorEntrada
from jogo.catalogo import Catalogo
from render.aparencias import Aparencias
from settings import ALTURA_TELA, ESCALA, LARGURA_TELA, TITULO
from telas.tela import Tela
from telas.tela_inicial import TelaInicial


class Aplicacao:
    QUADROS_POR_SEGUNDO = 60

    def __init__(self) -> None:
        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA_TELA * ESCALA, ALTURA_TELA * ESCALA))  # 960 x 640
        pygame.display.set_caption(TITULO)
        self.tela_jogo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))   # 240 x 160: tudo é desenhado aqui
        self.relogio = pygame.time.Clock()
        self.leitor_entrada = LeitorEntrada()
        self.catalogo = Catalogo.carregar()                                   # T11: lê todos os JSON uma vez
        self.aparencias = Aparencias.carregar(self.catalogo.aparencias)       # T16: carrega as imagens
        self.dispositivos = GerenciadorDispositivos(self.catalogo.controles)  # T27
        self.sessao = Sessao()                                                # T03
        self.sessao.tema = self.catalogo.tema_padrao
        # ranking: T58
        self.tela_atual: Tela | None = None
        self.trocar_tela(TelaInicial(self))

    def trocar_tela(self, nova_tela: Tela) -> None:
        if self.tela_atual is not None:
            self.tela_atual.ao_sair()
        nova_tela.ao_entrar()
        self.tela_atual = nova_tela

    def executar(self) -> None:
        while True:
            entrada = self.leitor_entrada.ler_quadro()
            if entrada.fechar:
                break
            self.dispositivos.atualizar(entrada)   # controles ligados/desligados (T69)
            self.dispositivos.amostrar()           # todo quadro, para não perder toque rápido
            self.tela_atual.tratar_entrada(entrada.menu)
            dt = self.relogio.tick(self.QUADROS_POR_SEGUNDO) / 1000
            self.tela_atual.atualizar(dt)
            self.tela_atual.desenhar(self.tela_jogo)
            pygame.transform.scale(self.tela_jogo, self.janela.get_size(), self.janela)
            pygame.display.flip()
        pygame.quit()
