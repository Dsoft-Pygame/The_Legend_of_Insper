"""Classe MovimentoGrade: anda de tile em tile, estilo Pokémon antigo.

O que é:
    Ao receber uma intenção, escolhe a direção principal (cima, baixo,
    esquerda ou direita), confere se o próximo tile está livre e anda até
    o centro dele. Enquanto não chega, ignora novas intenções. Parado no
    centro de um tile e sem intenção, fica parado.

Atributos:
    - tamanho_passo: int. Tamanho do tile em pixels (16).
    - destino: pygame.Vector2 | None. Centro do tile para onde está indo.

Métodos:
    - atualizar(corpo: Corpo, mapa: Mapa, dt: float) -> None.

Quem usa: personagens com "movimento": {"tipo": "grade"} (pelo registro).
"""
