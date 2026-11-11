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


from settings import (BONUS_TEMPO_MAXIMO, BONUS_VIDA_MAXIMO, PONTOS_NIVEL, TEMPO_REFERENCIA)


class Pontuacao:
    def __init__(self) -> None:
        self.total = 0
        self.inimigos_derrotados = 0
        self.pontos_inimigos = 0
        self.extrato: list[str] = []

    def inimigo_derrotado(self, nome: str, pontos: int) -> None:
        self.total += pontos
        self.pontos_inimigos += pontos
        self.inimigos_derrotados += 1

    def nivel_concluido(self, nome_nivel: str) -> None:
        self.total += PONTOS_NIVEL
        self.extrato.append(f"{nome_nivel} concluído +{PONTOS_NIVEL}")

    def chefe_derrotado(self, nome: str, pontos: int) -> None:
        self.total += pontos
        self.inimigos_derrotados += 1
        self.extrato.append(f"{nome} derrotado +{pontos}")

    def aplicar_bonus(self, venceu: bool, tempo: float, vida_restante: float) -> None:
        if not venceu:
            return
        else:
          bonus_tempo = max(0, round(BONUS_TEMPO_MAXIMO * (1 - tempo / TEMPO_REFERENCIA)))
          bonus_vida = round(BONUS_VIDA_MAXIMO * max(0.0, min(1.0, vida_restante)))

        self.total += bonus_tempo + bonus_vida

        self.extrato.append(f"Bônus de tempo +{bonus_tempo}")
        self.extrato.append(f"Bônus de vida +{bonus_vida}")