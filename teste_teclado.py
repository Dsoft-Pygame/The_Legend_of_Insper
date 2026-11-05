import sys
sys.path.insert(0, "src")
import json
import pygame
from entrada.teclado import DispositivoTeclado

pygame.init()
pygame.display.set_mode((320, 240))
config = json.load(open("src/data/controles.json", encoding="utf-8"))["teclado_wasd"]
teclado = DispositivoTeclado.de_config("teclado_wasd", config)
relogio = pygame.time.Clock()
quadro = 0
while not any(e.type == pygame.QUIT for e in pygame.event.get()):
    teclado.amostrar()
    quadro += 1
    if quadro % 3 == 0:                       # 1 tick a cada 3 quadros
        estado = teclado.ler()
        if estado.eixo != (0, 0) or estado.apertou:
            print(estado)
    relogio.tick(60)