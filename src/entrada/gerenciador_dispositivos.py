"""DispositivoFisico e GerenciadorDispositivos: teclados e controles.

DispositivoFisico (interface, typing.Protocol):
    A interface DispositivoEntrada (controle/dispositivo.py) mais dois
    métodos que só a camada de entrada usa:
        - amostrar() -> None: olha o hardware agora. Chamado a cada
          quadro (60 vezes por segundo). Guarda os botões que desceram
          até o próximo ler().
        - limpar() -> None: esquece os botões guardados.
    O ControladorHumano continua vendo só ler(), uma vez por tick
    (20 vezes por segundo).

GerenciadorDispositivos:
    O que é:
        Guarda todos os dispositivos disponíveis e diz qual está livre
        para um jogador novo. É o que deixa o co-op local pronto: cada
        PerfilJogador da Sessao guarda o nome de um dispositivo, e a
        TelaJogo pede o dispositivo por esse nome.

        Ao abrir o jogo, cria os teclados de data/controles.json
        ("teclado_wasd" e "teclado_setas") e um DispositivoGamepad para
        cada controle conectado. Controles ligados ou desligados no meio
        do jogo chegam pelo EntradaQuadro.

    Atributos:
        - dispositivos: dict[str, DispositivoFisico]. Por nome.
        - em_uso: set[str]. Nomes já entregues a algum jogador.

    Métodos:
        - atualizar(entrada: EntradaQuadro) -> None: cria ou remove gamepads.
        - amostrar() -> None: chama amostrar() de todos os dispositivos.
          A Aplicacao chama a cada quadro, logo depois de ler_quadro().
        - livres() -> list[str]: nomes dos dispositivos sem dono.
        - reservar(nome: str) -> DispositivoEntrada: marca como em uso,
          chama limpar() (o toque que confirmou o menu não vira ataque) e
          devolve.
        - liberar(nome: str) -> None: devolve ao fim da partida.
        - buscar(nome: str) -> DispositivoEntrada | None.

Quem usa: Aplicacao (cria, atualiza e amostra a cada quadro), TelaInicial
(escolhe o dispositivo de cada jogador), TelaJogo (pede o dispositivo).
Usa: entrada/teclado.py, entrada/gamepad.py, controle/dispositivo.py,
data/controles.json.
"""
