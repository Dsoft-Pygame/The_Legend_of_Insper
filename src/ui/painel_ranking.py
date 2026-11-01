"""Classe PainelRanking: o quadro que mostra o ranking.

O que é:
    Só desenha. Não lê nem salva arquivo; quem faz isso é o Ranking.

Atributos:
    - retangulo: pygame.Rect. Posição e tamanho do quadro na tela.

Métodos:
    - desenhar(superficie: pygame.Surface, lista: list[Partida],
      destaque: int | None) -> None: desenha o título e uma linha por
      partida (posição, nome, pontos). Se receber um destaque, pinta essa
      linha de outra cor (quem acabou de jogar).

Usada em: TelaInicial e TelaResultado.
"""
