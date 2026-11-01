"""Classe MovimentoLivre: top-down contínuo, em qualquer direção.

O que é:
    O movimento padrão. Anda intencao * velocidade * dt pixels por tick.
    Move primeiro no eixo x e depois no y, cada um conferindo
    mapa.area_livre(caixa). Assim, encostado numa parede, o personagem
    desliza ao longo dela em vez de travar.

Métodos:
    - atualizar(corpo: Corpo, mapa: Mapa, dt: float) -> None.

Quem usa: personagens com "movimento": "livre" (pelo registro).
"""
