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
import pygame

from entrada.entrada_menu import AcaoMenu, EntradaMenu
from settings import ALTURA_TELA, BLACK, LARGURA_TELA, WHITE, YELLOW
from telas.tela import Tela
from ui.texto import desenhar_texto


class TelaJogo(Tela):
    def tratar_entrada(self, entrada: EntradaMenu) -> None:
        if entrada.tem(AcaoMenu.CONFIRMAR):
            from telas.tela_resultado import TelaResultado   # aqui dentro: evita o import circular
            self.aplicacao.trocar_tela(TelaResultado(self.aplicacao))

    def atualizar(self, dt: float) -> None:
        pass

    def desenhar(self, superficie: pygame.Surface) -> None:
        superficie.fill(BLACK)
        desenhar_texto(superficie, "JOGO (em construção)", (LARGURA_TELA // 2, ALTURA_TELA // 2),
                       YELLOW, centralizado=True)
        classe = self.aplicacao.sessao.buscar(1).classe   # se aparecer a classe escolhida, a Sessao guardou
        desenhar_texto(superficie, str(classe), (LARGURA_TELA // 2, ALTURA_TELA // 2 + 20),
                       WHITE, centralizado=True)
