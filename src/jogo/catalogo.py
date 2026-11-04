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


import json
from dataclasses import dataclass
from pathlib import Path

from personagens.classe_heroi import ClasseHeroi
from settings import PASTA_DATA


class ErroDados(Exception):
    """Erro num arquivo de data/: diz o arquivo, a entrada e o que está errado."""


@dataclass(frozen=True)
class DefinicaoInimigo:
    nome: str
    vida: int
    velocidade: float
    dano_contato: int
    pontos: int
    raio_visao: float
    movimento: str | dict
    decisao: dict
    aparencia: str
    chefe: bool = False
    ataque: dict | None = None
    especial: dict | None = None


@dataclass(frozen=True)
class DefinicaoNivel:
    nome: str
    carregador: str
    mapa: str
    inimigos: dict[str, int]
    chefe: str | None = None


@dataclass(frozen=True)
class DefinicaoTema:
    nome: str
    direcao: str
    niveis: tuple[DefinicaoNivel, ...]


class Catalogo:
    def __init__(self, classes: dict[str, ClasseHeroi], inimigos: dict[str, DefinicaoInimigo], temas: dict[str, DefinicaoTema], tema_padrao: str, controles: dict, aparencias: dict) -> None:
        self.classes = classes
        self.inimigos = inimigos
        self.temas = temas
        self.tema_padrao = tema_padrao
        self.controles = controles
        self.aparencias = aparencias

    @classmethod
    def carregar(cls, pasta: Path = PASTA_DATA) -> "Catalogo":
        def ler(nome_arquivo: str) -> dict:
            caminho = pasta / nome_arquivo
            try:
                return json.loads(caminho.read_text(encoding="utf-8"))
            except FileNotFoundError:
                raise ErroDados(f"{nome_arquivo}: arquivo não encontrado em {pasta}")
            except json.JSONDecodeError as erro:
                raise ErroDados(f"{nome_arquivo}: JSON inválido na linha " f"{erro.lineno}: {erro.msg}")
        
        classes = {chave: ClasseHeroi(**dados) for chave, dados in ler("classes.json").items()}
        inimigos = {chave: DefinicaoInimigo(**dados) for chave, dados in ler("inimigos.json").items()}
        dados_temas = ler("temas.json")
        temas = {}

        for chave, tema in dados_temas["temas"].items():
            niveis = tuple(DefinicaoNivel(**nivel) for nivel in tema["niveis"])
            temas[chave] = DefinicaoTema(nome=tema["nome"], direcao=tema["direcao"], niveis=niveis)

        return cls(classes=classes, inimigos=inimigos, temas=temas, tema_padrao=dados_temas["padrao"], controles=ler("controles.json"), aparencias=ler("aparencias.json"))

