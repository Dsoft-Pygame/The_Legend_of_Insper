import pygame

from settings import BLACK, GRAY, RED, WHITE, YELLOW
from telas.tela import Tela
from ui import CaixaTexto, desenhar_texto



class TelaInicial(Tela):
    def __init__(self, aplicacao):
        super().__init__(aplicacao)
        self.caixa_nome = CaixaTexto(pygame.Rect(8, 76, 112, 16))
        self.aviso = ""                   # aparece se apertar Enter sem nome
        self.tempo = 0                    # segundos nesta tela: faz o cursor e o aviso piscarem

    def tratar_evento(self, evento):
        if evento.type == pygame.TEXTINPUT:
            self.caixa_nome.digitar(evento.text)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                self.caixa_nome.apagar()
            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.confirmar()

    def confirmar(self):
        nome = self.caixa_nome.texto.strip()   # strip tira os espaços do começo e do fim
        if nome == "":
            self.aviso = "Digite um nome"
            return
        self.aplicacao.nome_jogador = nome
        self.aplicacao.trocar_tela("classes")

    def desenhar(self, superficie):
        superficie.fill(BLACK)
        desenhar_texto(superficie, "The Legend", (64, 24), YELLOW, 22, centralizado=True)
        desenhar_texto(superficie, "of Insper", (64, 42), YELLOW, 22, centralizado=True)
        desenhar_texto(superficie, "Seu nome:", (8, 64), WHITE, 14)
        cursor_visivel = int(self.tempo * 2) % 2 == 0          # liga e desliga a cada meio segundo
        self.caixa_nome.desenhar(superficie, cursor_visivel)
        if self.aviso != "" and int(self.tempo * 3) % 2 == 0:
            desenhar_texto(superficie, self.aviso, (8, 98), RED, 14)
        desenhar_texto(superficie, "ENTER para jogar", (64, 140), GRAY, 14, centralizado=True)

    def atualizar(self, dt):
        self.tempo += dt
