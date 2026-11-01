"""tipos.py: tipos básicos compartilhados, como o Tipos.h da simulação.

O que guarda:
    - EntidadeId = int. Identificador único de cada coisa no nível. O Nivel
      guarda personagens, controladores e projéteis em dicionários por id.
    - Lado (enum): HEROIS e MONSTROS. Substitui o antigo dono = "jogador" /
      "inimigo" dos projéteis e diz quem pode machucar quem. Um ataque
      nunca acerta o próprio lado.
    - Vetor = pygame.Vector2 e Caixa = pygame.Rect: apelidos usados nas
      anotações de tipo. São só matemática (funcionam sem janela), por isso
      o domínio pode usá-los.

Regra das camadas de domínio (personagens/, movimento/, mapa/):
    Podem importar pygame.Vector2 e pygame.Rect. Nunca importam
    pygame.event, pygame.key, pygame.joystick ou pygame.display, e nunca
    desenham numa pygame.Surface.

Quem usa: quase todo mundo.
"""
