"""O ranking das partidas, guardado num arquivo JSON."""

import json
import os

from settings import ARQUIVO_RANKING


def pegar_pontos(partida):
    """Os pontos de uma partida. É a chave usada para ordenar o ranking."""
    return partida["pontos"]


class Ranking:
    """Guarda as partidas em data/ranking.json, da maior para a menor pontuação.

    Cada partida é um dicionário com nome, classe, pontos e venceu.
    """

    def __init__(self, arquivo=ARQUIVO_RANKING):
        """Lê as partidas do arquivo, se ele existe e não está vazio, e ordena da maior para a menor
        pontuação.
        """
        self.arquivo = arquivo
        self.partidas = []
        if os.path.exists(arquivo) and os.path.getsize(arquivo) > 0:   # arquivo vazio = ranking vazio
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
        """As primeiras partidas do ranking, até a quantidade pedida."""
        return self.partidas[:quantidade]

    def salvar(self):
        """Grava todas as partidas no arquivo JSON."""
        with open(self.arquivo, "w", encoding="utf-8") as dados:
            json.dump(self.partidas, dados, ensure_ascii=False, indent=2)
