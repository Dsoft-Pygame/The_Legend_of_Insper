"""Classes MapaTeclas e DispositivoTeclado: o teclado como dispositivo.

O que é:
    Um DispositivoTeclado é "uma parte do teclado" de um jogador. O teclado
    físico é um só, mas vira dois dispositivos para o co-op local: WASD
    para o P1 e setas para o P2. Quais teclas cada um usa vem de
    data/controles.json, não do código.

    Implementa DispositivoFisico (entrada/gerenciador_dispositivos.py),
    que é a interface DispositivoEntrada (controle/dispositivo.py) mais
    amostrar() e limpar(). O ControladorHumano não sabe se está falando
    com teclado ou controle.

    Por que dois métodos de leitura: a tela roda 60 quadros por segundo e
    a lógica 20 ticks. O teclado é olhado a cada quadro (amostrar) e
    entregue a cada tick (ler). Se fosse olhado só no tick, um toque de
    espaço que começa e termina no meio de um tick sumiria.

MapaTeclas (dataclass congelada):
    - cima, baixo, esquerda, direita, ataque, especial: int. Códigos de
      tecla do pygame (convertidos com pygame.key.key_code("w") etc.).

DispositivoTeclado:
    Atributos:
        - nome: str. Ex.: "teclado_wasd".
        - teclas: MapaTeclas.
        - eixo: tuple[float, float]. Do último amostrar().
        - segurando: frozenset[Botao]. Do último amostrar().
        - segurando_antes: frozenset[Botao]. Do amostrar() anterior, para
          saber quando um botão acabou de descer.
        - apertou_guardado: set[Botao]. Botões que desceram desde o
          último ler().

    Métodos:
        - amostrar() -> None: a cada quadro. Lê pygame.key.get_pressed() e
          calcula:
            * eixo: -1, 0 ou 1 em x e em y, com tamanho no máximo 1
              (na diagonal não fica mais rápido);
            * segurando: botões apertados agora;
            * botões em segurando que não estavam em segurando_antes
              entram em apertou_guardado.
        - ler() -> EstadoEntrada: a cada tick. Devolve eixo e segurando do
          último amostrar() e apertou = apertou_guardado; depois esvazia
          apertou_guardado.
        - limpar() -> None: esvazia apertou_guardado. Chamado ao reservar
          o dispositivo, para o ENTER ou espaço do menu não virar um
          ataque no primeiro tick.
        - de_config(nome: str, config: dict) -> DispositivoTeclado
          (classmethod): monta a partir de data/controles.json.

Quem usa: GerenciadorDispositivos.
Usa: controle/dispositivo.py (EstadoEntrada, Botao).
"""
from dataclasses import dataclass
import pygame
from controle.dispositivo import Botao, EstadoEntrada


@dataclass(frozen=True)
class MapaTeclas:
  cima: int
  baixo: int
  esquerda: int
  direita: int
  ataque: int
  especial: int


class DispositivoTeclado:
  def __init__(self, nome: str, teclas: MapaTeclas) -> None:
    self.nome = nome
    self.teclas = teclas
    self.eixo = (0.0, 0.0)
    self.segurando: frozenset[Botao] = frozenset()
    self.segurando_antes: frozenset[Botao] = frozenset()
    self.apertou_guardado: set[Botao] = set()

  def amostrar(self) -> None:
    apertadas = pygame.key.get_pressed()

    x = int(apertadas[self.teclas.direita]) - int(apertadas[self.teclas.esquerda])
    y = int(apertadas[self.teclas.baixo]) - int(apertadas[self.teclas.cima])

    eixo = pygame.Vector2(x, y)
    if eixo.length() > 1: # Normaliza para que a diagonal não seja mais rápida
        eixo = eixo.normalize()

    self.eixo = (eixo.x, eixo.y)

    segurando = set()
    if apertadas[self.teclas.ataque]:
        segurando.add(Botao.ATAQUE)
    if apertadas[self.teclas.especial]:
        segurando.add(Botao.ESPECIAL)

    self.segurando_antes = self.segurando
    self.segurando = frozenset(segurando)

    self.apertou_guardado |= self.segurando - self.segurando_antes # Guarda apenas os botões que acabaram de ser pressionados

  def ler(self) -> EstadoEntrada:
    estado = EstadoEntrada(
      eixo=self.eixo,
      segurando=self.segurando,
      apertou=frozenset(self.apertou_guardado)
    )

    self.apertou_guardado.clear()
    return estado

  def limpar(self) -> None:
    self.apertou_guardado.clear()

  @classmethod
  def de_config(cls, nome: str, config: dict) -> "DispositivoTeclado":
    teclas = MapaTeclas(
      cima=pygame.key.key_code(config["cima"]),
      baixo=pygame.key.key_code(config["baixo"]),
      esquerda=pygame.key.key_code(config["esquerda"]),
      direita=pygame.key.key_code(config["direita"]),
      ataque=pygame.key.key_code(config["ataque"]),
      especial=pygame.key.key_code(config["especial"])
    )

    return cls(nome, teclas)