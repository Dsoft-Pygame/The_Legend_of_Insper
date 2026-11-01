"""Classe CartaoClasse: o cartão de uma classe na tela de escolha.

Atributos:
    - classe: ClasseHeroi. Os dados da classe (vêm de data/classes.json).
    - retangulo: pygame.Rect. Posição e tamanho do cartão.

Métodos:
    - desenhar(superficie: pygame.Surface, aparencias: Aparencias,
      selecionado: bool) -> None: desenha a imagem (pela chave de
      aparência), o nome e os atributos (vida, velocidade, dano do
      ataque). Com selecionado=True, a borda fica destacada.

Usada em: TelaClasses.
"""
