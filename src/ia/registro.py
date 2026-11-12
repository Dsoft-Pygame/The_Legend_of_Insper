"""registro.py: os sistemas de decisão que podem ser usados nos dados.

O que é:
    Um dicionário SISTEMAS_DECISAO: dict[str, Callable[..., SistemaDecisao]]
    que liga o nome usado em data/inimigos.json à classe:
        "perseguir"   -> DecisaoPerseguir
        "zigue_zague" -> DecisaoZigueZague
        "chefe"       -> DecisaoChefe

    A Fabrica lê o campo "decisao" do inimigo, por exemplo
    {"tipo": "perseguir", "raio_alerta": 80}, procura o tipo aqui e cria
    a instância com o resto dos campos como parâmetros.

    Uma IA nova = um arquivo novo nesta pasta + uma linha aqui. Nenhum
    outro arquivo muda.

Funções:
    - criar_decisao(config: dict) -> SistemaDecisao: cria a partir do
      campo "decisao". Nome desconhecido gera erro na abertura do jogo,
      não no meio da partida.

Quem usa: Fabrica e Catalogo (para conferir os nomes).
"""


from typing import Callable

from ia.decisao_perseguir import DecisaoPerseguir
from ia.sistema_decisao import SistemaDecisao
from ia.decisao_zigue_zague import DecisaoZigueZague

SISTEMAS_DECISAO: dict[str, Callable[..., SistemaDecisao]] = {
    "perseguir": DecisaoPerseguir,
    "zigue_zague": DecisaoZigueZague
    # "chefe": T47
}


def criar_decisao(config: dict) -> SistemaDecisao:
    tipo = config.get("tipo")
    if tipo not in SISTEMAS_DECISAO:
        raise ValueError(f"Sistema de decisão desconhecido: '{tipo}'. Opções: {', '.join(SISTEMAS_DECISAO)}")
    parametros = {chave: valor for chave, valor in config.items() if chave != "tipo"}
    return SISTEMAS_DECISAO[tipo](**parametros)
