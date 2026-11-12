class Tela:
    """A mãe de todas as telas. A Aplicacao chama estes três métodos a cada quadro,
    e cada tela filha troca só os que precisa.
    """

    def __init__(self, aplicacao):
        self.aplicacao = aplicacao        # para trocar de tela e guardar nome, herói e pontos

    def tratar_evento(self, evento):
        pass                              # um evento do pygame: tecla, texto digitado...

    def atualizar(self, dt):
        pass                              # dt: segundos desde o quadro anterior

    def desenhar(self, superficie):
        pass
