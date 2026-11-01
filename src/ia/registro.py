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
