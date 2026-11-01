"""registro.py: os tipos de ataque que podem ser usados nos dados.

O que é:
    Um dicionário ATAQUES: dict[str, Callable[..., Ataque]] que liga o
    "tipo" usado nos JSON à classe:
        "projetil" -> AtaqueProjetil
        "golpe"    -> AtaqueGolpe

Funções:
    - criar_ataque(config: dict) -> Ataque: lê {"tipo": ..., parâmetros}
      e cria o ataque. Tipo desconhecido gera erro na abertura do jogo.

Um tipo de ataque novo (ex.: armadilha no chão) = um arquivo nesta pasta
+ uma linha aqui.

Quem usa: Fabrica e Catalogo (para conferir os nomes).
"""
