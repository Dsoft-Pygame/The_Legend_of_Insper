"""Classe GerenciadorDispositivos: quais teclados e controles existem.

O que é:
    Guarda todos os dispositivos disponíveis e diz qual está livre para um
    jogador novo. É o que deixa o co-op local pronto: cada PerfilJogador da
    Sessao guarda o nome de um dispositivo, e a TelaJogo pede o dispositivo
    por esse nome.

    Ao abrir o jogo, cria os teclados de data/controles.json
    ("teclado_wasd" e "teclado_setas") e um DispositivoGamepad para cada
    controle conectado. Controles ligados ou desligados no meio do jogo
    chegam pelo EntradaQuadro.

Atributos:
    - dispositivos: dict[str, DispositivoEntrada]. Por nome.
    - em_uso: set[str]. Nomes já entregues a algum jogador.

Métodos:
    - atualizar(entrada: EntradaQuadro) -> None: cria ou remove gamepads.
    - livres() -> list[str]: nomes dos dispositivos sem dono.
    - reservar(nome: str) -> DispositivoEntrada: marca como em uso e devolve.
    - liberar(nome: str) -> None: devolve ao fim da partida.
    - buscar(nome: str) -> DispositivoEntrada | None.

Quem usa: Aplicacao (cria e atualiza), TelaInicial (escolhe o
dispositivo de cada jogador), TelaJogo (pede o dispositivo).
Usa: entrada/teclado.py, entrada/gamepad.py, data/controles.json.
"""
