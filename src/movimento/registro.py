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
