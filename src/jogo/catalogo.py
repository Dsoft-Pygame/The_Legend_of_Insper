"""Classe Catalogo: lê e confere todo o conteúdo de data/ ao abrir o jogo.

O que é:
    Carrega classes.json, inimigos.json, temas.json, controles.json e
    aparencias.json uma vez só e transforma cada entrada numa definição
    (dataclass congelada). Se faltar um campo, ou um nome não existir nos
    registros (ex.: "decisao": {"tipo": "persegir"}), dá erro na hora, com
    o arquivo e a entrada, e não no meio da partida (o jogo não pode
    travar na feira). O formato de cada arquivo está em data/README.md.

DefinicaoInimigo (dataclass congelada): nome, vida, velocidade,
dano_contato, pontos, chefe, raio_visao, movimento, decisao, ataque,
especial, aparencia.

DefinicaoNivel (dataclass congelada): nome, carregador, mapa,
inimigos: dict[str, int] (tipo e quantidade), chefe: str | None.

DefinicaoTema (dataclass congelada): nome, direcao ("sobe" ou "desce"),
niveis: tuple[DefinicaoNivel, ...].

Atributos:
    - classes: dict[str, ClasseHeroi].
    - inimigos: dict[str, DefinicaoInimigo].
    - temas: dict[str, DefinicaoTema].
    - tema_padrao: str.
    - controles: dict. Teclas e botões por dispositivo (a entrada/ usa).
    - aparencias: dict. Cor ou sprite por chave (o render/ usa).

Métodos:
    - carregar(pasta: Path) -> Catalogo (classmethod).

Quem usa: Aplicacao (cria uma vez), Fabrica, Mundo, TelaClasses,
GerenciadorDispositivos, Aparencias.
"""
