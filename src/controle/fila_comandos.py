"""Classe FilaComandos: os pedidos do tick, esperando para serem aplicados.

O que é:
    Todos os controladores escrevem aqui, do mesmo jeito, na etapa
    coletar_comandos do Nivel. Depois, na etapa executar_comandos, o Nivel
    esvazia a fila e aplica cada comando no personagem certo. É a mesma
    separação "decidir, depois agir" da simulação lobo-coelho: ninguém
    mexe no mundo enquanto os outros ainda estão decidindo.

    Também é o ponto natural para gravar um replay: tudo que sai daqui,
    com o número do tick, reproduz a partida.

Atributos:
    - pedidos: list[tuple[EntidadeId, Comando]]. Em ordem de chegada.

Métodos:
    - adicionar(ator_id: EntidadeId, comando: Comando) -> None.
    - esvaziar() -> list[tuple[EntidadeId, Comando]]: devolve tudo e limpa.
    - __len__() -> int.

Quem usa: Nivel.
Usa: controle/comandos.py, personagens/tipos.py.
"""


from controle.comandos import Comando
from personagens.tipos import EntidadeId

class FilaComandos:
    def __init__(self) -> None:
        self.pedidos: list[tuple[EntidadeId, Comando]] = []
    
    def adicionar(self, ator_id: EntidadeId, comando: Comando) -> None:
        self.pedidos.append((ator_id, comando))

    def esvaziar(self) -> list[tuple[EntidadeId, Comando]]:
        pedidos = self.pedidos
        self.pedidos = []
        return pedidos
    def __len__(self) -> int:
        return len(self.pedidos)
        