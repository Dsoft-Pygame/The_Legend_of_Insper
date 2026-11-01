"""Classe AtaqueGolpe: golpe corpo a corpo numa área.

O que é:
    Cria um Projetil parado (velocidade zero) que dura uma fração de
    segundo:
        - golpe de machado do bárbaro: forma "frente", uma área pequena na
          frente de quem atacou;
        - giro do bárbaro: forma "volta", uma área em volta dele que
          atravessa (acerta todo mundo dentro).

Parâmetros (vêm de data/classes.json ou data/inimigos.json):
    - recarga: float.
    - dano: int.
    - alcance: int. Tamanho da área, em pixels.
    - forma: str. "frente" ou "volta".
    - duracao: float.
    - aparencia: str.

Métodos:
    - executar(atacante: Personagem) -> list[Projetil].

Quem usa: Fabrica (pelo tipo "golpe" no registro).
"""
