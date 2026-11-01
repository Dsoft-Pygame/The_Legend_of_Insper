"""Classes Animacao e ConjuntoAnimacoes: qual imagem mostrar agora.

O que é:
    Uma animação é uma sequência de imagens (quadros) tocada numa
    velocidade própria, por exemplo 8 imagens por segundo. A escolha da
    imagem depende só do TEMPO, nunca de contar ticks ou quadros de tela:
    se a lógica passar de 20 para 30 ticks, ou a tela de 60 para 144 fps,
    a animação continua na mesma velocidade.

    O tempo vem do personagem (tempo_na_acao, que conta desde que ele
    começou a ação atual) mais a fração do tick que já passou. Assim um
    ataque sempre começa da primeira imagem.

Animacao (dataclass congelada):
    - quadros: tuple[pygame.Surface, ...]. As imagens, em ordem.
    - por_segundo: float. Quantas imagens por segundo (ex.: 8).
    - repete: bool. True para andar e parado (volta ao começo); False
      para ataque e "atingido" (para na última imagem).

    Métodos:
        - quadro_em(tempo: float) -> pygame.Surface: indice =
          int(tempo * por_segundo); se repete, indice % len(quadros);
          senão, no máximo o último.
        - duracao() -> float: len(quadros) / por_segundo.

ConjuntoAnimacoes:
    As animações de uma aparência, por ação ("parado", "andando",
    "atacando", "especial", "atingido").

    Atributos:
        - animacoes: dict[str, Animacao].

    Métodos:
        - escolher(acao: str) -> Animacao: a animação da ação; se não
          tiver, a de "parado". Assim um inimigo simples pode ter só
          "parado" e "andando".
        - de_folha(folha: pygame.Surface, config: dict) -> ConjuntoAnimacoes
          (classmethod): recorta a folha de sprites (uma linha por ação,
          um quadro ao lado do outro) com o tamanho_quadro do JSON.

Formato no JSON: ver src/data/README.md, seção aparencias.json.

Quem usa: Aparencias.
"""
