"""Classe Tela (base abstrata, abc.ABC): o molde de todas as telas.

O que é:
    Toda tela do jogo é uma classe que herda de Tela. Como todas têm os
    mesmos métodos, a Aplicacao consegue rodar qualquer uma sem saber qual
    é. Trocar de tela é só trocar o objeto.

    As telas não recebem eventos do pygame: recebem uma EntradaMenu
    (entrada/entrada_menu.py), com ações como CONFIRMAR e VOLTAR e as
    letras digitadas. Assim funcionam igual com teclado ou com controle, e
    nenhuma tela importa pygame.event ou pygame.key.

Atributos:
    - aplicacao: Aplicacao. Para trocar de tela e ler ou gravar a Sessao.

Métodos (cada tela filha implementa os seus):
    - tratar_entrada(entrada: EntradaMenu) -> None (abstrato): reage às
      ações de menu e ao texto digitado.
    - atualizar(dt: float) -> None (abstrato): avança a lógica da tela.
      dt = segundos desde o último quadro (usar dt deixa a velocidade
      igual em PCs rápidos e lentos).
    - desenhar(superficie: pygame.Surface) -> None (abstrato).
    - ao_entrar() -> None e ao_sair() -> None (opcionais): preparar e
      limpar a tela.

Herdam dela: TelaInicial, TelaClasses, TelaJogo e TelaResultado.
"""
