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
from __future__ import annotations

import math
from typing import TYPE_CHECKING, Iterable

from personagens.tipos import EntidadeId, Lado

if TYPE_CHECKING:
    from mapa.mapa import Mapa
    from personagens.personagem import Personagem
    from personagens.projetil import Projetil

TAMANHO_SUBPASSO = 8    # pixels: menor que meia parede (16), então nada atravessa


def disparar_ataques(personagens: Iterable[Personagem]) -> list[Projetil]:
    novos: list[Projetil] = []
    for p in personagens:
        if p.quer_atacar and p.pode_atacar():
            novos.extend(p.ataque.executar(p))
            p.recarga_ataque = p.ataque.recarga
            p.mudar_acao("atacando")
        if p.quer_especial and p.pode_especial():
            novos.extend(p.ataque_especial.executar(p))
            p.recarga_especial = p.ataque_especial.recarga
            p.mudar_acao("especial")
        p.quer_atacar = False           # o pedido vale só para este tick
        p.quer_especial = False
    return novos


def mover_projeteis(projeteis: Iterable[Projetil], mapa: Mapa, dt: float) -> list[EntidadeId]:
    sumir: list[EntidadeId] = []
    for projetil in projeteis:
        projetil.caixas_do_tick = [projetil.caixa]          # onde ele começou
        if projetil.velocidade.length() == 0:
            projetil.avancar(dt)                            # golpe parado: só desconta a duração
        else:
            deslocamento = projetil.velocidade.length() * dt
            subpassos = max(1, math.ceil(deslocamento / TAMANHO_SUBPASSO))
            for _ in range(subpassos):
                projetil.avancar(dt / subpassos)
                if not mapa.area_livre(projetil.caixa):
                    sumir.append(projetil.id)               # bateu na parede
                    break
                projetil.caixas_do_tick.append(projetil.caixa)
        if projetil.acabou() and projetil.id not in sumir:
            sumir.append(projetil.id)
    return sumir


def aplicar_acertos(projeteis: Iterable[Projetil], personagens: Iterable[Personagem]) -> list[EntidadeId]:
    sumir: list[EntidadeId] = []
    alvos = list(personagens)                               # vai percorrer várias vezes
    for projetil in projeteis:
        for alvo in alvos:
            if alvo.lado == projetil.lado or not alvo.esta_vivo or alvo.id in projetil.ja_acertou:
                continue
            if any(caixa.colliderect(alvo.caixa) for caixa in projetil.caixas_do_tick):
                projetil.ja_acertou.add(alvo.id)
                alvo.receber_dano(projetil.dano, projetil.dono)
                if not projetil.atravessa:
                    sumir.append(projetil.id)
                    break                                   # não acerta mais ninguém
    return sumir


def aplicar_contato(personagens: Iterable[Personagem]) -> None:
    todos = list(personagens)
    monstros = [p for p in todos if p.lado == Lado.MONSTROS and p.esta_vivo and p.dano_contato > 0]
    herois = [p for p in todos if p.lado == Lado.HEROIS and p.esta_vivo]
    for monstro in monstros:
        for heroi in herois:
            if monstro.caixa.colliderect(heroi.caixa):
                heroi.receber_dano(monstro.dano_contato, monstro.id)
