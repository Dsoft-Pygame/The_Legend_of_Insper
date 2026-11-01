"""Interfaces Corpo e Movimento (typing.Protocol): o jeito de andar.

O que é:
    O jeito como um personagem anda (livre, de tile em tile, com física,
    voando) fica numa estratégia separada. O Personagem guarda um
    Movimento, e dá para trocar sem reescrever o personagem: basta
    entregar outro, por exemplo um MovimentoGrade de 16 pixels.

    O Movimento não conhece o Personagem inteiro, só o Corpo (o pedaço de
    que precisa), e não conhece o formato do mapa: só pergunta ao Mapa se
    uma área está livre.

Corpo (interface):
    - posicao: pygame.Vector2. Centro, em pixels do mapa.
    - tamanho: pygame.Vector2.
    - velocidade: float. Pixels por segundo.
    - intencao: pygame.Vector2. O que mover() pediu neste tick, com
      tamanho de 0 a 1 (meio analógico = meia velocidade).

Movimento (interface):
    - atualizar(corpo: Corpo, mapa: Mapa, dt: float) -> None: move o corpo
      de acordo com a intenção, sem atravessar o que o mapa diz que é
      sólido, e zera a intenção.

Implementações: MovimentoLivre (padrão) e MovimentoGrade.
Quem usa: Personagem (guarda), Nivel (chama na etapa mover_personagens).
"""
