from settings import BONUS_TEMPO_MAXIMO, BONUS_VIDA_MAXIMO, PONTOS_NIVEL, TEMPO_REFERENCIA


class Pontuacao:
    """Os pontos de uma partida e o motivo de cada um (o extrato que aparece no fim)."""

    def __init__(self):
        self.total = 0
        self.inimigos_derrotados = 0
        self.pontos_inimigos = 0
        self.extrato = []                 # textos como "Térreo concluído +500"

    def inimigo_derrotado(self, nome, pontos):
        self.total += pontos
        self.pontos_inimigos += pontos
        self.inimigos_derrotados += 1

    def nivel_concluido(self, nome_nivel):
        self.total += PONTOS_NIVEL
        self.extrato.append(f"{nome_nivel} concluído +{PONTOS_NIVEL}")

    def chefe_derrotado(self, nome, pontos):
        self.total += pontos
        self.inimigos_derrotados += 1
        self.extrato.append(f"{nome} derrotado +{pontos}")

    def aplicar_bonus(self, venceu, tempo, vida_restante):
        """Só quem venceu ganha bônus: por terminar rápido e pela vida que sobrou (de 0 a 1)."""
        if not venceu:
            return
        bonus_tempo = max(0, round(BONUS_TEMPO_MAXIMO * (1 - tempo / TEMPO_REFERENCIA)))
        bonus_vida = round(BONUS_VIDA_MAXIMO * max(0, min(1, vida_restante)))
        self.total += bonus_tempo + bonus_vida
        self.extrato.append(f"Bônus de tempo +{bonus_tempo}")
        self.extrato.append(f"Bônus de vida +{bonus_vida}")
