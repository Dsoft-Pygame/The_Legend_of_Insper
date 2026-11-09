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


from dataclasses import dataclass

from personagens.tipos import EntidadeId, Lado


@dataclass(frozen=True)
class PersonagemDerrotado:
    id: EntidadeId                      # quem morreu
    lado: Lado                          # HEROIS ou MONSTROS
    nome: str                           # "Slime", "Mago", ...
    pontos: int                         # quanto vale (0 nos heróis)
    chefe: bool                         # derrotar o chefe vence a partida
    derrotado_por: EntidadeId | None    # quem deu o último golpe


@dataclass(frozen=True)
class HeroiNaSaida:
    id: EntidadeId                      # o herói que pisou na saída


Evento = PersonagemDerrotado | HeroiNaSaida   # "um evento é um desses dois"
