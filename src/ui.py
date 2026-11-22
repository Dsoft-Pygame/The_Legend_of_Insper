"""Peças de interface usadas pelas telas: o texto e a caixa do nome "e o quadro do ranking"."""
import pygame
import os
from settings import DARK_GRAY, GRAY, WHITE, YELLOW, PASTA_ASSETS

fontes = {}   # uma fonte por tamanho, criada uma vez só
imagens = {}  # cada imagem de src/assets/ é lida do disco uma vez só

def fonte(tamanho):
    """A fonte padrão do pygame nesse tamanho. Cria uma vez só e guarda."""
    if tamanho not in fontes:
        fontes[tamanho] = pygame.font.Font(None, tamanho)   # None = a fonte padrão do pygame
    return fontes[tamanho]

def carregar_imagem(nome): #carrrega imagem se ela existir
    """Lê uma imagem de src/assets/ uma vez só e guarda. Devolve None se o arquivo não existe (quem chama
    desenha um quadrado no lugar).
    """
    if nome not in imagens:
        caminho = os.path.join(PASTA_ASSETS, nome)
        imagens[nome] = None
        if os.path.exists(caminho):
            imagens[nome] = pygame.image.load(caminho).convert_alpha()   # convert_alpha: fundo transparente
    return imagens[nome]

def desenhar_texto(superficie, texto, posicao, cor=WHITE, tamanho=32, centralizado=False):
    """Escreve o texto na tela e devolve o retângulo que ele ocupou."""
    imagem = fonte(tamanho).render(texto, False, cor)
    retangulo = imagem.get_rect()
    if centralizado:
        retangulo.center = posicao
    else:
        retangulo.topleft = posicao
    superficie.blit(imagem, retangulo)
    return retangulo


class CaixaTexto:
    """Campo onde o jogador digita o nome, com um cursor piscando no fim."""

    def __init__(self, retangulo, tamanho_maximo=12):
        """Uma caixa vazia nesse retângulo, que aceita até tamanho_maximo letras."""
        self.retangulo = retangulo
        self.tamanho_maximo = tamanho_maximo
        self.texto = ""

    def digitar(self, letras):
        """Acrescenta as letras digitadas: só letras, números, espaço, - e _."""
        for letra in letras:
            if len(self.texto) < self.tamanho_maximo and (letra.isalnum() or letra in " -_"):
                self.texto += letra

    def apagar(self):
        """Apaga a última letra (Backspace)."""
        self.texto = self.texto[:-1]

    def desenhar(self, superficie, cursor_visivel):
        """Desenha a caixa, o texto e, se cursor_visivel, o cursor amarelo no fim do texto."""
        pygame.draw.rect(superficie, DARK_GRAY, self.retangulo)
        pygame.draw.rect(superficie, WHITE, self.retangulo, 2)
        area = desenhar_texto(superficie, self.texto, (self.retangulo.x + 6, self.retangulo.y + 6))
        if cursor_visivel:
            x = self.retangulo.x + 6
            if self.texto != "":
                x = area.right + 2
            pygame.draw.line(superficie, YELLOW, (x, self.retangulo.y + 6), (x, self.retangulo.bottom - 8), 2)

def desenhar_ranking(superficie, retangulo, partidas, destaque=None):
    """Quadro do ranking: posição, nome e pontos de cada partida, já em ordem.

    A linha de número destaque (0 = a primeira) fica amarela.
    """
    pygame.draw.rect(superficie, DARK_GRAY, retangulo)
    pygame.draw.rect(superficie, GRAY, retangulo, 2)
    desenhar_texto(superficie, "RANKING", (retangulo.centerx, retangulo.y + 16), YELLOW, 32, centralizado=True)
    if len(partidas) == 0:
        desenhar_texto(superficie, "Ninguém jogou", (retangulo.centerx, retangulo.y + 60), GRAY, 28,
                       centralizado=True)
        return
    for i, partida in enumerate(partidas):
        y = retangulo.y + 36 + i * 24
        cor = WHITE
        if i == destaque:
            cor = YELLOW
        desenhar_texto(superficie, f"{i + 1}. {partida['nome'][:8]}", (retangulo.x + 8, y), cor, 28)
        pontos = str(partida["pontos"])
        largura = fonte(28).size(pontos)[0]            # para encostar os pontos na borda direita
        desenhar_texto(superficie, pontos, (retangulo.right - 8 - largura, y), cor, 28)
    
def desenhar_barra(superficie, retangulo, valor, maximo, cor):
    """Barra de vida: a parte colorida mostra quanto sobra de valor, de 0 até maximo."""
    pygame.draw.rect(superficie, DARK_GRAY, retangulo)
    cheia = retangulo.copy()
    cheia.width = round(retangulo.width * max(0, valor) / maximo)
    pygame.draw.rect(superficie, cor, cheia)
    pygame.draw.rect(superficie, WHITE, retangulo, 2)