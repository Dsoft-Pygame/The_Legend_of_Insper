"""Classe Nivel: um nível em andamento e o tick que move tudo.

O que é:
    Junta um Mapa com quem está nele: personagens, controladores e
    projéteis. A cada tick faz as etapas abaixo, sempre nesta ordem, como
    o Simulacao::tick_atualizar da simulação lobo-coelho. O Nivel não sabe
    o formato do mapa (só usa a interface Mapa) e não desenha nada.

Atributos:
    - nome: str. Ex.: "Catacumbas".
    - numero: int.
    - mapa: Mapa.
    - personagens: dict[EntidadeId, Personagem].
    - controladores: dict[EntidadeId, Controlador]. Quem manda em cada um.
    - raios_visao: dict[EntidadeId, float]. Até onde cada um enxerga.
    - projeteis: dict[EntidadeId, Projetil].
    - fila: FilaComandos.
    - proximo_id: EntidadeId.

Montagem:
    - adicionar(personagem: Personagem, controlador: Controlador,
      raio_visao: float) -> EntidadeId. Quem entra já está no lugar
      certo (colocar_em), sem posição anterior de outro nível.
    - trocar_controlador(id: EntidadeId, controlador: Controlador) -> bool:
      False se o id não existe.
    - remover(id: EntidadeId) -> Personagem | None: tira do nível (usado
      para levar os heróis ao próximo nível).
    - buscar(id: EntidadeId) -> Personagem | None.

Consultas:
    - observar(id: EntidadeId) -> Visao: monta o retrato do que esse
      personagem enxerga, como o Mundo::observar da simulação.
    - herois() -> list[Personagem] e monstros() -> list[Personagem].
    - esta_limpo() -> bool: nenhum monstro vivo (a saída abre).

O tick:
    - tick_atualizar(dt: float, tick: int) -> list[Evento]:
      dt é sempre o PASSO do Mundo (0,05 s a 20 ticks por segundo).
        0. guardar_posicoes(): cada entidade copia posicao para
           posicao_anterior, para o render poder interpolar.
        1. coletar_comandos(tick): para cada personagem vivo, monta a
           Visao, chama controlador.gerar_comandos e põe na fila. Ninguém
           altera o mundo nesta etapa.
        2. executar_comandos(): esvazia a fila e aplica cada comando no
           personagem, se ele ainda existir e estiver vivo.
        3. mover_personagens(dt): personagem.movimento.atualizar(...) para
           cada um, avancar_tempos(dt) e mudar_acao("andando") se a
           posição mudou ou mudar_acao("parado") se não (respeitando
           DURACAO_ACAO de um ataque em andamento).
        4. resolver_combate(dt): ver jogo/combate.py.
        5. remover_mortos(): tira quem morreu e cria os eventos
           PersonagemDerrotado.
        6. checar_saida(): HeroiNaSaida quando um herói encosta na saída
           com o nível limpo.
      Devolve os eventos do tick para o Mundo aplicar as regras.

Quem usa: Mundo, RenderizadorNivel (só lê).
Usa: mapa/mapa.py, controle/, personagens/, jogo/combate.py,
jogo/eventos.py.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from controle.fila_comandos import FilaComandos
from personagens.tipos import EntidadeId, Lado
from personagens.visao import Avistado, Visao

if TYPE_CHECKING:
    from controle.controlador import Controlador
    from mapa.mapa import Mapa
    from personagens.personagem import Personagem


class Nivel:
    def __init__(self, nome: str, numero: int, mapa: Mapa) -> None:
        self.nome = nome
        self.numero = numero
        self.mapa = mapa
        self.personagens: dict[EntidadeId, Personagem] = {}
        self.controladores: dict[EntidadeId, Controlador] = {}
        self.raios_visao: dict[EntidadeId, float] = {}
        self.projeteis: dict = {}                      # id -> Projetil (T41)
        self.fila = FilaComandos()
        self.proximo_id: EntidadeId = 1

    # ---- montagem ----

    def novo_id(self) -> EntidadeId:
        id_novo = self.proximo_id
        self.proximo_id += 1
        return id_novo

    def adicionar(self, personagem: Personagem, controlador: Controlador, raio_visao: float) -> EntidadeId:
        id_novo = self.novo_id()
        personagem.id = id_novo
        personagem.colocar_em(personagem.posicao)      # zera a posição anterior (podia ser do nível passado)
        self.personagens[id_novo] = personagem
        self.controladores[id_novo] = controlador
        self.raios_visao[id_novo] = raio_visao
        return id_novo

    def trocar_controlador(self, id: EntidadeId, controlador: Controlador) -> bool:
        if id not in self.personagens:
            return False
        self.controladores[id] = controlador
        return True

    def remover(self, id: EntidadeId) -> Personagem | None:
        self.controladores.pop(id, None)
        self.raios_visao.pop(id, None)
        return self.personagens.pop(id, None)

    def buscar(self, id: EntidadeId) -> Personagem | None:
        return self.personagens.get(id)

    # ---- consultas ----

    def herois(self) -> list[Personagem]:
        return [p for p in self.personagens.values() if p.lado == Lado.HEROIS]

    def monstros(self) -> list[Personagem]:
        return [p for p in self.personagens.values() if p.lado == Lado.MONSTROS]

    def esta_limpo(self) -> bool:
        return not any(m.esta_vivo for m in self.monstros())

    def observar(self, id: EntidadeId, tick: int = 0, dt: float = 0.0) -> Visao:
        eu = self.personagens[id]
        raio = self.raios_visao[id]
        avistados = tuple(avistar(outro) for outro in self.personagens.values()
                          if outro.id != id and outro.esta_vivo
                          and outro.posicao.distance_to(eu.posicao) <= raio)
        return Visao(tick=tick, dt=dt, eu=avistar(eu), direcao_olhar=pygame.Vector2(eu.direcao_olhar),
                     pode_atacar=eu.pode_atacar(), pode_especial=eu.pode_especial(),
                     avistados=avistados, mapa=self.mapa)


def avistar(personagem: Personagem) -> Avistado:
    """A "foto" de um personagem. O Vector2 é uma cópia: a IA não mexe na posição de verdade."""
    return Avistado(id=personagem.id, lado=personagem.lado, posicao=pygame.Vector2(personagem.posicao),
                    vida=personagem.vida, vida_maxima=personagem.vida_maxima, chefe=personagem.chefe)
