"""Classes MapaTeclas e DispositivoTeclado: o teclado como dispositivo.

O que é:
    Um DispositivoTeclado é "uma parte do teclado" de um jogador. O teclado
    físico é um só, mas vira dois dispositivos para o co-op local: WASD
    para o P1 e setas para o P2. Quais teclas cada um usa vem de
    data/controles.json, não do código.

    Implementa a interface DispositivoEntrada (controle/dispositivo.py):
    o ControladorHumano não sabe se está falando com teclado ou controle.

MapaTeclas (dataclass congelada):
    - cima, baixo, esquerda, direita, ataque, especial: int. Códigos de
      tecla do pygame (convertidos com pygame.key.key_code("w") etc.).

DispositivoTeclado:
    Atributos:
        - nome: str. Ex.: "teclado_wasd".
        - teclas: MapaTeclas.
        - segurando_antes: frozenset[Botao]. Para saber quando um botão
          acabou de ser apertado.

    Métodos:
        - ler() -> EstadoEntrada: lê pygame.key.get_pressed() e devolve:
            * eixo: -1, 0 ou 1 em x e em y, com tamanho no máximo 1
              (na diagonal não fica mais rápido);
            * segurando: botões apertados agora;
            * apertou: botões que não estavam apertados na leitura anterior.
        - de_config(nome: str, config: dict) -> DispositivoTeclado
          (classmethod): monta a partir de data/controles.json.

Quem usa: GerenciadorDispositivos.
Usa: controle/dispositivo.py (EstadoEntrada, Botao).
"""
