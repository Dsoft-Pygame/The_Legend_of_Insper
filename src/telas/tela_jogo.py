"""Classe TelaJogo (herda de Tela): a tela onde se joga.

O que é:
    Uma tela "fina": quem controla a partida é o Mundo, e quem desenha o
    nível é o RenderizadorNivel. A TelaJogo só monta as peças, passa o
    tempo, desenha e decide quando a partida acabou.

    Ela é chamada 60 vezes por segundo, mas a partida anda 20 ticks por
    segundo. Quem converte um no outro é o Mundo; a TelaJogo só entrega o
    tempo real e, na hora de desenhar, quanto do próximo tick já passou.

Atributos:
    - mundo: Mundo.
    - renderizador: RenderizadorNivel.
    - hud: Hud.
    - aviso_nivel: float. Segundos restantes mostrando o nome do nível.

O que faz:
    - ao_entrar(): para CADA PerfilJogador da Sessao (um hoje, vários no
      co-op):
        1. pede o dispositivo dele ao GerenciadorDispositivos;
        2. cria o personagem com fabrica.criar_heroi(perfil.classe, ...);
        3. cria um ControladorHumano com esse dispositivo;
        4. junta tudo num Heroi.
      Depois cria o Mundo com a lista de heróis e o tema da Sessao.
    - tratar_entrada(entrada: EntradaMenu): VOLTAR pode pausar (futuro).
      O movimento dos heróis não passa por aqui: vem dos dispositivos,
      pelos controladores.
    - atualizar(dt): a cada quadro,
        1. mundo.tempo_avancar(dt): roda 0, 1 ou mais ticks;
        2. renderizador.avancar(dt): o relógio do desenho anda sempre;
        3. desconta aviso_nivel.
      Se mundo.terminou(), guarda o resultado e a pontuação na Sessao e
      troca para TelaResultado.
    - desenhar(superficie): renderizador.desenhar(superficie,
      mundo.nivel_atual, mundo.fracao_tick()) e, por cima,
      hud.desenhar(superficie, mundo.resumo()). Ao trocar de nível, mostra
      o nome dele no meio da tela por uns segundos. O HUD não é
      interpolado: vida e pontos mudam de uma vez, no tick.

Usa: jogo/mundo.py, jogo/fabrica.py, controle/controlador_humano.py,
render/renderizador_nivel.py, ui/hud.py,
entrada/gerenciador_dispositivos.py.
"""
import random

import pygame

from controle.controlador_humano import ControladorHumano
from entrada.entrada_menu import EntradaMenu
from jogo.fabrica import Fabrica
from jogo.mundo import Heroi, Mundo
from render.renderizador_nivel import RenderizadorNivel
from settings import ALTURA_TELA, LARGURA_TELA, YELLOW
from telas.tela import Tela
from ui.texto import desenhar_texto

TEMPO_AVISO_NIVEL = 2.0     # segundos com o nome do nível no meio da tela


class TelaJogo(Tela):
    def __init__(self, aplicacao) -> None:
        super().__init__(aplicacao)
        self.mundo = None                   # é criado no ao_entrar
        self.renderizador = RenderizadorNivel(aplicacao.aparencias)
        self.aviso_nivel = 0.0
        self.nivel_desenhado = None

    def ao_entrar(self) -> None:
        app = self.aplicacao
        fabrica = Fabrica(app.catalogo, semente=random.randrange(1_000_000))
        herois = []
        for perfil in app.sessao.jogadores:
            dispositivo = app.dispositivos.reservar(perfil.dispositivo)                 # T27
            personagem = fabrica.criar_heroi(perfil.classe, pygame.Vector2(0, 0))       # o Mundo põe no H
            herois.append(Heroi(perfil.numero, perfil.nome, personagem, ControladorHumano(dispositivo)))
        tema = app.catalogo.temas[app.sessao.tema or app.catalogo.tema_padrao]
        self.mundo = Mundo(tema, fabrica, herois)
        self.trocou_de_nivel()

    def trocou_de_nivel(self) -> None:
        self.nivel_desenhado = self.mundo.nivel_atual
        self.renderizador.mudar_mapa(self.mundo.nivel_atual)
        self.aviso_nivel = TEMPO_AVISO_NIVEL

    def tratar_entrada(self, entrada: EntradaMenu) -> None:
        pass    # pausa: T65

    def atualizar(self, dt: float) -> None:
        self.mundo.tempo_avancar(dt)        # roda 0, 1 ou mais ticks
        self.renderizador.avancar(dt)
        if self.mundo.nivel_atual is not self.nivel_desenhado:
            self.trocou_de_nivel()
        self.aviso_nivel = max(0.0, self.aviso_nivel - dt)
        # fim da partida: T52

    def desenhar(self, superficie: pygame.Surface) -> None:
        self.renderizador.desenhar(superficie, self.mundo.nivel_atual, self.mundo.fracao_tick())
        if self.aviso_nivel > 0:
            desenhar_texto(superficie, self.mundo.nivel_atual.nome, (LARGURA_TELA // 2, ALTURA_TELA // 2),
                           YELLOW, 24, centralizado=True)
        # HUD: T60
