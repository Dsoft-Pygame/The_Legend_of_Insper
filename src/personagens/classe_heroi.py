"""Classe ClasseHeroi (dataclass congelada): uma classe jogável, como dado.

O que é:
    O herói continua TENDO uma classe em vez de SER um mago (composição),
    como já estava no desenho original. A diferença é que Mago, Arqueiro e
    Bárbaro deixam de ser subclasses em código e viram entradas em
    data/classes.json. Uma classe nova é só mais uma entrada no JSON,
    reaproveitando os tipos de ataque que já existem.

Atributos:
    - nome: str. "Mago", "Arqueiro", "Bárbaro".
    - descricao: str. Aparece na tela de escolha.
    - vida_maxima: int.
    - velocidade: float.
    - movimento: str | dict. Configuração do movimento (normalmente "livre").
    - aparencia: str. Chave para o render.
    - ataque: dict. Configuração do ataque básico (tipo + parâmetros).
    - especial: dict. Configuração da habilidade especial.

As três classes de hoje (formato completo em data/README.md):
    - Mago: frágil, dano alto à distância. Ataque: bola de fogo lenta e
      forte. Especial: anel de fogo, várias bolas em todas as direções.
    - Arqueiro: ágil, ataca rápido de longe. Ataque: flecha rápida.
      Especial: tiro triplo, três flechas em leque.
    - Bárbaro: resistente, luta de perto. Ataque: golpe de machado numa
      área pequena na frente. Especial: giro que acerta todo mundo em volta.

Quem cria: Catalogo, lendo data/classes.json.
Quem usa: Fabrica (monta o Personagem), TelaClasses e CartaoClasse
(mostram nome, descrição e atributos).
"""


from dataclasses import dataclass


@dataclass(frozen=True)
class ClasseHeroi:
    nome: str                 # "Mago"
    descricao: str            # o texto que aparece na escolha de classe
    vida_maxima: int          # ex.: 60
    velocidade: float         # pixels por segundo
    movimento: str | dict     # "livre" ou {"tipo": "...", ...}
    aparencia: str            # chave do aparencias.json, ex.: "mago"
    ataque: dict              # o ataque normal (tipo e números)
    especial: dict            # o ataque especial
