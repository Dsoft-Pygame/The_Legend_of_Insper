"""Classe MovimentoLivre: top-down contínuo, em qualquer direção.

O que é:
    O movimento padrão. Anda intencao * velocidade * dt pixels por tick.
    Move primeiro no eixo x e depois no y, cada um conferindo
    mapa.area_livre(caixa). Assim, encostado numa parede, o personagem
    desliza ao longo dela em vez de travar.

    Se o passo inteiro de um eixo bate em algo, o personagem não fica
    parado onde está: avança de pixel em pixel até encostar. Sem isso, com
    passos de 3 a 5 px por tick, ele parava a 1, 2 ou 3 px da parede,
    cada vez numa distância diferente.

    Empurrando reto contra uma quina (ex.: entrada de corredor), se
    desviar até TOLERANCIA_QUINA px para o lado libera o caminho, ele
    escorrega para esse lado em vez de ficar preso na ponta da parede.

Métodos:
    - atualizar(corpo: Corpo, mapa: Mapa, dt: float) -> None.

Quem usa: personagens com "movimento": "livre" (pelo registro).
"""
from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from movimento.movimento import Corpo, caixa_em, pixel



if TYPE_CHECKING:
    from mapa.mapa import Mapa

TOLERANCIA_QUINA = 4  # px que o personagem pode ser desviado para contornar uma quina

class MovimentoLivre:
    def atualizar(self, corpo: Corpo, mapa: Mapa, dt: float) -> None:
        deslocamento = corpo.intencao * corpo.velocidade * dt

        bateu_x = self._andar(corpo, mapa, 0, deslocamento.x) # Tenta mover no eixo x
        bateu_y = self._andar(corpo, mapa, 1, deslocamento.y) # Tenta mover no eixo y

        # Só contorna quina quando empurra reto (na diagonal já desliza sozinho)
        if bateu_x and deslocamento.y == 0:
            self._contornar_quina(corpo, mapa, 0, deslocamento.x)
        if bateu_y and deslocamento.x == 0:
            self._contornar_quina(corpo, mapa, 1, deslocamento.y)

        corpo.intencao = pygame.Vector2(0, 0) # Zera a intenção para o próximo tick

    def _livre(self, corpo: Corpo, mapa: Mapa, posicao: pygame.Vector2) -> bool:
        return mapa.area_livre(caixa_em(posicao, corpo.tamanho))

    def _andar(self, corpo: Corpo, mapa: Mapa, eixo: int, distancia: float) -> bool:
        """Anda no eixo (0 = x, 1 = y). Devolve True se bateu em algo."""
        if distancia == 0:
            return False

        nova = corpo.posicao.copy()
        nova[eixo] += distancia
        if self._livre(corpo, mapa, nova):
            corpo.posicao[eixo] = nova[eixo]
            return False

        # Bateu: avança pixel a pixel até encostar. O pixel do destino já
        # sabemos que está bloqueado, então para antes dele.
        sentido = 1 if distancia > 0 else -1
        inicio = pixel(corpo.posicao[eixo])
        encostado = inicio
        teste = corpo.posicao.copy()
        for centro in range(inicio + sentido, pixel(nova[eixo]), sentido):
            teste[eixo] = centro
            if not self._livre(corpo, mapa, teste):
                break
            encostado = centro
        corpo.posicao[eixo] = encostado   # inteiro: a caixa fica colada, sem sobra de fração
        return True

    def _contornar_quina(self, corpo: Corpo, mapa: Mapa, eixo: int, distancia: float) -> None:
        """Bateu em `eixo` empurrando reto: procura o menor desvio lateral
        que libera o caminho e escorrega até lá (no máximo o passo do tick)."""
        lateral = 1 - eixo
        sentido = 1 if distancia > 0 else -1
        passo = abs(distancia)

        teste = pygame.Vector2(pixel(corpo.posicao.x), pixel(corpo.posicao.y))
        teste[eixo] += sentido                       # 1 px à frente
        base = teste[lateral]
        for desvio in range(1, TOLERANCIA_QUINA + 1):
            for lado in (-1, 1):
                teste[lateral] = base + lado * desvio
                if self._livre(corpo, mapa, teste):
                    self._andar(corpo, mapa, lateral, lado * min(passo, desvio))
                    return
