"""Classe DecisaoZigueZague: vai na direção do herói, desviando de lado.

O que é:
    A IA do Morcego (rápido, pouca vida, voa em zigue-zague). Vai para o
    herói mais próximo, mas soma à direção um desvio para o lado que troca
    de sinal de tempos em tempos.

Parâmetros (vêm do campo "decisao" em data/inimigos.json):
    - raio_alerta: float.
    - periodo: float. Segundos entre uma troca de lado e outra.
    - amplitude: float. Quanto desvia (0 = reto, 1 = 45 graus).

Memória:
    - lado_atual: int. +1 ou -1.
    - tempo_restante: float.

Métodos:
    - decidir(visao: Visao, gerador: random.Random) -> list[Comando].
      Sem herói à vista, vaga como a DecisaoPerseguir.

Quem usa: ControladorIA (pelo nome "zigue_zague" no registro).
Usa: personagens/visao.py, controle/comandos.py.
"""
