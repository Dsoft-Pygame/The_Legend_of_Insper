"""registro.py: os movimentos que podem ser usados nos dados.

O que é:
    Um dicionário MOVIMENTOS: dict[str, Callable[..., Movimento]]:
        "livre" -> MovimentoLivre
        "grade" -> MovimentoGrade

    O campo "movimento" em data/classes.json e data/inimigos.json escolhe
    qual usar. Pode ser só o nome ("livre") ou um objeto com parâmetros
    ({"tipo": "grade", "tamanho_passo": 16}).

Funções:
    - criar_movimento(config: str | dict) -> Movimento.

Um movimento novo (ex.: com inércia e atrito) = um arquivo nesta pasta +
uma linha aqui.

Quem usa: Fabrica e Catalogo (para conferir os nomes).
"""
from typing import Callable
from movimento.movimento import Movimento
from movimento.movimento_livre import MovimentoLivre



MOVIMENTOS: dict[str, Callable[..., Movimento]] = {"livre": MovimentoLivre}

def criar_movimento(config: str | dict) -> Movimento:
    if isinstance(config, str):
        tipo = config
        parametros = {}
    else:
        tipo = config["tipo"]
        parametros = {
            chave: valor
            for chave, valor in config.items()
            if chave != "tipo"
        }

    if tipo not in MOVIMENTOS:
        raise ValueError(
            f"Movimento desconhecido: '{tipo}'. "
            f"Opções: {', '.join(MOVIMENTOS)}"
        )

    return MOVIMENTOS[tipo](**parametros)