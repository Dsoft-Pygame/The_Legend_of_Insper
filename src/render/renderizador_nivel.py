"""Classe RenderizadorNivel: desenha o nível. É o único que desenha o mundo.

O que é:
    Separa o desenho da lógica, como a Interface::desenhar da simulação
    lobo-coelho desenha o Mundo inteiro e o Animal nunca se desenha. Ele
    só LÊ o Nivel: nunca move, cria ou remove nada.

Atributos:
    - aparencias: Aparencias.
    - camera: Camera.

Métodos:
    - desenhar(superficie: pygame.Surface, nivel: Nivel) -> None:
        1. camera.seguir(posições dos heróis vivos);
        2. desenha os ladrilhos de nivel.mapa.ladrilhos_em(área visível);
        3. desenha a saída (diferente se estiver aberta);
        4. desenha personagens e projéteis visíveis, ordenados pelo y
           (quem está mais embaixo aparece na frente);
        5. personagem invulnerável pisca.
    - mudar_mapa(nivel: Nivel) -> None: avisa a câmera do tamanho do mapa
      novo.

Quem usa: TelaJogo.
Usa: render/camera.py, render/aparencias.py, jogo/nivel.py (só leitura).
"""
