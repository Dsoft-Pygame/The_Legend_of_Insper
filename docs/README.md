# The Legend of Insper

Jogo de ação top-down em Python com [pygame-ce](https://pyga.me/). O jogador escolhe uma classe (Mago, Arqueiro ou Bárbaro) e atravessa os andares de uma torre cheia de monstros. O jogo ainda está sendo feito: o que já funciona está em [Estado atual](#estado-atual).

O código usa só classes normais com herança simples e `super()`. A organização está em [ARQUITETURA.md](ARQUITETURA.md).

## Como rodar

Requisitos: Python 3.10 ou mais novo.

```
pip install -r requirements.txt
python src/main.py
```

## Controles

| Onde | Tecla | O que faz |
|---|---|---|
| Tela inicial | Enter | vai para a escolha de classe |
| Escolha de classe | A / D ou ← / → | trocam a classe |
| | Enter | começa o jogo |
| | Esc | volta para a tela inicial |
| Jogo | W A S D | andar |
| | Espaço | ataque |
| | Shift esquerdo | especial |

## Classes

| Classe | Vida | Velocidade | Dano | Ataque (Espaço) | Especial (Shift esquerdo) |
|---|---|---|---|---|---|
| Mago | 60 | 70 | 30 | bola de fogo lenta e forte | anel com 12 bolas de fogo |
| Arqueiro | 80 | 100 | 10 | flecha rápida | 3 flechas em leque |
| Bárbaro | 140 | 75 | 35 | machadada logo na frente | giro que acerta todos em volta |

## Inimigos

Os inimigos já existem como classes em `personagens/inimigos.py`, com os números do `inimigos.json` da main, mas ainda não aparecem no jogo (T51).

| Inimigo | Vida | Dano ao encostar | Pontos | Jeito |
|---|---|---|---|---|
| Slime | 20 | 10 | 50 | lento; persegue quando o herói chega perto |
| Esqueleto | 40 | 15 | 80 | mais rápido e percebe o herói de mais longe |
| Morcego | 10 | 5 | 70 | muito rápido; o zigue-zague ainda está no branch task-46 |
| Dragão Ancião | 600 | 25 | 2000 | o chefe do Topo da Torre; os ataques de chefe ainda faltam |

## Pastas

```
src/
├── main.py              cria a Aplicacao e roda
├── settings.py          cores, tamanhos, FPS, pontuação e a lista de níveis
├── aplicacao.py         janela, loop e troca de tela; guarda o herói escolhido e o ranking
├── ui.py                texto e caixa do nome
├── telas/               tela inicial, escolha de classe, jogo e resultado
├── jogo/                mapa, câmera, nível, pontuação e ranking
├── personagens/         entidade, personagem, heróis, inimigos e projéteis
├── assets/              sprites e sons, quando tiver
└── data/
    ├── mapas/           um .txt por nível
    └── ranking.json     as partidas do ranking (fica fora do git)
```

## Estado atual

O jogo está no mesmo ponto da main antes da simplificação. Dá para escolher a classe e andar pelo Térreo usando o ataque e o especial, com a câmera seguindo o herói. Como ainda não aparecem inimigos, a saída já fica aberta, piscando, e encostar nela ainda não faz nada.

Já estão escritos, mas ainda não ligados no jogo: as classes de inimigo, o dano dos projéteis e de contato, a `Pontuacao`, o `Ranking` (lido ao abrir o jogo) e a `CaixaTexto`.

Faltam:

- criar os inimigos das letras do mapa e as regras da partida: pontos, passar de nível pela saída, vitória e derrota (T51);
- o nome do jogador na tela inicial (T55), o quadro do ranking e a tela de resultado com os pontos;
- o HUD e a pausa (T65);
- os mapas dos andares 2 e 3, o zigue-zague do morcego e os ataques do chefe.
