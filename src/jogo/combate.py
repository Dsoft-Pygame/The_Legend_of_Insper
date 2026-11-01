"""combate.py: ataques, projéteis, colisões e dano.

O que é:
    A parte do tick que antes ficava dentro do Nivel ("checa colisões").
    Fica num arquivo próprio para o Nivel continuar curto e para as regras
    de dano estarem num lugar só. Nenhuma função daqui desenha ou lê
    entrada.

Funções:
    - disparar_ataques(personagens: Iterable[Personagem]) -> list[Projetil]:
      para cada personagem que pediu ataque ou especial e pode, chama o
      Ataque dele, começa a recarga e devolve os projéteis criados.
    - mover_projeteis(projeteis: Iterable[Projetil], mapa: Mapa,
      dt: float) -> list[EntidadeId]: avança cada projétil e devolve os
      que devem sumir (bateram em parede, segundo mapa.area_livre, ou
      acabou a duração).
    - aplicar_acertos(projeteis: Iterable[Projetil],
      personagens: Iterable[Personagem]) -> list[EntidadeId]: projétil que
      encosta em alguém do outro lado dá dano (uma vez por alvo); devolve
      os projéteis que somem (os que não atravessam).
    - aplicar_contato(personagens: Iterable[Personagem]) -> None: monstro
      com dano_contato que encosta num herói dá dano. A invulnerabilidade
      do herói evita dano a cada tick.

Quem usa: Nivel, na etapa resolver_combate.
Usa: personagens/, mapa/mapa.py.
"""
