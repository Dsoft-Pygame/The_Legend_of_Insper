# Arquitetura

O jogo é feito de classes pequenas. Cada classe filha herda de uma mãe só, chama `super().__init__(...)` e troca só o que muda.

## O loop e as telas

A `Aplicacao` (`src/aplicacao.py`) abre a janela e roda o loop a 60 quadros por segundo. Em cada quadro ela:

1. lê os eventos com `pygame.event.get()` e entrega cada um para a tela atual (`tratar_evento`);
2. chama `atualizar(dt)` da tela, com `dt` = segundos desde o quadro anterior;
3. chama `desenhar(superficie)` numa superfície de 240 x 160 e amplia 4 vezes na janela.

As telas não importam umas às outras. Para trocar, uma tela pede `self.aplicacao.trocar_tela("nome")`, e a `Aplicacao` cria a tela nova:

```
inicial ──Enter──> classes ──Enter──> jogo
   ^                  │
   └──────Esc─────────┘

resultado ──Enter──> inicial        (o jogo ainda não chega aqui: é a T51)
```

O que passa de uma tela para outra fica guardado na `Aplicacao`: o `heroi` escolhido na TelaClasses e o `ranking`, lido do arquivo quando o jogo abre.

## Árvore de herança

```
Tela                      telas/tela.py: tratar_evento, atualizar e desenhar vazios
├── TelaInicial           título; Enter vai para a escolha de classe
├── TelaClasses           Mago, Arqueiro ou Bárbaro
├── TelaJogo              o nível, os ataques e a câmera
└── TelaResultado         "FIM" (o jogo ainda não chega aqui)

Entidade                  posição, tamanho, cor, retangulo() e desenhar()
├── Personagem            vida, mover() sem atravessar parede, receber_dano(), pisca invulnerável
│   ├── Heroi             anda com WASD, recargas, usar_ataque() e usar_especial()
│   │   ├── Mago          troca atacar() e especial()
│   │   ├── Arqueiro      troca atacar() e especial()
│   │   └── Barbaro       troca atacar() e especial()
│   └── Inimigo           vaga e persegue o herói; dano de contato e pontos (ainda fora do jogo)
│       ├── Slime         só muda os números
│       ├── Esqueleto     só muda os números
│       ├── Morcego       só muda os números (o zigue-zague está no branch task-46)
│       └── Dragao        só muda os números (os ataques de chefe ainda faltam)
└── Projetil              anda, some na parede ou quando o tempo acaba; dono "heroi" ou "inimigo"
    └── Golpe             corpo a corpo: fica parado e troca bateu_na_parede(); o giro atravessa
```

Sem mãe: `Aplicacao`, `Mapa`, `Camera`, `Nivel`, `Pontuacao`, `Ranking` e `CaixaTexto`.

## Um quadro do nível

A `TelaJogo` transforma Espaço e Shift esquerdo em `heroi.usar_ataque()` e `heroi.usar_especial()` e põe os projéteis criados no nível. Depois, `Nivel.atualizar(dt)` faz, nesta ordem:

1. o herói anda;
2. cada inimigo pensa e anda (o `atualizar` devolve os projéteis que ele criar, para o chefe poder atirar);
3. os projéteis andam e somem os que bateram na parede ou acabaram o tempo;
4. projétil do herói que encosta num inimigo dá dano, e projétil de inimigo dá dano no herói; cada projétil acerta cada alvo uma vez só;
5. inimigo encostado no herói dá dano de contato;
6. os inimigos mortos saem da lista.

Como na main, a lista de inimigos começa vazia, então hoje só os passos 1 e 3 mudam alguma coisa na tela. A T51 cria os inimigos das letras do mapa, soma os pontos de quem morre e usa o `Nivel.heroi_na_saida()` para passar de nível.

Depois de levar dano, o herói fica 0,8 s invulnerável e piscando, por isso um inimigo encostado não tira vida a cada quadro.

## Andar sem atravessar parede

O `Personagem.mover()` anda um eixo de cada vez, e o eixo que entraria na parede não anda. Assim, andando na diagonal, o herói escorrega pela parede.

Andando reto contra a quina de uma porta, ele desvia até 4 pixels para o lado (`contornar_quina`), como o `MovimentoLivre` da main. É isso que deixa o herói, de 12 pixels, passar nas portas de 1 tile (16 pixels) sem precisar acertar o pixel.

## Os mapas

Cada nível é um `.txt` em `src/data/mapas/`, e cada letra é um tile de 16 x 16 pixels:

| Letra | O que é |
|---|---|
| `#` | parede |
| `.` | chão |
| `H` | onde o herói começa |
| `S` | saída |
| `s`, `e`, `m` | slime, esqueleto, morcego (por enquanto viram chão: T51) |
| `C` | chefe |

O `Mapa` guarda as paredes, a saída e onde nasce cada um. A lista de níveis fica em `NIVEIS`, no `settings.py`, com os inimigos de cada andar anotados. Por enquanto só o Térreo tem mapa.

Para criar um inimigo novo: escreva uma classe filha de `Inimigo` em `personagens/inimigos.py`, chame `super().__init__(...)` com os números dele e escolha uma letra para o mapa.

## Pontuação e ranking

A `Pontuacao` já tem as regras, mas o jogo ainda não usa (T51):

- cada inimigo derrotado vale os seus pontos (Slime 50, Esqueleto 80, Morcego 70, Dragão 2000);
- nível concluído vale 500;
- só quem vence ganha bônus pelo tempo e pela vida que sobrou (`Pontuacao.aplicar_bonus`).

O `Ranking` guarda cada partida como um dicionário (nome, classe, pontos, venceu) em `src/data/ranking.json`. Ele é lido quando o jogo abre; salvar a partida e mostrar o quadro ainda faltam.

## Regras do código

- Herança com uma mãe só e `super()`. Nada de decoradores, `abc`, `typing`, `dataclasses`, `enum` ou anotações de tipo.
- Nada de `raise` ou `try`. Quando precisar conferir algo, um `if`.
- Os números do jogo ficam no `__init__` da classe ou no `settings.py`.
- Tudo que anda usa `velocidade * dt`, com `dt` em segundos.
- Docstring de 1 a 3 linhas por classe e comentários curtos em português.
