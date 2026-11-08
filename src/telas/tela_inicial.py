"""Classe TelaInicial (herda de Tela): a primeira tela do jogo.

O que aparece:
    - À esquerda: nome do jogo e um campo para digitar o nome do jogador.
    - À direita: o ranking com os melhores jogadores.
    - Embaixo: "ENTER para jogar".

Atributos:
    - caixa_nome: CaixaTexto onde o jogador digita o nome.
    - painel_ranking: PainelRanking que desenha a lista.
    - aviso: str. "Digite um nome" quando tenta seguir com o nome vazio.

O que faz:
    - ao_entrar(): limpa a Sessao e a caixa do nome.
    - tratar_entrada(entrada: EntradaMenu): passa entrada.texto para
      caixa_nome.digitar e APAGAR para caixa_nome.apagar. CONFIRMAR com o
      nome preenchido cria o PerfilJogador do P1 na Sessao e troca para
      TelaClasses. O P1 fica com o dispositivo que apertou CONFIRMAR
      (teclado_wasd, se foi o teclado). Nome vazio mostra o aviso.
    - atualizar(dt): pisca o cursor e o aviso.
    - desenhar(superficie): título, caixa de nome e ranking.

Co-op (quando for feito): um segundo jogador aperta CONFIRMAR no próprio
dispositivo e digita o nome; vira o PerfilJogador 2.

Usa: ui/caixa_texto.py, ui/painel_ranking.py, jogo/ranking.py,
aplicacao/sessao.py, entrada/gerenciador_dispositivos.py.
"""
import pygame

from entrada.entrada_menu import AcaoMenu, EntradaMenu
from settings import ALTURA_TELA, BLACK, GRAY, LARGURA_TELA, YELLOW
from telas.tela import Tela
from ui.texto import desenhar_texto


class TelaInicial(Tela):
    def ao_entrar(self) -> None:
        self.aplicacao.sessao.limpar()                 # toda vez que a tela aparece, começa uma partida nova

    def tratar_entrada(self, entrada: EntradaMenu) -> None:
        if entrada.tem(AcaoMenu.CONFIRMAR):
            self.aplicacao.sessao.adicionar_jogador("Jogador", "teclado_wasd")   # jogador provisório (T55)
            from telas.tela_classes import TelaClasses  # aqui dentro: evita o import circular
            self.aplicacao.trocar_tela(TelaClasses(self.aplicacao))

    def atualizar(self, dt: float) -> None:
        pass

    def desenhar(self, superficie: pygame.Surface) -> None:
        superficie.fill(BLACK)
        desenhar_texto(superficie, "The Legend of Insper", (LARGURA_TELA // 2, ALTURA_TELA // 2),
                       YELLOW, 22, centralizado=True)
        desenhar_texto(superficie, "ENTER para jogar", (LARGURA_TELA // 2, ALTURA_TELA // 2 + 24),
                       GRAY, centralizado=True)
