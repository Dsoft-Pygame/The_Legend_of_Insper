"""Classe DecisaoPerseguir: vaga até ver um herói, então vai atrás dele.

O que é:
    A IA dos inimigos comuns (Slime, Esqueleto). Antes era o método
    Inimigo.pensar(jogador); agora é um sistema de decisão separado, que
    serve para qualquer personagem, inclusive um herói no piloto automático.

Parâmetros (vêm do campo "decisao" em data/inimigos.json):
    - raio_alerta: float. A partir de quantos pixels começa a perseguir.
    - distancia_ataque: float. Perto assim, pede Atacar() (se o personagem
      não tiver ataque, o dano é só por contato).
    - tempo_vagando: float. Segundos andando numa direção antes de sortear
      outra.

Memória:
    - direcao_vagando: pygame.Vector2.
    - tempo_restante: float.

Métodos:
    - decidir(visao: Visao, gerador: random.Random) -> list[Comando]:
        1. procura o herói mais próximo (visao.mais_proximo(Lado.HEROIS));
        2. se ele estiver dentro do raio_alerta, Mover na direção dele e,
           se estiver perto, Atacar;
        3. senão, vaga: segue na direção sorteada ou fica parado.
      Com vários heróis (co-op), persegue o mais próximo.

Quem usa: ControladorIA (pelo nome "perseguir" no registro).
Usa: personagens/visao.py, controle/comandos.py.
"""
