"""Classe CarregadorTexto (implementa CarregadorMapa): mapa escrito à mão.

O que é:
    Lê um arquivo de texto de data/mapas/ em que cada caractere é um tile
    e devolve um MapaTiles:
        #  parede
        .  chão
        H  onde os heróis aparecem (o P1 no primeiro H, o P2 no segundo,
           ou ao lado do primeiro se só houver um)
        I  onde um inimigo pode aparecer
        C  onde o chefe aparece
        S  saída
    Os marcadores H, I e C viram chão depois de lidos.

Métodos:
    - carregar(origem: str) -> Mapa: lê data/<origem>. Linhas de tamanhos
      diferentes ou caractere desconhecido geram erro com o número da linha.

Trocar por mapas do Tiled depois = um CarregadorTiled novo, sem mudar o
resto do jogo.

Quem usa: Mundo (pelo registro de mapas).
"""
