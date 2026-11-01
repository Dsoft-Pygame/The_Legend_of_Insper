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
