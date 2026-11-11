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
"""
import pygame

from entrada.entrada_menu import AcaoMenu, EntradaMenu
from settings import BLACK, GRAY, LARGURA_TELA, WHITE, YELLOW
from telas.tela import Tela
from ui.cartao_classe import CartaoClasse
from ui.texto import desenhar_texto


class TelaClasses(Tela):
    def __init__(self, aplicacao) -> None:
        super().__init__(aplicacao)

        classes = aplicacao.catalogo.classes
        self.chaves = list(classes.keys())
        self.selecionado = 0

        n=len(self.chaves)
        largura = min(72,(LARGURA_TELA-8-6*(n-1))//n)
        x0=(LARGURA_TELA - (n*largura+(n-1)*6)) // 2
        self.cartoes = [CartaoClasse(classes[chave], pygame.Rect(x0 + i*(largura + 6), 22, largura, 90)) for i, chave in enumerate(self.chaves)]

    def tratar_entrada(self, entrada: EntradaMenu) -> None:
        for acao, k in entrada.acoes: #entrada.acoes retorna 2 variaveis, mas não se usa a segunda aqui
            if acao == AcaoMenu.ESQUERDA:
                self.selecionado = (self.selecionado - 1) % len(self.cartoes) #vai para a esquerda

            elif acao == AcaoMenu.DIREITA:
                self.selecionado = (self.selecionado + 1) % len(self.cartoes) #vai para a direita

            elif acao == AcaoMenu.CONFIRMAR:
                self.aplicacao.sessao.buscar(1).classe = self.chaves[self.selecionado]
                from telas.tela_jogo import TelaJogo
                self.aplicacao.trocar_tela(TelaJogo(self.aplicacao))
                return

            elif acao == AcaoMenu.VOLTAR:
                from telas.tela_inicial import TelaInicial
                self.aplicacao.trocar_tela(TelaInicial(self.aplicacao))
                return


    def atualizar(self, dt: float):
        pass #provisorio

    def desenhar(self, superficie: pygame.Surface) -> None:
        superficie.fill(BLACK)
        desenhar_texto(superficie, "Escolha sua classe", (LARGURA_TELA // 2, 10), YELLOW, 18, centralizado=True)

        for i, cartao in enumerate(self.cartoes):
            cartao.desenhar(superficie, self.aplicacao.aparencias, i == self.selecionado)

        descricao = self.cartoes[self.selecionado].classe.descricao
        desenhar_texto(superficie, descricao, (LARGURA_TELA // 2, 124), WHITE, 14, centralizado=True)

        desenhar_texto(superficie, "ENTER escolhe   ESC volta", (LARGURA_TELA // 2, 148), GRAY, 14, centralizado=True)