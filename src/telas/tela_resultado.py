"""Classe TelaResultado (herda de Tela): o fim da partida.

O que aparece:
    - VITÓRIA ou DERROTA.
    - Nome e classe de cada jogador da Sessao.
    - Os pontos da partida (inimigos, níveis, chefe, bônus) e o total.
    - Em que posição ficou no ranking e o ranking ao lado.

O que faz:
    - ao_entrar(): aplica os bônus finais na Pontuacao e salva a partida
      no Ranking. Sempre salva, ganhando ou perdendo. Libera os
      dispositivos dos jogadores.
    - tratar_entrada(entrada: EntradaMenu): CONFIRMAR volta para
      TelaInicial.
    - atualizar(dt): se ninguém apertar nada por alguns segundos, volta
      sozinha (para o próximo visitante da feira).

Usa: jogo/ranking.py, jogo/pontuacao.py, ui/painel_ranking.py,
aplicacao/sessao.py.
"""
