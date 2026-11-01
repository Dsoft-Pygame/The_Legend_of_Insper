"""Classe Aparencias: transforma a chave de aparência em algo desenhável.

O que é:
    As entidades e o mapa guardam só chaves ("slime", "mago", "parede").
    Esta classe guarda, para cada chave, uma cor RGB de settings.py (até
    ter arte) ou um sprite de assets/. Trocar toda a arte do jogo é mexer
    em data/aparencias.json e em assets/, sem tocar em nenhuma entidade.

Atributos:
    - cores: dict[str, tuple[int, int, int]].
    - sprites: dict[str, pygame.Surface]. Carregados uma vez só.
    - padrao: tuple[int, int, int]. Cor gritante (magenta) para chave
      desconhecida, como a cor de inconsistência da simulação: se algo
      aparecer magenta, falta a aparência dele no JSON.

Métodos:
    - carregar(config: dict) -> Aparencias (classmethod): lê o que veio de
      data/aparencias.json.
    - obter(chave: str) -> pygame.Surface | tuple[int, int, int].

Quem usa: RenderizadorNivel e CartaoClasse.
Usa: settings.py, assets/.
"""
