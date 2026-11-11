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
