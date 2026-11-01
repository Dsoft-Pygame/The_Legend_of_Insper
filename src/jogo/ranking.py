"""Classe Ranking: o placar da feira.

O que é:
    Guarda todas as partidas num arquivo, para o ranking continuar lá
    mesmo depois de fechar o jogo. Só lê e salva; quem desenha é o
    PainelRanking (ui/).

Partida (dataclass congelada):
    - nome: str. No co-op, os nomes juntos ("Ana e Beto").
    - classe: str. No co-op, as classes juntas.
    - pontos: int.
    - venceu: bool.

Atributos:
    - caminho_arquivo: Path. Onde salvar (src/data/ranking.json).
    - partidas: list[Partida]. Em ordem do maior para o menor.

Métodos:
    - carregar() -> None: lê o arquivo ao abrir o jogo. Se não existir ou
      estiver estragado, começa com a lista vazia (o jogo não pode travar
      na feira).
    - adicionar(partida: Partida) -> int: coloca a partida na lista,
      ordena, salva e devolve a posição em que ficou.
    - melhores(quantidade: int) -> list[Partida]: os primeiros colocados.
    - salvar() -> None: grava a lista no arquivo.

Quem usa: Aplicacao (cria uma vez), TelaInicial e TelaResultado.
"""
