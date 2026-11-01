"""Classe Hud: as informações por cima do jogo.

O que aparece:
    - Canto superior esquerdo: uma barra de vida para CADA herói, com o
      nome do jogador. Com um jogador, uma barra; no co-op, uma embaixo da
      outra.
    - Topo, no meio: nome do nível (ex.: "Andar 2").
    - Canto superior direito: pontuação.
    - Embaixo, quando houver chefe: nome e barra de vida do chefe.
    - Quando o nível está limpo: aviso "Saída aberta!".

O Hud não recebe o Jogador nem o Mundo: recebe um ResumoPartida (dados
prontos, só leitura, criado por Mundo.resumo()). Não usa a câmera, porque
fica sempre no mesmo lugar da tela.

Métodos:
    - desenhar(superficie: pygame.Surface, resumo: ResumoPartida) -> None.

Usada em: TelaJogo.
"""
