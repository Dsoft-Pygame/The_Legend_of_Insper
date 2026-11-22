"""A poção de vida que cai dos inimigos."""

from personagens.entidade import Entidade
from settings import CURA_POCAO, MAGENTA
from ui import carregar_imagem


class Pocao(Entidade):
    """Poção de vida: às vezes cai de um inimigo derrotado e cura o herói que encostar nela.

    Sem o pocao.png, desenha um quadradinho magenta no lugar.
    """

    def __init__(self, x, y):
        """Cria a poção com centro em (x, y), com a cura de CURA_POCAO e o desenho do frasco."""
        super().__init__(x, y, 12, 12, MAGENTA)
        self.cura = CURA_POCAO
        self.imagem = carregar_imagem("pocao.png")   # frasco de 16 x 16, um pouco maior que a colisão
