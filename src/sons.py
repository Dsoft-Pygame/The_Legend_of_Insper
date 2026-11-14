"""Sons do jogo: efeitos curtos e músicas de fundo, pedidos pelo nome."""
import os

import pygame

from settings import PASTA_SONS, VOLUME_EFEITOS, VOLUME_MUSICA

# nome do som -> arquivo em src/assets/sons/
EFEITOS = {
    "ataque": "ataque.wav",
    "acerto": "acerto.wav",
    "inimigo_derrotado": "inimigo_derrotado.wav",
    "chefe_derrotado": "chefe_derrotado.wav",
    "heroi_derrotado": "heroi_derrotado.wav",
    "porta": "porta.wav",
    "menu_mover": "menu_mover.wav",
    "menu_confirmar": "menu_confirmar.wav",
}
MUSICAS = {
    "menu": "musica_menu.ogg",
    "torre": "musica_torre.ogg",
    "chefe": "musica_chefe.ogg",
    "resultado": "musica_resultado.ogg",
}


class Som:
    """Toca os efeitos e as músicas pelo nome. Sem placa de som ou sem o arquivo, fica em silêncio."""

    def __init__(self):
        self.ligado = pygame.mixer.get_init() is not None   # o pygame.init() já tentou ligar o som
        self.efeitos = {}                                   # nome -> pygame.mixer.Sound
        self.musica_atual = None
        if self.ligado:
            for nome in EFEITOS:
                caminho = os.path.join(PASTA_SONS, EFEITOS[nome])
                if os.path.exists(caminho):
                    self.efeitos[nome] = pygame.mixer.Sound(caminho)
                    self.efeitos[nome].set_volume(VOLUME_EFEITOS)

    def tocar(self, nome):
        """Toca um efeito curto, como "ataque". Se o arquivo não existe, não faz nada."""
        if nome in self.efeitos:
            self.efeitos[nome].play()

    def tocar_musica(self, nome):
        """Troca a música de fundo, que fica repetindo. Se já é essa que está tocando, deixa como está."""
        if not self.ligado or nome == self.musica_atual or nome not in MUSICAS:
            return
        caminho = os.path.join(PASTA_SONS, MUSICAS[nome])
        if not os.path.exists(caminho):
            return
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.set_volume(VOLUME_MUSICA)
        pygame.mixer.music.play(-1)                         # -1 = repete para sempre
        self.musica_atual = nome

    def pausar_musica(self, pausar):
        """True pausa a música, False continua de onde parou."""
        if not self.ligado:
            return
        if pausar:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
