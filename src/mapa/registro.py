"""registro.py: os carregadores de mapa que podem ser usados nos dados.

O que é:
    Um dicionário CARREGADORES: dict[str, Callable[[], CarregadorMapa]]:
        "texto" -> CarregadorTexto

    Cada nível em data/temas.json diz o carregador e a origem, por exemplo
    {"carregador": "texto", "mapa": "mapas/nivel_1.txt"}. Um gerador
    procedural ou um leitor do Tiled entra com uma linha aqui.

Funções:
    - criar_carregador(nome: str) -> CarregadorMapa.

Quem usa: Mundo e Catalogo (para conferir os nomes).
"""
from typing import Callable

from mapa.carregador_texto import CarregadorTexto
from mapa.mapa import CarregadorMapa

CARREGADORES: dict[str, Callable[[], CarregadorMapa]] = {"texto": CarregadorTexto}


def criar_carregador(nome: str) -> CarregadorMapa:
    if nome not in CARREGADORES:
        raise ValueError(f"Carregador de mapa desconhecido: '{nome}'. Opções: {', '.join(CARREGADORES)}")
    return CARREGADORES[nome]()
