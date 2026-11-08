"""Classe TelaClasses (herda de Tela): escolha da classe.

O que aparece:
    Um cartão para cada classe de data/classes.json (hoje Mago, Arqueiro e
    Bárbaro), cada um com imagem, nome e atributos. O cartão selecionado
    fica destacado, e embaixo aparece a descrição da classe selecionada.
    Uma classe nova no JSON aparece aqui sozinha.

Atributos:
    - cartoes: list[CartaoClasse]. Um por ClasseHeroi do Catalogo.
    - selecionado: int. Índice do cartão destacado.

O que faz:
    - tratar_entrada(entrada: EntradaMenu):
        * ESQUERDA e DIREITA mudam o selecionado;
        * CONFIRMAR grava a classe no PerfilJogador do P1 e troca para
          TelaJogo;
        * VOLTAR volta para TelaInicial.
    - desenhar(superficie): cartões e descrição.

Co-op (quando for feito): um selecionado por jogador, cada um mexendo com
o próprio dispositivo (a EntradaMenu diz de qual dispositivo veio cada
ação).

Usa: ui/cartao_classe.py, jogo/catalogo.py, aplicacao/sessao.py.
"""
import pygame

from entrada.entrada_menu import AcaoMenu, EntradaMenu
from settings import BLACK, LARGURA_TELA, WHITE, YELLOW
from telas.tela import Tela
from ui.texto import desenhar_texto


class TelaClasses(Tela):
    def __init__(self, aplicacao) -> None:
        super().__init__(aplicacao)                    # guarda self.aplicacao
        self.opcoes = ["mago", "arqueiro", "barbaro"]
        self.selecionado = 0                           # índice em self.opcoes

    def tratar_entrada(self, entrada: EntradaMenu) -> None:
        if entrada.tem(AcaoMenu.ESQUERDA):
            self.selecionado = (self.selecionado - 1) % len(self.opcoes)   # o % dá a volta
        if entrada.tem(AcaoMenu.DIREITA):
            self.selecionado = (self.selecionado + 1) % len(self.opcoes)
        if entrada.tem(AcaoMenu.CONFIRMAR):
            self.aplicacao.sessao.buscar(1).classe = self.opcoes[self.selecionado]
            from telas.tela_jogo import TelaJogo        # aqui dentro: evita o import circular
            self.aplicacao.trocar_tela(TelaJogo(self.aplicacao))
        elif entrada.tem(AcaoMenu.VOLTAR):
            from telas.tela_inicial import TelaInicial
            self.aplicacao.trocar_tela(TelaInicial(self.aplicacao))

    def atualizar(self, dt: float) -> None:
        pass

    def desenhar(self, superficie: pygame.Surface) -> None:
        superficie.fill(BLACK)
        for i, opcao in enumerate(self.opcoes):
            cor = YELLOW if i == self.selecionado else WHITE
            desenhar_texto(superficie, opcao, (LARGURA_TELA // 2, 50 + i * 20), cor, centralizado=True)
