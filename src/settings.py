"""Configurações do jogo (o único arquivo com valores preenchidos).

Tudo que é "número mágico" (resolução, FPS, cores, caminhos, regras de
pontuação) mora aqui, para ser ajustado sem caçar valores pelo código.
"""
from pathlib import Path

# Cores (enquanto não tiver sprites)
BLACK = (16, 16, 24)
WHITE = (240, 240, 232)
GRAY = (120, 120, 130)
RED = (220, 60, 60)
GREEN = (80, 200, 100)
YELLOW = (250, 210, 80)
BLUE = (80, 140, 230)
DARK_GRAY = (40, 40, 52)
BROWN = (120, 80, 40)
ORANGE = (240, 140, 40)
CYAN = (80, 210, 210)
PINK = (240, 120, 180)
PURPLE = (150, 80, 200)
MAGENTA = (255, 0, 255)

# Telas
TITULO = "The Legend of Insper"
LARGURA_TELA = 240
ALTURA_TELA = 160
ESCALA = 4 
TAMANHO_TILE = 16

# Pastas
PASTA_SRC = Path(__file__).resolve().parent
PASTA_DATA = PASTA_SRC / "data"
PASTA_ASSETS = PASTA_SRC / "assets"

# Pontuacao
PONTOS_NIVEL = 500
BONUS_TEMPO_MAXIMO = 3000
TEMPO_REFERENCIA = 600
BONUS_VIDA_MAXIMO = 1000