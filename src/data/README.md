# data/: o conteúdo do jogo

Tudo que é conteúdo mora aqui, e não no código: classes jogáveis, inimigos, temas e níveis, controles, aparências e mapas. Um inimigo novo que reaproveita um comportamento que já existe é só uma entrada em `inimigos.json`; nenhum arquivo `.py` muda.

Os arquivos abaixo ainda vão ser criados. Como JSON não aceita comentários, o formato de cada um fica documentado aqui. Todos os números são **valores de exemplo**, para ajustar no balanceamento.

Tempos (`recarga`, `duracao`) são em segundos. A lógica roda a 20 ticks por segundo, então eles andam de 0,05 em 0,05 s (0,3 s = 6 ticks), e um valor menor que 0,05 s dura um tick inteiro. Velocidades são em pixels por segundo.

Ao abrir o jogo, `jogo/catalogo.py` lê tudo e confere: campo faltando ou nome que não existe nos registros (IA, movimento, ataque, carregador de mapa) dá erro na hora, com o arquivo e a entrada, e não no meio da partida.

| Arquivo | O que guarda | Quem lê |
|---|---|---|
| `classes.json` | As classes jogáveis (Mago, Arqueiro, Bárbaro) | `Catalogo` → `Fabrica`, `TelaClasses` |
| `inimigos.json` | Os inimigos e o chefe: atributos, IA, movimento, ataques | `Catalogo` → `Fabrica` |
| `temas.json` | Os temas e os 3 níveis de cada um | `Catalogo` → `Mundo` |
| `controles.json` | Teclas e botões de cada dispositivo | `GerenciadorDispositivos` |
| `aparencias.json` | Cor, sprite ou animações de cada chave de aparência | `Aparencias` (render) |
| `mapas/*.txt` | Os mapas dos níveis, desenhados em texto | `CarregadorTexto` |
| `ranking.json` | As partidas jogadas (gerado pelo jogo, fora do git) | `Ranking` |

## classes.json

Cada classe tem atributos, um movimento, uma aparência, um `ataque` e um `especial`. O `tipo` do ataque é um nome do registro `personagens/ataques/registro.py` (`projetil` ou `golpe`); os outros campos são os parâmetros dele.

```json
{
  "mago": {
    "nome": "Mago",
    "descricao": "Frágil, mas com dano alto à distância.",
    "vida_maxima": 60, "velocidade": 70, "movimento": "livre", "aparencia": "mago",
    "ataque":   {"tipo": "projetil", "recarga": 0.6, "dano": 30, "velocidade": 90,
                 "duracao": 1.5, "quantidade": 1, "abertura": 0, "tamanho": 8, "aparencia": "bola_fogo"},
    "especial": {"tipo": "projetil", "recarga": 5.0, "dano": 20, "velocidade": 90,
                 "duracao": 1.0, "quantidade": 12, "abertura": 360, "tamanho": 8, "aparencia": "bola_fogo"}
  },
  "arqueiro": {
    "nome": "Arqueiro",
    "descricao": "Ágil, ataca rápido de longe.",
    "vida_maxima": 80, "velocidade": 100, "movimento": "livre", "aparencia": "arqueiro",
    "ataque":   {"tipo": "projetil", "recarga": 0.3, "dano": 10, "velocidade": 200,
                 "duracao": 1.0, "quantidade": 1, "abertura": 0, "tamanho": 4, "aparencia": "flecha"},
    "especial": {"tipo": "projetil", "recarga": 3.0, "dano": 10, "velocidade": 200,
                 "duracao": 1.0, "quantidade": 3, "abertura": 30, "tamanho": 4, "aparencia": "flecha"}
  },
  "barbaro": {
    "nome": "Bárbaro",
    "descricao": "Resistente, luta de perto.",
    "vida_maxima": 140, "velocidade": 75, "movimento": "livre", "aparencia": "barbaro",
    "ataque":   {"tipo": "golpe", "recarga": 0.5, "dano": 35, "alcance": 18,
                 "forma": "frente", "duracao": 0.1, "aparencia": "golpe"},
    "especial": {"tipo": "golpe", "recarga": 4.0, "dano": 25, "alcance": 32,
                 "forma": "volta", "duracao": 0.3, "aparencia": "giro"}
  }
}
```

## inimigos.json

Cada inimigo diz o `tipo` da IA (nome do registro `ia/registro.py`) com os parâmetros dela, o movimento (registro `movimento/registro.py`) e, se tiver, ataque e especial. `"chefe": true` faz a derrota dele vencer a partida.

```json
{
  "slime": {
    "nome": "Slime", "vida": 20, "velocidade": 30, "dano_contato": 10, "pontos": 50,
    "raio_visao": 96, "movimento": "livre", "aparencia": "slime",
    "decisao": {"tipo": "perseguir", "raio_alerta": 80, "distancia_ataque": 0, "tempo_vagando": 1.5}
  },
  "esqueleto": {
    "nome": "Esqueleto", "vida": 40, "velocidade": 55, "dano_contato": 15, "pontos": 80,
    "raio_visao": 128, "movimento": "livre", "aparencia": "esqueleto",
    "decisao": {"tipo": "perseguir", "raio_alerta": 112, "distancia_ataque": 0, "tempo_vagando": 1.0}
  },
  "morcego": {
    "nome": "Morcego", "vida": 10, "velocidade": 90, "dano_contato": 5, "pontos": 70,
    "raio_visao": 128, "movimento": "livre", "aparencia": "morcego",
    "decisao": {"tipo": "zigue_zague", "raio_alerta": 120, "periodo": 0.4, "amplitude": 0.8}
  },
  "dragao": {
    "nome": "Dragão Ancião", "vida": 600, "velocidade": 45, "dano_contato": 25, "pontos": 2000,
    "chefe": true, "raio_visao": 240, "movimento": "livre", "aparencia": "dragao",
    "decisao": {"tipo": "chefe", "intervalo_especial": 3.0, "lentidao_fase_1": 0.5, "distancia_ataque": 64},
    "ataque":   {"tipo": "projetil", "recarga": 1.0, "dano": 15, "velocidade": 120,
                 "duracao": 2.0, "quantidade": 1, "abertura": 0, "tamanho": 8, "aparencia": "bola_fogo"},
    "especial": {"tipo": "projetil", "recarga": 3.0, "dano": 15, "velocidade": 100,
                 "duracao": 2.0, "quantidade": 12, "abertura": 360, "tamanho": 8, "aparencia": "bola_fogo"}
  }
}
```

## temas.json

O tema ainda não foi decidido (torre, Insper ou dungeon), então todos podem ficar aqui e `padrao` diz qual o jogo usa. Cada nível diz o carregador de mapa (registro `mapa/registro.py`), o arquivo do mapa, quantos inimigos de cada tipo e, no último, o chefe.

```json
{
  "padrao": "torre",
  "temas": {
    "torre": {
      "nome": "Subindo a Torre",
      "direcao": "sobe",
      "niveis": [
        {"nome": "Térreo",        "carregador": "texto", "mapa": "mapas/torre_1.txt",
         "inimigos": {"slime": 6}},
        {"nome": "Biblioteca",    "carregador": "texto", "mapa": "mapas/torre_2.txt",
         "inimigos": {"slime": 4, "morcego": 4}},
        {"nome": "Topo da Torre", "carregador": "texto", "mapa": "mapas/torre_3.txt",
         "inimigos": {"esqueleto": 4}, "chefe": "dragao"}
      ]
    }
  }
}
```

Trocar de tema = mudar `padrao` (ou escolher outro tema numa tela, no futuro), sem mexer em nenhuma classe.

## controles.json

Os nomes das teclas são os do pygame (`pygame.key.key_code` converte). O teclado vira dois dispositivos para o co-op local.

```json
{
  "teclado_wasd":  {"tipo": "teclado", "cima": "w", "baixo": "s", "esquerda": "a", "direita": "d",
                    "ataque": "space", "especial": "left shift"},
  "teclado_setas": {"tipo": "teclado", "cima": "up", "baixo": "down", "esquerda": "left", "direita": "right",
                    "ataque": "right ctrl", "especial": "right shift"},
  "gamepad":       {"tipo": "gamepad", "zona_morta": 0.2, "ataque": 0, "especial": 1}
}
```

## aparencias.json

Para cada chave de aparência usada nos outros arquivos, uma de três formas:

- `cor`: nome de uma cor de `settings.py`, enquanto não houver arte;
- `sprite`: uma imagem parada em `assets/`;
- `folha`: uma folha de sprites em `assets/`, com animações.

Chave sem entrada aparece magenta no jogo.

```json
{
  "chao":   {"cor": "BLACK"},
  "parede": {"cor": "GRAY"},
  "saida":  {"cor": "YELLOW"},
  "mago":   {"cor": "BLUE"},
  "bola_fogo": {"cor": "RED"},
  "dragao": {"sprite": "dragao.png"},
  "slime": {
    "folha": "slime.png",
    "tamanho_quadro": [16, 16],
    "animacoes": {
      "parado":   {"linha": 0, "quadros": 2, "por_segundo": 2},
      "andando":  {"linha": 1, "quadros": 4, "por_segundo": 8},
      "atacando": {"linha": 2, "quadros": 3, "por_segundo": 10, "repete": false},
      "atingido": {"linha": 3, "quadros": 2, "por_segundo": 10, "repete": false}
    }
  }
}
```

Na folha, cada ação é uma linha (`linha` 0 é a de cima) e as imagens ficam lado a lado, todas do tamanho `tamanho_quadro`. `por_segundo` é a velocidade da animação em tempo real: não depende de ticks nem de fps. `repete` é `true` se omitido; ataque e "atingido" costumam parar na última imagem. Ação sem animação usa a de `"parado"`. As ações possíveis são as do personagem: `parado`, `andando`, `atacando`, `especial` e `atingido`. O personagem virado para a esquerda usa a mesma imagem espelhada.

## mapas/*.txt

Um caractere por tile de 16×16 pixels. Todas as linhas com o mesmo tamanho.

| Caractere | Significa |
|---|---|
| `#` | parede |
| `.` | chão |
| `H` | onde os heróis aparecem (P1 no primeiro, P2 no segundo ou ao lado) |
| `I` | onde um inimigo pode aparecer |
| `C` | onde o chefe aparece |
| `S` | saída (abre quando não sobra nenhum inimigo) |

```
##############################
#H...........#..........I....#
#............#...............#
#.....I......#####..########## 
#............................#
#...######.........I.........#
#...#....#...................#
#...#..I.#..........######..S#
##############################
```

Um mapa vindo do Tiled ou gerado por código entra com outro carregador, e este formato continua valendo para os mapas escritos à mão.
