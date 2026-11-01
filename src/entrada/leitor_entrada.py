"""Classe LeitorEntrada: o único lugar do jogo que lê pygame.event.

Regra da camada entrada/:
    Só os arquivos desta pasta podem importar pygame.event, pygame.key e
    pygame.joystick. Personagens, mapa, movimento, IA, jogo, telas e ui
    nunca importam nada disso. O teste tests/test_camadas.py confere.

O que é:
    Uma vez por quadro, a Aplicacao chama ler_quadro(). Ele esvazia a fila
    de eventos do pygame (pygame.event.get()) e transforma tudo em dados
    simples, sem pygame:
        - a janela foi fechada;
        - ações de menu (cima, baixo, esquerda, direita, confirmar, voltar,
          apagar), vindas do teclado ou de qualquer controle;
        - letras digitadas (para a caixa do nome);
        - controles que foram ligados ou desligados.

    O movimento e os ataques durante a partida NÃO passam por aqui: cada
    dispositivo (teclado.py, gamepad.py) olha o estado das teclas e botões
    a cada quadro (amostrar) e entrega ao seu ControladorHumano a cada
    tick (ler).

Atributos:
    - teclas_menu: dict[int, AcaoMenu]. Qual tecla vira qual ação de menu
      (setas e WASD navegam, ENTER confirma, ESC volta, BACKSPACE apaga).
    - botoes_menu: dict[int, AcaoMenu]. O mesmo para botões de controle
      (direcional navega, A confirma, B volta).

Métodos:
    - ler_quadro() -> EntradaQuadro: lê os eventos do quadro e devolve o
      resumo (ver entrada_menu.py).

Quem usa: Aplicacao.
Usa: entrada/entrada_menu.py.
"""
