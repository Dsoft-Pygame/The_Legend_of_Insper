from personagens.entidade import Entidade
from settings import CURA_POCAO, MAGENTA


class Pocao(Entidade):
    """Poção de vida: às vezes cai de um inimigo derrotado e cura o herói que encostar nela.

    Por enquanto é um quadradinho colorido; quando tiver o desenho, é só pôr a self.imagem.
    """

    def __init__(self, x, y):
        super().__init__(x, y, 12, 12, MAGENTA)
        self.cura = CURA_POCAO
