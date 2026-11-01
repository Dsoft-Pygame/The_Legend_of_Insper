"""Interface Ataque (typing.Protocol): o que acontece quando alguém ataca.

O que é:
    Uma estratégia trocável, como o Movimento. O Personagem guarda um
    Ataque para o ataque básico e outro para o especial. Na etapa
    resolver_combate do Nivel, se o personagem pediu e pode atacar, o
    combate chama executar e põe no nível os projéteis que voltaram.

    Ataques são compartilhados entre heróis e inimigos: o anel de fogo do
    Mago e os tiros em todas as direções do chefe são o mesmo
    AtaqueProjetil com parâmetros diferentes.

Atributos:
    - recarga: float. Segundos entre um uso e outro.

Métodos:
    - executar(atacante: Personagem) -> list[Projetil]: cria os projéteis
      a partir da posição, do lado e da direção do olhar do atacante.

Implementações: AtaqueProjetil e AtaqueGolpe.
Quem usa: Personagem (guarda), jogo/combate.py (chama), Fabrica (cria
pelo registro).
"""
