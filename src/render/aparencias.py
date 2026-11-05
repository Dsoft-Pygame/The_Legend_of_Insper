"""Classe Aparencias: transforma a chave de aparência em algo desenhável.

O que é:
    As entidades e o mapa guardam só chaves ("slime", "mago", "parede").
    Esta classe guarda, para cada chave, uma cor RGB de settings.py (até
    ter arte), um sprite parado de assets/ ou uma folha de sprites com
    animações. Trocar toda a arte do jogo é mexer em data/aparencias.json
    e em assets/, sem tocar em nenhuma entidade.

Atributos:
    - cores: dict[str, tuple[int, int, int]].
    - sprites: dict[str, pygame.Surface]. Carregados uma vez só.
    - animacoes: dict[str, ConjuntoAnimacoes]. Para as chaves que têm
      folha de sprites.
    - padrao: tuple[int, int, int]. Cor gritante (magenta) para chave
      desconhecida, como a cor de inconsistência da simulação: se algo
      aparecer magenta, falta a aparência dele no JSON.

Métodos:
    - carregar(config: dict) -> Aparencias (classmethod): lê o que veio de
      data/aparencias.json.
    - obter(chave: str) -> pygame.Surface | tuple[int, int, int]: a imagem
      parada (mapa, cartões das classes).
    - quadro(chave: str, acao: str, tempo: float)
      -> pygame.Surface | tuple[int, int, int]: se a chave tem animações,
      ConjuntoAnimacoes.escolher(acao).quadro_em(tempo); se não, obter(chave).
      Quem ainda é só uma cor continua funcionando igual.

Quem usa: RenderizadorNivel e CartaoClasse.
Usa: render/animacoes.py, settings.py, assets/.
"""
from pathlib import Path
import pygame
from settings import MAGENTA, PASTA_ASSETS
Visual = pygame.Surface | tuple[int, int, int]   # uma imagem OU uma cor RGB

import settings
from settings import MAGENTA, PASTA_ASSETS


class Aparencias:
    def __init__(self) -> None:
        self.cores: dict[str, tuple[int, int, int]] = {}
        self.sprites: dict[str, pygame.Surface] = {}
        self.animacoes: dict = {}
        self.padrao = MAGENTA

    @classmethod
    def carregar(cls, config: dict, pasta_assets: Path = PASTA_ASSETS) -> "Aparencias":
        aparencias = cls()

        for chave, entrada in config.items():
            if "cor" in entrada:
                if not hasattr(settings, entrada["cor"]):
                    raise ValueError(
                        f"aparencias.json, '{chave}': a cor "
                        f"'{entrada['cor']}' não existe no settings.py"
                    )

                aparencias.cores[chave] = getattr(settings, entrada["cor"])

            if "sprite" in entrada:
                aparencias.sprites[chave] = pygame.image.load(
                    pasta_assets / entrada["sprite"]
                ).convert_alpha()

            if "folha" in entrada:
                # folhas de animação: T62
                pass

        return aparencias

    def obter(self, chave: str) -> Visual:
        if chave in self.sprites:
            return self.sprites[chave]

        return self.cores.get(chave, self.padrao)

    def quadro(self, chave: str, acao: str, tempo: float) -> Visual:
        return self.obter(chave)


def desenhar_visual(
    superficie: pygame.Surface,
    visual: Visual,
    retangulo: pygame.Rect,
    espelhar: bool = False
) -> None:
    if isinstance(visual, pygame.Surface):
        if espelhar:
            visual = pygame.transform.flip(visual, True, False)

        superficie.blit(visual, visual.get_rect(center=retangulo.center))
    else:
        pygame.draw.rect(superficie, visual, retangulo)