"""main.py: ponto de entrada do jogo.

O que é:
    O arquivo que se executa para abrir o jogo: `python src/main.py`.
    Não tem lógica de jogo. Só cria a Aplicacao e manda ela rodar.

O que faz:
    1. Cria um objeto Aplicacao (aplicacao/aplicacao.py).
    2. Chama aplicacao.executar(), que só termina quando a janela fecha.
"""
from aplicacao.aplicacao import Aplicacao


def main() -> None:
    aplicacao = Aplicacao()
    aplicacao.executar()


if __name__ == "__main__":
    main()
