"""Classes MapaTeclas e DispositivoTeclado: o teclado como dispositivo.

O que é:
    Um DispositivoTeclado é "uma parte do teclado" de um jogador. O teclado
    físico é um só, mas vira dois dispositivos para o co-op local: WASD
    para o P1 e setas para o P2. Quais teclas cada um usa vem de
    data/controles.json, não do código.

    Implementa DispositivoFisico (entrada/gerenciador_dispositivos.py),
    que é a interface DispositivoEntrada (controle/dispositivo.py) mais
    amostrar() e limpar(). O ControladorHumano não sabe se está falando
    com teclado ou controle.

    Por que dois métodos de leitura: a tela roda 60 quadros por segundo e
    a lógica 20 ticks. O teclado é olhado a cada quadro (amostrar) e
    entregue a cada tick (ler). Se fosse olhado só no tick, um toque de
    espaço que começa e termina no meio de um tick sumiria.

MapaTeclas (dataclass congelada):
    - cima, baixo, esquerda, direita, ataque, especial: int. Códigos de
      tecla do pygame (convertidos com pygame.key.key_code("w") etc.).

DispositivoTeclado:
    Atributos:
        - nome: str. Ex.: "teclado_wasd".
        - teclas: MapaTeclas.
        - eixo: tuple[float, float]. Do último amostrar().
        - segurando: frozenset[Botao]. Do último amostrar().
        - segurando_antes: frozenset[Botao]. Do amostrar() anterior, para
          saber quando um botão acabou de descer.
        - apertou_guardado: set[Botao]. Botões que desceram desde o
          último ler().

    Métodos:
        - amostrar() -> None: a cada quadro. Lê pygame.key.get_pressed() e
          calcula:
            * eixo: -1, 0 ou 1 em x e em y, com tamanho no máximo 1
              (na diagonal não fica mais rápido);
            * segurando: botões apertados agora;
            * botões em segurando que não estavam em segurando_antes
              entram em apertou_guardado.
        - ler() -> EstadoEntrada: a cada tick. Devolve eixo e segurando do
          último amostrar() e apertou = apertou_guardado; depois esvazia
          apertou_guardado.
        - limpar() -> None: esvazia apertou_guardado. Chamado ao reservar
          o dispositivo, para o ENTER ou espaço do menu não virar um
          ataque no primeiro tick.
        - de_config(nome: str, config: dict) -> DispositivoTeclado
          (classmethod): monta a partir de data/controles.json.

Quem usa: GerenciadorDispositivos.
Usa: controle/dispositivo.py (EstadoEntrada, Botao).
"""
