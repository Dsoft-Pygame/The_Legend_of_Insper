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


import json
from dataclasses import asdict, dataclass
from pathlib import Path

from settings import PASTA_DATA


@dataclass(frozen=True)
class Partida:
    nome: str
    classe: str
    pontos: int
    venceu: bool


class Ranking:
    def __init__(self, caminho_arquivo: Path = PASTA_DATA / "ranking.json") -> None:
        self.caminho_arquivo = Path(caminho_arquivo)
        self.partidas: list[Partida] = []

    def carregar(self) -> None:
        try:
            dados = json.loads(self.caminho_arquivo.read_text(encoding="utf-8"))
            self.partidas = [Partida(**item) for item in dados]
        except (OSError, json.JSONDecodeError, TypeError):
            self.partidas = []

        self.partidas.sort(key=lambda p: p.pontos, reverse=True)

    def adicionar(self, partida: Partida) -> int:
        self.partidas.append(partida)
        self.partidas.sort(key=lambda p: p.pontos, reverse=True)
        self.salvar()

        for i, p in enumerate(self.partidas, start=1):
            if p is partida:
                return i

        raise RuntimeError("Partida não encontrada no ranking.")

    def melhores(self, quantidade: int) -> list[Partida]:
        return self.partidas[:quantidade]

    def salvar(self) -> None:
        self.caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

        self.caminho_arquivo.write_text(
            json.dumps([asdict(p) for p in self.partidas], ensure_ascii=False, indent=2), encoding="utf-8",)

