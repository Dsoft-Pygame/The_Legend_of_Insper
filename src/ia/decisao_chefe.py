"""Classe DecisaoChefe: o comportamento do chefe, em duas fases.

O que é:
    Antes era Chefe.pensar(jogador). Agora o chefe é um Personagem comum
    (com muita vida e "chefe": true em data/inimigos.json), e todo o jeito
    dele de lutar mora aqui.

Fases (a fase sai da própria Visao: vida dividida por vida_maxima):
    - Fase 1, vida acima da metade: persegue devagar o herói mais próximo
      (Mover com tamanho lentidao_fase_1) e pede Atacar() quando perto.
    - Fase 2, vida na metade ou menos: persegue na velocidade toda e, a
      cada intervalo_especial segundos, pede Especial(). No chefe, o
      especial é um anel de projéteis em todas as direções, definido em
      data/inimigos.json, não aqui.

Parâmetros (vêm do campo "decisao" em data/inimigos.json):
    - intervalo_especial: float.
    - lentidao_fase_1: float. Fração da velocidade na fase 1 (ex.: 0.5).
    - distancia_ataque: float.

Memória:
    - tempo_ate_especial: float.

Métodos:
    - decidir(visao: Visao, gerador: random.Random) -> list[Comando].

Quem usa: ControladorIA (pelo nome "chefe" no registro).
Usa: personagens/visao.py, controle/comandos.py.
"""
