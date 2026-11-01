"""Classes Sessao e PerfilJogador: quem está jogando agora.

O que é:
    A Sessao substitui as antigas variáveis "nome_jogador" e
    "classe_escolhida" da Aplicacao. Em vez de um jogador fixo, ela guarda
    uma LISTA de perfis. Hoje a lista tem um perfil só; o co-op local é
    colocar um segundo perfil, sem mudar nenhuma outra classe.

PerfilJogador (dataclass):
    - numero: int. 1 para o P1, 2 para o P2...
    - nome: str. Digitado na TelaInicial.
    - dispositivo: str. Nome do dispositivo de entrada desse jogador
      ("teclado_wasd", "teclado_setas", "gamepad_0"...).
    - classe: str | None. Chave da classe em data/classes.json ("mago",
      "arqueiro", "barbaro"); None até a TelaClasses.

Sessao:
    Atributos:
        - jogadores: list[PerfilJogador].
        - tema: str. Chave do tema em data/temas.json.
        - pontuacao: Pontuacao | None. A da partida atual (uma só no co-op).
        - venceu: bool. Resultado da última partida.

    Métodos:
        - adicionar_jogador(nome: str, dispositivo: str) -> PerfilJogador.
        - buscar(numero: int) -> PerfilJogador | None.
        - limpar() -> None: começa uma sessão nova.

Quem usa: Aplicacao, TelaInicial, TelaClasses, TelaJogo, TelaResultado.
Usa: jogo/pontuacao.py.
"""
