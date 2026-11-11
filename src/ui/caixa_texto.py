"""Classe CaixaTexto: campo para digitar o nome do jogador.

O que é:
    Um retângulo na tela onde aparece o que o jogador digita, com um
    cursor piscando no final. Não lê o teclado: a TelaInicial entrega o
    texto digitado e o APAGAR que vieram na EntradaMenu.

Atributos:
    - texto: str. O que já foi digitado.
    - tamanho_maximo: int. Quantas letras cabem no nome.
    - retangulo: pygame.Rect. Posição e tamanho da caixa na tela.

Métodos:
    - digitar(letras: str) -> None: acrescenta as letras, ignorando
      caracteres estranhos e o que passar do tamanho máximo.
    - apagar() -> None: tira a última letra.
    - desenhar(superficie: pygame.Surface, cursor_visivel: bool) -> None:
      desenha a caixa, o texto e o cursor.

Usada em: TelaInicial.
"""


import pygame

from settings import DARK_GRAY, WHITE, YELLOW
from ui.texto import desenhar_texto

CARACTERES_EXTRAS = " -_"     # além de letras e números, só estes são aceitos

class CaixaTexto:
    def __init__(self, retangulo: pygame.Rect, tamanho_maximo: int = 12) -> None:
        self.retangulo = retangulo
        self.tamanho_maximo = tamanho_maximo
        self.texto = ""

    def digitar(self, letras: str) -> None:
        for letra in letras:
            if len(self.texto) >= self.tamanho_maximo:
                break
            if letra.isalnum() or letra in CARACTERES_EXTRAS:
                self.texto += letra
    def apagar(self) -> None:
        self.texto = self.texto[:-1]

    def limpar(self) -> None:
        self.texto = ""

    def desenhar(self, superficie: pygame.Surface, cursor_visivel: bool) -> None:
        pygame.draw.rect(superficie, DARK_GRAY, self.retangulo)
        pygame.draw.rect(superficie, WHITE, self.retangulo, 1)
        area = desenhar_texto(superficie, self.texto, (self.retangulo.x + 3, self.retangulo.y + 3))
        if cursor_visivel:
            x = area.right + 1 if self.texto else self.retangulo.x + 3
            pygame.draw.line(superficie, YELLOW, (x, self.retangulo.y + 3), (x, self.retangulo.bottom - 4))
