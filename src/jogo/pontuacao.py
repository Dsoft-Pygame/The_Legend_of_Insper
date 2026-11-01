"""Classe Pontuacao: os pontos de uma partida.

O que é:
    Cada partida tem uma Pontuacao nova. O Mundo vai somando pontos a
    partir dos eventos do Nivel, e a TelaResultado mostra o total no fim.
    No co-op a pontuação é uma só, somada por todos os heróis.

Atributos:
    - total: int. Os pontos somados até agora.
    - inimigos_derrotados: int. Quantos inimigos os heróis derrotaram.
    - extrato: list[str]. O motivo de cada ponto ("Nível 1 concluído +500"),
      mostrado na tela de resultado.

Métodos:
    - inimigo_derrotado(nome: str, pontos: int) -> None: soma os pontos de
      um inimigo.
    - nivel_concluido(nome_nivel: str) -> None: soma os pontos de passar de
      nível.
    - chefe_derrotado(nome: str, pontos: int) -> None: soma os pontos do
      chefe.
    - aplicar_bonus(venceu: bool, tempo: float, vida_restante: float)
      -> None: no fim da partida, se venceu, soma bônus por terminar rápido
      e pela vida que sobrou (de 0 a 1; no co-op, a média dos heróis).

Ideia de valores: inimigo 50 a 100 (cada um define os seus em
data/inimigos.json), nível 500, chefe 2000. Ganhando ou perdendo, o total
vai para o ranking.

Quem usa: Mundo e TelaResultado.
"""
