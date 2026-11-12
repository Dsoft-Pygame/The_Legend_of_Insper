import json
import os

from settings import ARQUIVO_RANKING


def pegar_pontos(partida):
    return partida["pontos"]


class Ranking:
    """Guarda as partidas em data/ranking.json, da maior para a menor pontuação.

    Cada partida é um dicionário com nome, classe, pontos e venceu.
    """

    def __init__(self, arquivo=ARQUIVO_RANKING):
        self.arquivo = arquivo
        self.partidas = []
        if os.path.exists(arquivo):
            with open(arquivo, encoding="utf-8") as dados:
                self.partidas = json.load(dados)
        self.partidas.sort(key=pegar_pontos, reverse=True)

    def adicionar(self, nome, classe, pontos, venceu):
        """Guarda a partida, salva o arquivo e devolve a posição dela (1 = primeiro lugar)."""
        self.partidas.append({"nome": nome, "classe": classe, "pontos": pontos, "venceu": venceu})
        self.partidas.sort(key=pegar_pontos, reverse=True)
        self.salvar()
        posicao = 0
        for partida in self.partidas:     # empate fica atrás de quem já estava lá
            if partida["pontos"] >= pontos:
                posicao += 1
        return posicao

    def melhores(self, quantidade):
        return self.partidas[:quantidade]

    def salvar(self):
        with open(self.arquivo, "w", encoding="utf-8") as dados:
            json.dump(self.partidas, dados, ensure_ascii=False, indent=2)
