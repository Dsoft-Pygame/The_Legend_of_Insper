# Arquitetura

O jogo é feito de classes pequenas. Cada classe filha herda de uma mãe só, chama `super().__init__(...)` e troca só o que muda.

## O loop e as telas

A `Aplicacao` (`src/aplicacao.py`) abre a janela e roda o loop a 60 quadros por segundo. Em cada quadro ela:

1. lê os eventos com `pygame.event.get()` e entrega cada um para a tela atual (`tratar_evento`);
2. chama `atualizar(dt)` da tela, com `dt` = segundos desde o quadro anterior;
3. chama `desenhar(superficie)` numa superfície de 480 x 320 e amplia 2 vezes na janela.

As telas não importam umas às outras. Para trocar, uma tela pede `self.aplicacao.trocar_tela("nome")`, e a `Aplicacao` cria a tela nova:

```
inicial ──Enter──> classes ──Enter──> controles ──Enter──> jogo ──chefe derrotado ou herói sem vida──> resultado
   ^                │   ^                 │                                                                 │
   ├─────Esc────────┘   └──────Esc────────┘                                                                 │
   └────────────────────────────────────────Enter (ou 20 s parada)──────────────────────────────────────────┘
```

O que passa de uma tela para outra fica guardado na `Aplicacao`: o nome digitado na TelaInicial, o `heroi` escolhido na TelaClasses, a `pontuacao` e o resultado da partida, e o `ranking`, lido do arquivo quando o jogo abre.

## Árvore de herança

```
Tela                      telas/tela.py: tratar_evento, atualizar e desenhar vazios
├── TelaInicial           título, nome do jogador e ranking; Enter vai para a escolha de classe
├── TelaClasses           Mago, Arqueiro ou Bárbaro
├── TelaControles         as teclas do jogo, antes da partida; Enter começa e Esc volta para a escolha de classe
├── TelaJogo              o nível, os ataques, a câmera, o HUD, a pausa e a troca de andar
└── TelaResultado         vitória ou derrota, extrato dos pontos e ranking

Entidade                  posição, tamanho, cor, retangulo() e desenhar()
├── Personagem            vida, mover() sem atravessar parede, receber_dano(), pisca invulnerável
│   ├── Heroi             anda com WASD, recargas, usar_ataque() e usar_especial()
│   │   ├── Mago          troca atacar() e especial()
│   │   ├── Arqueiro      troca atacar() e especial()
│   │   └── Barbaro       troca atacar() e especial()
│   └── Inimigo           vaga e persegue o herói; dano de contato, pontos e animação (quadros que trocam com o tempo)
│       ├── Slime         só muda os números e quica
│       ├── Esqueleto     só muda os números
│       ├── Morcego       persegue em zigue-zague
│       └── Dragao        2 fases, bola e anel de fogo (pisca vermelho 0,5 s antes do anel); contorna as paredes até o herói (Mapa.proximo_passo)
├── Projetil              anda, some na parede ou quando o tempo acaba; dono "heroi" ou "inimigo"
│   └── Golpe             corpo a corpo: fica parado e troca bateu_na_parede(); o giro atravessa inimigos, mas nenhum golpe passa parede
└── Pocao                 poção de vida que cai dos inimigos
```

Sem mãe: `Aplicacao`, `Mapa`, `Camera`, `Nivel`, `Pontuacao`, `Ranking` e `CaixaTexto`.

## Um quadro do nível

A `TelaJogo` transforma Espaço e Shift esquerdo em `heroi.usar_ataque()` e `heroi.usar_especial()` e põe os projéteis criados no nível. Depois, `Nivel.atualizar(dt)` faz, nesta ordem:

1. o herói anda;
2. cada inimigo pensa e anda (o `atualizar` devolve os projéteis que ele criar, para o chefe poder atirar);
3. os projéteis andam e somem os que bateram na parede ou acabaram o tempo;
4. projétil do herói que encosta num inimigo dá dano e empurra o inimigo (knockback: a força é o `empurrao_ataque` da classe, e a `resistencia` do inimigo diminui, de 0 no slime e no morcego até 0,85 no Dragão), e projétil de inimigo dá dano no herói; cada projétil acerta cada alvo uma vez só; o inimigo empurrado desliza sem atravessar parede e vai freando;
5. inimigo encostado no herói dá dano de contato;
6. os inimigos mortos saem da lista, e cada um (menos o chefe) tem 30% de chance de deixar uma `Pocao` de vida no lugar;
7. poção encostada no herói devolve 25 de vida, sem passar da vida máxima, e some.

Os inimigos são criados a partir das letras do mapa quando o nível abre. Cada inimigo derrotado soma os seus pontos na `Pontuacao`. Sem inimigos, a saída abre, e a `TelaJogo` usa o `Nivel.heroi_na_saida()` para passar de andar. A partida termina quando o chefe morre (vitória) ou quando a vida do herói acaba (derrota).

Depois de levar dano, o herói fica 0,8 s invulnerável e piscando, por isso um inimigo encostado não tira vida a cada quadro.

## Andar sem atravessar parede

O `Personagem.mover()` anda um eixo de cada vez, e o eixo que entraria na parede não anda. Assim, andando na diagonal, o herói escorrega pela parede.

Andando reto contra a quina de uma porta, ele desvia até 8 pixels para o lado (`contornar_quina`), como o `MovimentoLivre` da main. É isso que deixa o herói, de 24 pixels, passar nas portas de 1 tile (32 pixels) sem precisar acertar o pixel.

## Os mapas

Cada nível é um `.txt` em `src/data/mapas/`, e cada letra é um tile de 32 x 32 pixels:

| Letra | O que é |
|---|---|
| `#` | parede |
| `.` | chão |
| `H` | onde o herói começa |
| `S` | saída |
| `s`, `e`, `m` | slime, esqueleto, morcego |
| `C` | chefe |

O `Mapa` guarda as paredes, a saída e onde nasce cada um. A lista de níveis fica em `NIVEIS`, no `settings.py`, com os inimigos de cada andar anotados e os tiles de chão e parede de cada um. O `Nivel` escolhe uma das 4 variantes de cada tile pela posição dele, então o desenho não muda de um quadro para o outro.

Para criar um inimigo novo: escreva uma classe filha de `Inimigo` em `personagens/inimigos.py`, chame `super().__init__(...)` com os números dele e escolha uma letra para o mapa.

## Pontuação e ranking

A `Pontuacao` soma os pontos da partida inteira:

- cada inimigo derrotado vale os seus pontos (Slime 50, Esqueleto 80, Morcego 70, Dragão 2000);
- nível concluído vale 500;
- só quem vence ganha bônus pelo tempo e pela vida que sobrou (`Pontuacao.aplicar_bonus`).

O `Ranking` guarda cada partida como um dicionário (nome, classe, pontos, venceu) em `src/data/ranking.json`. Ele é lido quando o jogo abre, mostrado na TelaInicial e na TelaResultado, e a partida é salva assim que a TelaResultado abre, ganhando ou perdendo.

## Regras do código

- Herança com uma mãe só e `super()`. Nada de decoradores, `abc`, `typing`, `dataclasses`, `enum` ou anotações de tipo.
- Nada de `raise` ou `try`. Quando precisar conferir algo, um `if`.
- Os números do jogo ficam no `__init__` da classe ou no `settings.py`.
- Tudo que anda usa `velocidade * dt`, com `dt` em segundos.
- Docstring de 1 a 3 linhas em todo arquivo, classe e função, e comentários curtos em português.
