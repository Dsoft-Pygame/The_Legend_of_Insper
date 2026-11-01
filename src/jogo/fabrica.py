"""Classe Fabrica: monta personagens e controladores a partir dos dados.

O que é:
    O único lugar que junta as peças: definição dos dados + Movimento +
    Ataques + sistema de decisão. Ninguém mais precisa saber como um slime
    é montado. Um inimigo novo que reaproveita peças existentes não mexe
    aqui, só no JSON.

Atributos:
    - catalogo: Catalogo. Definições lidas de data/.
    - semente: int. Passada para cada ControladorIA.

Métodos:
    - criar_heroi(classe: str, posicao: pygame.Vector2) -> Personagem:
      monta o Personagem do lado HEROIS com a ClasseHeroi escolhida. O
      controlador do herói não é criado aqui: quem cria é a TelaJogo,
      porque depende do dispositivo de cada jogador.
    - criar_monstro(tipo: str, posicao: pygame.Vector2)
      -> tuple[Personagem, Controlador]: monta o Personagem do lado
      MONSTROS e o ControladorIA com o sistema de decisão do JSON.

Quem usa: Mundo e TelaJogo.
Usa: jogo/catalogo.py, movimento/registro.py,
personagens/ataques/registro.py, ia/registro.py,
controle/controlador_ia.py.
"""
