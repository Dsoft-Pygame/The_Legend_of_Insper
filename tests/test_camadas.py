"""Teste das camadas: confere as regras da arquitetura lendo os imports.

O que vai fazer:
    Percorre todos os .py de src/ com o módulo ast (lê o código, sem
    executar nada) e falha se:
        1. algum arquivo fora de src/entrada/ usar pygame.event,
           pygame.key ou pygame.joystick (import ou chamada);
        2. algum arquivo de personagens/, movimento/, mapa/, controle/,
           ia/ ou jogo/ usar pygame.display ou desenhar numa Surface
           (essas camadas só podem usar pygame.Vector2 e pygame.Rect);
        3. uma camada importar uma camada de cima. Ordem, de cima para
           baixo (na mesma linha = mesma camada, podem se importar):
               aplicacao
               entrada, telas, ui, render
               jogo
               controle, ia
               personagens, movimento, mapa
           settings.py pode ser importado por qualquer um.

    A mensagem de erro diz o arquivo, a linha e a regra quebrada.

Como rodar: python -m pytest tests/ (ou python tests/test_camadas.py,
que roda sem o pytest).

Por que existe: a separação só vale se ninguém furar sem perceber. O
teste avisa na hora, sem precisar revisar import por import.
"""
