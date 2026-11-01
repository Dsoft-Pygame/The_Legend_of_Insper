"""Classe Entidade: a base de tudo que existe dentro de um nível.

O que é:
    Personagens e projéteis têm coisas em comum: um id, uma posição no
    mapa e um tamanho. Isso fica aqui e as outras herdam.

    A Entidade NÃO tem imagem e NÃO se desenha. Ela guarda só uma chave de
    aparência ("slime", "mago", "flecha"); quem transforma essa chave em
    cor ou sprite é o render (render/aparencias.py). Assim dá para trocar
    toda a arte sem mexer em nenhuma entidade.

Atributos:
    - id: EntidadeId.
    - posicao: pygame.Vector2. Centro, em pixels do mapa (não da tela).
    - tamanho: pygame.Vector2. Largura e altura da caixa de colisão.
    - aparencia: str. Chave para o render.

Propriedades:
    - caixa -> pygame.Rect: retângulo de colisão montado a partir de
      posicao e tamanho.

Herdam dela: Personagem e Projetil.
"""
