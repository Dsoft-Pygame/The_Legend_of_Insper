"""Classe AtaqueProjetil: atira um ou mais projéteis.

O que é:
    Cobre todos os ataques à distância, só mudando os parâmetros:
        - flecha do arqueiro: quantidade 1, abertura 0;
        - tiro triplo do arqueiro: quantidade 3, abertura 30 graus;
        - bola de fogo do mago: quantidade 1, velocidade baixa, dano alto;
        - anel de fogo do mago e tiros do chefe: quantidade 12,
          abertura 360 graus.

Parâmetros (vêm de data/classes.json ou data/inimigos.json):
    - recarga: float.
    - dano: int.
    - velocidade: float. Pixels por segundo.
    - duracao: float. Segundos até o projétil sumir.
    - quantidade: int.
    - abertura: float. Ângulo total do leque, em graus, centrado na
      direção do olhar.
    - tamanho: int. Lado da caixa do projétil, em pixels.
    - aparencia: str. Chave para o render ("flecha", "bola_fogo").

Métodos:
    - executar(atacante: Personagem) -> list[Projetil].

Quem usa: Fabrica (pelo tipo "projetil" no registro).
"""
