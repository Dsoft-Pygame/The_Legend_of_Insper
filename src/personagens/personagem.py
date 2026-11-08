"""Classe Personagem (herda de Entidade): herói, inimigo ou chefe.

O que é:
    Substitui as antigas classes Jogador, Inimigo e Chefe. Como o Animal da
    simulação lobo-coelho, é uma classe só: o que muda de um slime para um
    mago são os DADOS (data/classes.json, data/inimigos.json) e QUEM
    CONTROLA (o Controlador guardado no Nivel), não a classe.

    O Personagem:
        - não lê teclado nem controle;
        - não decide nada (isso é do Controlador e do sistema de decisão);
        - não desenha;
        - só guarda estado e expõe ações, que não sabem quem pediu.

Atributos:
    - lado: Lado. HEROIS ou MONSTROS.
    - nome: str. Ex.: "Mago", "Slime", "Dragão Ancião" (aparece no HUD).
    - vida, vida_maxima: int.
    - velocidade: float. Pixels por segundo.
    - dano_contato: int. Dano ao encostar em alguém do outro lado (0 nos
      heróis).
    - pontos: int. Quanto vale ao ser derrotado (0 nos heróis).
    - chefe: bool. Derrotar um chefe vence a partida.
    - direcao_olhar: pygame.Vector2. Para onde está virado (para mirar).
    - intencao: pygame.Vector2. O que mover() pediu neste tick (tamanho de
      0 a 1). O movimento zera depois de andar.
    - movimento: Movimento. O jeito de andar (estratégia trocável).
    - ataque, especial: Ataque | None. O ataque básico e a habilidade
      especial (estratégias trocáveis; nos heróis vêm da ClasseHeroi).
    - quer_atacar, quer_especial: bool. Pedidos deste tick.
    - recarga_ataque, recarga_especial: float. Segundos até poder de novo.
    - invulneravel: float. Segundos sem levar dano depois de um golpe
      (o render faz piscar).
    - ultimo_agressor: EntidadeId | None. Quem deu o último golpe.
    - acao_atual: str. O que está fazendo agora: "parado", "andando",
      "atacando", "especial" ou "atingido". Não é desenho, é estado: o
      render usa para escolher a animação. O Nivel põe "andando" ou
      "parado" depois de mover; o combate põe "atacando" ou "especial"
      quando o ataque sai e "atingido" quando leva dano. Essas três ficam
      por DURACAO_ACAO (0,3 s) antes de andar ou parar poder trocá-las,
      para o golpe não ser cortado pela metade.
    - tempo_na_acao: float. Segundos desde que acao_atual mudou (para a
      animação de ataque começar da primeira imagem).

Ações (chamadas pelos comandos; só registram a intenção):
    - mover(direcao: pygame.Vector2) -> None: guarda a intenção e vira o
      personagem para lá.
    - atacar() -> None: marca quer_atacar.
    - especial() -> None: marca quer_especial.

Regras do próprio personagem:
    - receber_dano(quantidade: int, agressor: EntidadeId | None) -> bool:
      tira vida se não estiver invulnerável; devolve False se o golpe foi
      ignorado.
    - pode_atacar() -> bool e pode_especial() -> bool: vivo e sem recarga.
    - avancar_tempos(dt: float) -> None: desconta recargas e
      invulnerabilidade e soma dt em tempo_na_acao.
    - mudar_acao(acao: str) -> None: troca acao_atual e zera
      tempo_na_acao. Se já estava nessa ação, não zera (a animação de
      andar não recomeça a cada tick).
    - esta_vivo -> bool (propriedade): vida > 0.

Quem cria: Fabrica, a partir dos dados.
Quem usa: Nivel, jogo/combate.py, render (só lê).
Usa: personagens/entidade.py, movimento/movimento.py,
personagens/ataques/ataque.py.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from personagens.entidade import Entidade
from personagens.tipos import EntidadeId, Lado

if TYPE_CHECKING:
    from movimento.movimento import Movimento
    from personagens.ataques.ataque import Ataque

DURACAO_ACAO = 0.3                                     # segundos que um golpe "segura" a animação
ACOES_QUE_SEGURAM = ("atacando", "especial", "atingido")


class Personagem(Entidade):
    def __init__(self, lado: Lado, nome: str, posicao: pygame.Vector2, tamanho: pygame.Vector2,
                 aparencia: str, vida_maxima: int, velocidade: float, movimento: Movimento,
                 ataque: Ataque | None = None, ataque_especial: Ataque | None = None,
                 dano_contato: int = 0, pontos: int = 0, chefe: bool = False,
                 tempo_invulneravel: float = 0.0) -> None:
        super().__init__(posicao, tamanho, aparencia)
        self.lado = lado
        self.nome = nome
        self.vida = vida_maxima                        # começa cheio
        self.vida_maxima = vida_maxima
        self.velocidade = velocidade
        self.dano_contato = dano_contato
        self.pontos = pontos
        self.chefe = chefe
        self.movimento = movimento
        self.ataque = ataque
        self.ataque_especial = ataque_especial         # não "especial": isso apagaria o método
        self.tempo_invulneravel = tempo_invulneravel

        self.direcao_olhar = pygame.Vector2(1, 0)
        self.intencao = pygame.Vector2(0, 0)
        self.quer_atacar = False
        self.quer_especial = False
        self.recarga_ataque = 0.0
        self.recarga_especial = 0.0
        self.invulneravel = 0.0
        self.ultimo_agressor: EntidadeId | None = None
        self.acao_atual = "parado"
        self.tempo_na_acao = 0.0

    def mover(self, direcao: pygame.Vector2) -> None:
        direcao = pygame.Vector2(direcao)              # cópia (aceita tupla)
        if direcao.length() == 0:
            return
        if direcao.length() > 1:
            direcao = direcao.normalize()
        self.intencao = direcao
        self.direcao_olhar = direcao.normalize()

    def atacar(self) -> None:
        self.quer_atacar = True

    def especial(self) -> None:
        self.quer_especial = True

    @property
    def esta_vivo(self) -> bool:
        return self.vida > 0

    def receber_dano(self, quantidade: int, agressor: EntidadeId | None) -> bool:
        if not self.esta_vivo or self.invulneravel > 0:
            return False
        self.vida = max(0, self.vida - quantidade)
        self.ultimo_agressor = agressor
        self.invulneravel = self.tempo_invulneravel
        self.mudar_acao("atingido")
        return True

    def pode_atacar(self) -> bool:
        return self.esta_vivo and self.ataque is not None and self.recarga_ataque <= 0

    def pode_especial(self) -> bool:
        return self.esta_vivo and self.ataque_especial is not None and self.recarga_especial <= 0

    def avancar_tempos(self, dt: float) -> None:
        self.recarga_ataque = max(0.0, self.recarga_ataque - dt)
        self.recarga_especial = max(0.0, self.recarga_especial - dt)
        self.invulneravel = max(0.0, self.invulneravel - dt)
        self.tempo_na_acao += dt

    def mudar_acao(self, acao: str) -> None:
        if acao == self.acao_atual:
            return
        if (acao in ("andando", "parado") and self.acao_atual in ACOES_QUE_SEGURAM
                and self.tempo_na_acao < DURACAO_ACAO):
            return
        self.acao_atual = acao
        self.tempo_na_acao = 0.0
