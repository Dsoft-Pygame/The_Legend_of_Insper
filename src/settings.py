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
MAGENTA = (240, 60, 200)  # a poção de vida

# Tela
TITULO = "The Legend of Insper"
LARGURA_TELA = 480        # tudo é desenhado nesta resolução e depois ampliado na janela
ALTURA_TELA = 320
ESCALA = 2                # janela de 960 x 640
FPS = 60
TAMANHO_TILE = 32

# Pastas
PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
PASTA_ASSETS = os.path.join(PASTA_SRC, "assets")
PASTA_MAPAS = os.path.join(PASTA_SRC, "data", "mapas")
ARQUIVO_RANKING = os.path.join(PASTA_SRC, "data", "ranking.json")
PASTA_SONS = os.path.join(PASTA_ASSETS, "sons")

# Som (de 0 a 1)
VOLUME_MUSICA = 0.5
VOLUME_EFEITOS = 0.7

# Pontuação
PONTOS_NIVEL = 500
BONUS_TEMPO_MAXIMO = 3000
TEMPO_REFERENCIA = 600    # segundos: quem termina depois disso não ganha bônus de tempo
BONUS_VIDA_MAXIMO = 1000

# Poção de vida
CHANCE_POCAO = 0.15       # chance de um inimigo derrotado (menos o chefe) deixar uma poção
CURA_POCAO = 25           # quanto de vida a poção devolve

# Níveis, em ordem: (nome, arquivo em data/mapas/, tiles do chão, tiles da parede).
# Os inimigos de cada um são as letras do mapa. Os tiles são o começo do nome dos PNGs
# em assets/tiles/: "chao" usa chao_1.png até chao_4.png.
NIVEIS = [
    ("Térreo", "torre_1.txt", "chao", "parede"),                       # 4 slimes
    ("Biblioteca", "torre_2.txt", "chao_madeira", "parede_biblio"),    # 3 slimes, 3 esqueletos e 2 morcegos
    ("Topo da Torre", "torre_3.txt", "chao", "parede"),                # 2 esqueletos, 1 morcego e o chefe Dragão
]
