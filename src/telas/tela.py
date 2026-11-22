"""A classe mãe das telas do jogo."""

class Tela:
    """A mãe de todas as telas. A Aplicacao chama estes três métodos a cada quadro,
    e cada tela filha troca só os que precisa.
    """

    def __init__(self, aplicacao):
        """Guarda a Aplicacao, que a tela usa para trocar de tela e ler o que foi escolhido."""
        self.aplicacao = aplicacao        # para trocar de tela e guardar o herói escolhido

    def tratar_evento(self, evento):
        """Recebe um evento do pygame (tecla, texto digitado...). Cada tela filha troca este método."""
        pass                              # um evento do pygame: tecla, texto digitado...

    def atualizar(self, dt):
        """Avança a tela dt segundos. A mãe não faz nada."""
        pass                              # dt: segundos desde o quadro anterior

    def desenhar(self, superficie):
        """Desenha a tela na superfície de 480 x 320. A mãe não desenha nada."""
        pass
