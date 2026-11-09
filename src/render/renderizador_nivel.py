"""Classe RenderizadorNivel: desenha o nível. É o único que desenha o mundo.

O que é:
    Separa o desenho da lógica, como a Interface::desenhar da simulação
    lobo-coelho desenha o Mundo inteiro e o Animal nunca se desenha. Ele
    só LÊ o Nivel: nunca move, cria ou remove nada.

    A lógica roda a 20 ticks por segundo e a tela a 60 quadros por
    segundo. Entre um tick e o próximo, o renderizador desenha 3 quadros,
    e em cada um coloca as entidades um pouco mais à frente no caminho
    entre posicao_anterior e posicao. Assim o herói anda liso na tela,
    mesmo que a posição "de verdade" só mude 20 vezes por segundo.

Atributos:
    - aparencias: Aparencias.
    - camera: Camera.
    - relogio: float. Segundos de tela desde o começo da partida. Serve
      para o que pisca ou se mexe sem depender de uma ação (herói
      invulnerável piscando, saída aberta brilhando, ladrilho de água).

Métodos:
    - avancar(dt: float) -> None: relogio += dt. A TelaJogo chama a cada
      quadro, inclusive nos quadros em que nenhum tick roda.
    - desenhar(superficie: pygame.Surface, nivel: Nivel, alfa: float)
      -> None. alfa vem de mundo.fracao_tick(), de 0 a 1:
        1. posição de desenho de cada entidade:
           posicao_anterior.lerp(posicao, alfa);
        2. camera.seguir(posições de desenho dos heróis vivos), para a
           câmera também andar lisa;
        3. desenha os ladrilhos de nivel.mapa.ladrilhos_em(área visível);
        4. desenha a saída (diferente se estiver aberta);
        5. desenha personagens e projéteis visíveis, ordenados pelo y de
           desenho (quem está mais embaixo aparece na frente). A imagem de
           cada personagem vem de aparencias.quadro(aparencia, acao_atual,
           tempo_na_acao + alfa * Mundo.PASSO), virada para o lado de
           direcao_olhar;
        6. personagem invulnerável pisca, usando o relogio.
      A caixa de desenho é montada na posição de desenho. Ela não usa
      entidade.caixa, que é a do tick e serve só para colisão.
    - mudar_mapa(nivel: Nivel) -> None: avisa a câmera do tamanho do mapa
      novo.

Quem usa: TelaJogo.
Usa: render/camera.py, render/aparencias.py, jogo/nivel.py (só leitura),
jogo/mundo.py (só a constante PASSO).
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from render.aparencias import Aparencias, desenhar_visual
from render.camera import Camera
from settings import BLACK
from jogo.mundo import Mundo                    # só para usar Mundo.PASSO
from personagens.personagem import Personagem   # para saber se a entidade é personagem ou projétil

if TYPE_CHECKING:
    from jogo.nivel import Nivel


class RenderizadorNivel: #renderiza o nivel
    def __init__(self, aparencias: Aparencias) -> None:
        self.aparencias = aparencias
        self.camera = Camera()
        self.relogio = 0.0

    def avancar(self, dt: float) -> None: #ataualiza o tempo a cada quadro
        self.relogio += dt

    def mudar_mapa(self, nivel: Nivel) -> None: #avisa a câmera do tamanho do mapa novo
        self.camera.mudar_mapa(nivel.mapa.largura, nivel.mapa.altura)

    def desenhar(self, superficie: pygame.Surface, nivel: Nivel, alfa: float) -> None:
        superficie.fill(BLACK)

        # Calcula as posições de desenho sem alterar as posições das entidades.
        entidades = list(nivel.personagens.values()) + list(nivel.projeteis.values())

        posicoes = {e.id: e.posicao_anterior.lerp(e.posicao, alfa) for e in entidades}

        self.camera.seguir([posicoes[h.id]
            for h in nivel.herois()
            if h.esta_vivo
        ])

        saida_aberta = nivel.esta_limpo()

        # Desenha todos os ladrilhos da área visível.
        for retangulo, chave in nivel.mapa.ladrilhos_em(self.camera.area_visivel()):
            if chave == "saida" and saida_aberta:
                if int(self.relogio * 4) % 2 == 0:
                    chave = "saida_aberta"

            desenhar_visual(superficie, self.aparencias.obter(chave), self.camera.para_tela(retangulo))

        # Quem está mais embaixo é desenhado por último.
        for entidade in sorted(entidades, key=lambda e: posicoes[e.id].y):
            posicao = posicoes[entidade.id]

            caixa = pygame.Rect(
                0, 0,
                int(entidade.tamanho.x),
                int(entidade.tamanho.y),
            )
            caixa.center = (round(posicao.x), round(posicao.y))

            # Pula entidades que estão fora da câmera.
            if not self.camera.esta_visivel(caixa):
                continue

            if isinstance(entidade, Personagem):
                # Personagens invulneráveis piscam.
                if entidade.invulneravel > 0:
                    if int(self.relogio * 10) % 2 == 0:
                        continue

                tempo = entidade.tempo_na_acao + alfa * Mundo.PASSO
                visual = self.aparencias.quadro(entidade.aparencia, entidade.acao_atual, tempo)
                espelhar = entidade.direcao_olhar.x < 0

            else:
                visual = self.aparencias.obter(entidade.aparencia)
                espelhar = False

            desenhar_visual(superficie, visual, self.camera.para_tela(caixa), espelhar)