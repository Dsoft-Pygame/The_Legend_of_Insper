"""Classe Projetil (herda de Entidade): tudo que voa (ou não) e dá dano.

Exemplos: flecha do arqueiro, bola de fogo do mago, tiros do chefe.

    O golpe corpo a corpo (machado do bárbaro) também é um Projetil: um
    projétil parado (velocidade zero) que dura uma fração de segundo na
    frente de quem atacou. Assim o combate trata tudo do mesmo jeito.

Atributos:
    - lado: Lado. De quem é; nunca acerta o próprio lado.
    - dono: EntidadeId. Quem atirou (para saber quem derrotou quem).
    - velocidade: pygame.Vector2. Direção e rapidez, em pixels por segundo.
    - dano: int.
    - duracao: float. Segundos até sumir sozinho.
    - atravessa: bool. Se True, continua depois de acertar (giro do
      bárbaro); se False, some no primeiro acerto.
    - ja_acertou: set[EntidadeId]. Para não acertar o mesmo alvo duas vezes.

Métodos:
    - avancar(dt: float) -> None: anda em linha reta e desconta a duração.
    - acabou() -> bool: a duração chegou a zero.

Some ao bater numa parede ou acertar alguém: quem decide isso é o
combate (jogo/combate.py), perguntando ao Mapa.

Quem cria: os ataques (personagens/ataques/).
Quem usa: Nivel, jogo/combate.py, render (só lê).
"""
