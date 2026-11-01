"""Classe Personagem (herda de Entidade): herói, inimigo ou chefe.

O que é:
    Substitui as antigas classes Jogador, Inimigo e Chefe. Como o Animal da
    simulação lobo-coelho, é uma classe só: o que muda de um slime para um
    mago são os DADOS (data/classes.json, data/inimigos.json) e QUEM
    CONTROLA (o Controlador guardado no Nivel), não a classe.

    O Personagem:
        - não lê teclado nem controle;
        - não decide nada (isso é do Controlador e do sistema de decisão);
        - não desenha;
        - só guarda estado e expõe ações, que não sabem quem pediu.

Atributos:
    - lado: Lado. HEROIS ou MONSTROS.
    - nome: str. Ex.: "Mago", "Slime", "Dragão Ancião" (aparece no HUD).
    - vida, vida_maxima: int.
    - velocidade: float. Pixels por segundo.
    - dano_contato: int. Dano ao encostar em alguém do outro lado (0 nos
      heróis).
    - pontos: int. Quanto vale ao ser derrotado (0 nos heróis).
    - chefe: bool. Derrotar um chefe vence a partida.
    - direcao_olhar: pygame.Vector2. Para onde está virado (para mirar).
    - intencao: pygame.Vector2. O que mover() pediu neste tick (tamanho de
      0 a 1). O movimento zera depois de andar.
    - movimento: Movimento. O jeito de andar (estratégia trocável).
    - ataque, especial: Ataque | None. O ataque básico e a habilidade
      especial (estratégias trocáveis; nos heróis vêm da ClasseHeroi).
    - quer_atacar, quer_especial: bool. Pedidos deste tick.
    - recarga_ataque, recarga_especial: float. Segundos até poder de novo.
    - invulneravel: float. Segundos sem levar dano depois de um golpe
      (o render faz piscar).
    - ultimo_agressor: EntidadeId | None. Quem deu o último golpe.

Ações (chamadas pelos comandos; só registram a intenção):
    - mover(direcao: pygame.Vector2) -> None: guarda a intenção e vira o
      personagem para lá.
    - atacar() -> None: marca quer_atacar.
    - especial() -> None: marca quer_especial.

Regras do próprio personagem:
    - receber_dano(quantidade: int, agressor: EntidadeId | None) -> bool:
      tira vida se não estiver invulnerável; devolve False se o golpe foi
      ignorado.
    - pode_atacar() -> bool e pode_especial() -> bool: vivo e sem recarga.
    - avancar_tempos(dt: float) -> None: desconta recargas e
      invulnerabilidade.
    - esta_vivo -> bool (propriedade): vida > 0.

Quem cria: Fabrica, a partir dos dados.
Quem usa: Nivel, jogo/combate.py, render (só lê).
Usa: personagens/entidade.py, movimento/movimento.py,
personagens/ataques/ataque.py.
"""
