"""combate.py: ataques, projéteis, colisões e dano.

O que é:
    A parte do tick que antes ficava dentro do Nivel ("checa colisões").
    Fica num arquivo próprio para o Nivel continuar curto e para as regras
    de dano estarem num lugar só. Nenhuma função daqui desenha ou lê
    entrada.

Funções:
    - disparar_ataques(personagens: Iterable[Personagem]) -> list[Projetil]:
      para cada personagem que pediu ataque ou especial e pode, chama o
      Ataque dele, começa a recarga, chama mudar_acao("atacando") ou
      mudar_acao("especial") e devolve os projéteis criados (cada um
      nasce com colocar_em, sem posição anterior).
    - mover_projeteis(projeteis: Iterable[Projetil], mapa: Mapa,
      dt: float) -> list[EntidadeId]: avança cada projétil e devolve os
      que devem sumir (bateram em parede, segundo mapa.area_livre, ou
      acabou a duração). A 20 ticks por segundo, um projétil a 200 px/s
      anda 10 px por tick; acima de meio tile por tick (8 px), ele anda
      em subpassos de no máximo 8 px, conferindo a parede em cada um,
      para não atravessar uma parede de 16 px sem encostar nela.
    - aplicar_acertos(projeteis: Iterable[Projetil],
      personagens: Iterable[Personagem]) -> list[EntidadeId]: projétil que
      encosta em alguém do outro lado dá dano (uma vez por alvo; quem
      leva dano faz mudar_acao("atingido")); devolve
      os projéteis que somem (os que não atravessam). Usa as mesmas
      posições dos subpassos, para um projétil rápido não pular um alvo.
    - aplicar_contato(personagens: Iterable[Personagem]) -> None: monstro
      com dano_contato que encosta num herói dá dano. A invulnerabilidade
      do herói evita dano a cada tick.

Quem usa: Nivel, na etapa resolver_combate.
Usa: personagens/, mapa/mapa.py.
"""
