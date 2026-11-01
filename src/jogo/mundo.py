"""Classe Mundo: a partida inteira, com os níveis em sequência.

O que é:
    O Mundo controla a partida: monta os níveis do tema, um de cada vez,
    leva os heróis de um nível para o outro e decide vitória e derrota.
    A TelaJogo só conversa com o Mundo, nunca direto com um Nivel.

    O Mundo não desenha e não conhece a câmera (isso é do render). Ele
    também não sabe quantos jogadores existem: recebe uma lista de heróis.

Heroi (dataclass):
    - numero: int. 1 para o P1, 2 para o P2...
    - nome: str. Nome do jogador.
    - personagem: Personagem.
    - controlador: Controlador. Normalmente um ControladorHumano.

ResumoPartida (dataclass congelada), o que o HUD recebe:
    - herois: tuple[tuple[str, int, int], ...]. Nome, vida e vida máxima
      de cada herói.
    - pontos: int.
    - nome_nivel: str.
    - chefe: tuple[str, int, int] | None. Nome, vida e vida máxima.
    - saida_aberta: bool.

Atributos:
    - tema: DefinicaoTema. Vem do Catalogo (data/temas.json).
    - fabrica: Fabrica. Cria os inimigos de cada nível.
    - herois: list[Heroi]. Passam de nível com a vida que sobrou.
    - indice_nivel: int.
    - nivel_atual: Nivel.
    - pontuacao: Pontuacao. Uma por partida (somada por todos no co-op).
    - tick: int. Quantos ticks já se passaram.
    - tempo_acumulado: float. Para o passo fixo.
    - PASSO: float. Duração fixa de um tick (1/60 s).
    - venceu: bool. True quando um chefe cai.

Métodos:
    - tempo_avancar(dt: float) -> None: passo fixo com acumulador, como o
      Simulacao::tempo_avancar: soma dt (no máximo 0,25 s por quadro) e
      roda tick_atualizar quantas vezes couber. Cada tick representa
      sempre o mesmo tempo, em PC rápido ou lento.
    - tick_atualizar() -> None: roda nivel_atual.tick_atualizar(PASSO, tick)
      e aplica as regras com os eventos que voltaram:
        * PersonagemDerrotado de monstro: soma os pontos dele;
        * PersonagemDerrotado de chefe: soma os pontos do chefe e venceu;
        * HeroiNaSaida: soma os pontos do nível e chama proximo_nivel();
        * todos os heróis derrotados: derrota.
    - proximo_nivel() -> None: carrega o mapa do próximo nível (com o
      carregador que o tema indica), coloca os heróis nos surgimentos e
      cria os inimigos e o chefe pela Fabrica.
    - terminou() -> bool: venceu, ou todos os heróis caíram.
    - resumo() -> ResumoPartida: dados prontos para o HUD.

Quem usa: TelaJogo.
Usa: jogo/nivel.py, jogo/fabrica.py, jogo/pontuacao.py, jogo/eventos.py,
mapa/registro.py.
"""
