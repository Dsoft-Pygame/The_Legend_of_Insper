"""Classe TelaInicial (herda de Tela): a primeira tela do jogo.

O que aparece:
    - À esquerda: nome do jogo e um campo para digitar o nome do jogador.
    - À direita: o ranking com os melhores jogadores.
    - Embaixo: "ENTER para jogar".

Atributos:
    - caixa_nome: CaixaTexto onde o jogador digita o nome.
    - painel_ranking: PainelRanking que desenha a lista.
    - aviso: str. "Digite um nome" quando tenta seguir com o nome vazio.

O que faz:
    - ao_entrar(): limpa a Sessao e a caixa do nome.
    - tratar_entrada(entrada: EntradaMenu): passa entrada.texto para
      caixa_nome.digitar e APAGAR para caixa_nome.apagar. CONFIRMAR com o
      nome preenchido cria o PerfilJogador do P1 na Sessao e troca para
      TelaClasses. O P1 fica com o dispositivo que apertou CONFIRMAR
      (teclado_wasd, se foi o teclado). Nome vazio mostra o aviso.
    - atualizar(dt): pisca o cursor e o aviso.
    - desenhar(superficie): título, caixa de nome e ranking.

Co-op (quando for feito): um segundo jogador aperta CONFIRMAR no próprio
dispositivo e digita o nome; vira o PerfilJogador 2.

Usa: ui/caixa_texto.py, ui/painel_ranking.py, jogo/ranking.py,
aplicacao/sessao.py, entrada/gerenciador_dispositivos.py.
"""
