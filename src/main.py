"""Ponto de entrada do jogo: python src/main.py"""
from aplicacao import Aplicacao


def main():
    """Cria a Aplicacao e roda o jogo até a janela fechar."""
    aplicacao = Aplicacao()
    aplicacao.executar()


if __name__ == "__main__":
    main()
