import pygame

from render.camera import Camera


def test_centraliza_no_alvo():
    camera = Camera(240, 160)
    camera.mudar_mapa(720, 320)
    camera.seguir([pygame.Vector2(360, 160)])
    assert (camera.x, camera.y) == (240, 80)


def test_para_na_borda_do_mapa():
    camera = Camera(240, 160)
    camera.mudar_mapa(720, 320)
    camera.seguir([pygame.Vector2(10, 10)])
    assert (camera.x, camera.y) == (0, 0)
    camera.seguir([pygame.Vector2(715, 315)])
    assert (camera.x, camera.y) == (480, 160)


def test_varios_alvos_usa_o_ponto_medio():
    camera = Camera(240, 160)
    camera.mudar_mapa(720, 320)
    camera.seguir([pygame.Vector2(300, 160), pygame.Vector2(420, 160)])
    assert camera.x == 240


def test_para_tela_desconta_a_camera():
    camera = Camera(240, 160)
    camera.mudar_mapa(720, 320)
    camera.seguir([pygame.Vector2(360, 160)])
    assert camera.para_tela(pygame.Rect(250, 90, 16, 16)) == pygame.Rect(10, 10, 16, 16)


def test_esta_visivel():
    camera = Camera(240, 160)
    camera.mudar_mapa(720, 320)
    assert camera.esta_visivel(pygame.Rect(100, 100, 16, 16))
    assert not camera.esta_visivel(pygame.Rect(500, 100, 16, 16))