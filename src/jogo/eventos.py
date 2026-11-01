"""Eventos da partida: o que aconteceu num tick, guardado como dado.

O que é:
    O Nivel não soma pontos nem decide vitória; ele só conta o que
    aconteceu, devolvendo uma lista de eventos (dataclasses congeladas),
    do mesmo jeito que o matar_animais da simulação devolve a lista de
    mortos. O Mundo lê a lista e aplica as regras. Se um dia tiver som ou
    conquistas, eles leem a mesma lista.

Eventos:
    - PersonagemDerrotado: id, lado, nome, pontos, chefe: bool,
      derrotado_por: EntidadeId | None (quem deu o último golpe; serve
      para pontos por jogador no co-op).
    - HeroiNaSaida: id do herói.

Evento = PersonagemDerrotado | HeroiNaSaida (apelido de tipo).

Quem cria: Nivel.
Quem usa: Mundo.
"""
