"""Configurações do jogo: cores, tamanhos, pastas, pontuação e a lista de níveis."""
import os

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

# Tela
TITULO = "The Legend of Insper"
LARGURA_TELA = 240        # tudo é desenhado nesta resolução e depois ampliado na janela
ALTURA_TELA = 160
ESCALA = 4                # janela de 960 x 640
FPS = 60
TAMANHO_TILE = 16

# Pastas
PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
PASTA_ASSETS = os.path.join(PASTA_SRC, "assets")
PASTA_MAPAS = os.path.join(PASTA_SRC, "data", "mapas")
ARQUIVO_RANKING = os.path.join(PASTA_SRC, "data", "ranking.json")

# Pontuação
PONTOS_NIVEL = 500
BONUS_TEMPO_MAXIMO = 3000
TEMPO_REFERENCIA = 600    # segundos: quem termina depois disso não ganha bônus de tempo
BONUS_VIDA_MAXIMO = 1000

# Níveis, em ordem: (nome, arquivo em data/mapas/)
NIVEIS = [
    ("Térreo", "torre_1.txt"),
    ("Biblioteca", "torre_2.txt"),
    ("Topo da Torre", "torre_3.txt"),
]
