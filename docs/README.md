# The Legend of Insper

Jogo de ação top-down em Python com [pygame-ce](https://pyga.me/). O jogador escolhe uma classe (Mago, Arqueiro ou Bárbaro) e atravessa os andares de uma torre cheia de monstros. O jogo ainda está sendo feito: o que já funciona está em [Estado atual](#estado-atual).

O código usa só classes normais com herança simples e `super()`. A organização está em [ARQUITETURA.md](ARQUITETURA.md).

## Simplificação

O código foi simplificado a pedido do professor, com ajuda de IA: saíram os decoradores, as classes abstratas, as anotações de tipo, o tratamento de exceções e os testes com pytest. O que mudou e como foi feito está em [SIMPLIFICACAO.md](SIMPLIFICACAO.md).

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

| Classe | Vida | Velocidade | Dano | Ataque (Espaço) | Especial (Shift esquerdo) | Recarga do especial |
|---|---|---|---|---|---|---|
| Mago | 60 | 140 | 30 | bola de fogo lenta e forte | anel com 12 bolas de fogo | 9 s |
| Arqueiro | 80 | 200 | 10 | flecha rápida | 5 flechas em leque, de 15 de dano | 5 s |
| Bárbaro | 140 | 150 | 35 | machadada logo na frente | giro que acerta todos em volta | 7 s |

Embaixo da barra de vida fica a barra do especial: azul enquanto recarrega, com os segundos que faltam do lado, e amarela com "ESPECIAL PRONTO" piscando quando dá para usar. A recarga e a duração do especial de cada classe são `tempo_especial` e `duracao_especial`, no `__init__` da classe em `personagens/herois.py`.

## Inimigos

Os inimigos já existem como classes em `personagens/inimigos.py`, com os números do `inimigos.json` da main, mas ainda não aparecem no jogo (T51).

| Inimigo | Vida | Dano ao encostar | Pontos | Jeito |
|---|---|---|---|---|
| Slime | 20 | 10 | 50 | lento; persegue quando o herói chega perto |
| Esqueleto | 40 | 15 | 80 | mais rápido e percebe o herói de mais longe |
| Morcego | 10 | 5 | 70 | muito rápido; o zigue-zague ainda está no branch task-46 |
| Dragão Ancião | 450 | 25 | 2000 | o chefe do Topo da Torre; os ataques de chefe ainda faltam |

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

## Créditos

- Sprites dos heróis (`src/assets/mago.png`, `arqueiro.png` e `barbaro.png`): Thiago A. Gomes.
- Sons e músicas (`src/assets/sons/`): gerados por código pelo Claude (assistente de IA da Anthropic). Detalhes em `src/assets/sons/CREDITOS.md`.
- Tiles de chão e parede (`src/assets/tiles/`): pedra (Térreo e Topo da Torre) e biblioteca (Biblioteca), 4 variantes de cada, gerados por código (`gerar_tiles.py`, na pasta de sprites do grupo).

Os outros desenhos (saída e inimigos) ainda não existem: sem o PNG, o jogo desenha o quadrado colorido no lugar.
