# Como trocar cada sistema

Guia curto de onde mexer para trocar ou adicionar cada peça do jogo. A regra geral: **conteúdo novo é dado** (um JSON em `src/data/`), **comportamento novo é um arquivo** numa pasta + **uma linha no registro** dela. Nenhum outro arquivo muda.

Por que funciona assim está em [ARQUITETURA.md](ARQUITETURA.md); o formato dos JSON está em [src/data/README.md](../src/data/README.md).

## Trocar o mapa

**Outro mapa do mesmo tipo (texto):**

1. Crie `src/data/mapas/<nome>.txt` com `#` parede, `.` chão, `H` heróis, `I` inimigos, `C` chefe e `S` saída.
2. Em `src/data/temas.json`, aponte o nível para ele: `"mapa": "mapas/<nome>.txt"`.

**Outro sistema de mapa inteiro** (Tiled, gerado por código, outro formato):

1. Crie `mapa/mapa_<nome>.py` com uma classe que cumpre a interface `Mapa` (`largura`, `altura`, `area_livre`, `surgimentos`, `saida`, `ladrilhos_em`).
2. Crie `mapa/carregador_<nome>.py` com uma classe que cumpre `CarregadorMapa` (`carregar(origem) -> Mapa`).
3. Em `mapa/registro.py`, uma linha: `"<nome>"` → a classe do carregador.
4. Em `src/data/temas.json`, use `"carregador": "<nome>"` nos níveis que quiser.

Não muda: personagens, movimento, IA, combate e render. Todos só fazem as perguntas da interface `Mapa`.

## Trocar o movimento

**De um personagem ou inimigo:** no `classes.json` ou `inimigos.json`, troque o campo `"movimento"`, por exemplo de `"livre"` para `{"tipo": "grade", "tamanho_passo": 16}`.

**No meio do jogo** (ex.: ao pisar no gelo): o código do jogo entrega outro objeto ao personagem (`personagem.movimento` passa a ser outro `Movimento`). O personagem não muda.

**Criar um jeito novo de andar** (ex.: com inércia e atrito):

1. Crie `movimento/movimento_<nome>.py` com uma classe que tem `atualizar(corpo, mapa, dt)`. Ela lê `corpo.intencao`, move `corpo.posicao`, pergunta `mapa.area_livre(...)` antes de andar e zera a intenção no fim.
2. Em `movimento/registro.py`, uma linha: `"<nome>"` → a classe.
3. Use `"movimento": "<nome>"` no JSON.

## Trocar ou adicionar um inimigo

**Inimigo novo que reaproveita uma IA existente** (nenhum `.py` muda):

1. Em `src/data/inimigos.json`, uma entrada nova com vida, velocidade, dano de contato, pontos, raio de visão, movimento, aparência e `"decisao": {"tipo": "perseguir", ...}` (ou outra IA do registro). Ataque e especial são opcionais.
2. Em `src/data/aparencias.json`, a cor ou o sprite da aparência dele.
3. Em `src/data/temas.json`, coloque o tipo nos níveis em que ele aparece: `"inimigos": {"<tipo>": 3}`.

**Mudar um inimigo que já existe:** só os números no `inimigos.json`.

**Trocar o chefe:** crie o inimigo novo com `"chefe": true` e troque o `"chefe"` do último nível no `temas.json`.

## Trocar a IA

**A IA de um inimigo:** troque o `"tipo"` do campo `"decisao"` no `inimigos.json` (ex.: o esqueleto passa a usar `"zigue_zague"`).

**Criar uma IA nova** (ex.: um inimigo que foge e atira):

1. Crie `ia/decisao_<nome>.py` com uma classe que tem `decidir(visao, gerador) -> list[Comando]`. As regras de toda IA:
    - olha só a `Visao` (onde estão os outros, vidas, recargas, o mapa para perguntas);
    - devolve comandos (`Mover`, `Atacar`, `Especial`) e não altera nada;
    - toda sorte vem de `gerador`, nunca do `random` global;
    - pode guardar memória própria (cada inimigo tem a sua instância).
2. Em `ia/registro.py`, uma linha: `"<nome>"` → a classe.
3. Use `"decisao": {"tipo": "<nome>", ...parâmetros}` no `inimigos.json`.

**Trocar quem controla um personagem durante o jogo:** o `Nivel` tem `trocar_controlador(id, controlador)`. Com um `ControladorIA`, um herói vai para o piloto automático; com um `ControladorHumano`, um jogador passa a controlar um inimigo. O personagem não muda.

## Trocar o controle de um jogador

- **Teclas:** edite `src/data/controles.json` (nomes de tecla do pygame).
- **Jogar com controle em vez de teclado:** o `PerfilJogador` dele recebe o dispositivo `"gamepad_0"` em vez de `"teclado_wasd"`. O `ControladorHumano` é o mesmo.
- **Um tipo de dispositivo novo** (ex.: tela de toque): uma classe em `entrada/` com `nome` e `ler() -> EstadoEntrada`, registrada no `GerenciadorDispositivos`.

## Adicionar o segundo jogador (co-op local)

O resto do jogo já trabalha com listas: `TelaJogo` cria um herói e um controlador para cada jogador da `Sessao`, o `Mundo` guarda uma lista de heróis, a câmera segue o centro deles, o HUD desenha uma barra por herói, a derrota é quando todos caem e a IA persegue o mais próximo. Falta só deixar o segundo jogador entrar:

1. **TelaInicial:** quando chegar um `CONFIRMAR` de um dispositivo que ainda não tem dono (a `EntradaMenu` diz qual foi, e o `GerenciadorDispositivos` diz se está livre), crie o segundo perfil com `sessao.adicionar_jogador(nome, dispositivo)`. Com um teclado só, o P1 usa `teclado_wasd` e o P2 usa `teclado_setas`.
2. **TelaClasses:** um cartão selecionado por jogador; cada ação de menu move o seletor do jogador dono daquele dispositivo. Vai para a `TelaJogo` quando todos confirmarem.
3. **Mapas:** coloque um segundo `H`, ou deixe o P2 aparecer ao lado do primeiro.
4. **Ranking:** decidir como salvar uma partida de dois (ex.: nomes juntos, "Ana e Beto").

Tela dividida, se um dia for preciso, são duas `Camera` e dois desenhos na `TelaJogo`, sem mexer na partida.

## Adicionar uma classe jogável

1. Em `src/data/classes.json`, uma entrada com nome, descrição, vida, velocidade, movimento, aparência, `ataque` e `especial` (tipos de ataque do registro, com os parâmetros).
2. Em `src/data/aparencias.json`, a aparência dela.

A `TelaClasses` mostra todas as classes do JSON, então ela aparece sozinha. Um tipo de ataque realmente novo é um arquivo em `personagens/ataques/` + uma linha em `personagens/ataques/registro.py`.

## Trocar a arte

Em `src/data/aparencias.json`, troque `{"cor": "GREEN"}` por `{"sprite": "slime.png"}` e coloque o arquivo em `src/assets/`. Nenhuma entidade muda: elas só guardam a chave `"slime"`.

**Para animar:** desenhe uma folha de sprites com uma linha por ação (parado, andando, atacando...) e troque a entrada por `{"folha": "slime.png", "tamanho_quadro": [16, 16], "animacoes": {...}}`, com quantas imagens e quantas por segundo cada ação tem (formato em [src/data/README.md](../src/data/README.md#aparenciasjson)). Ação sem animação usa a de `"parado"`. Nenhum código muda: o personagem já diz o que está fazendo (`acao_atual`) e o render escolhe a imagem pelo tempo.

## Trocar quantos ticks e quadros por segundo

- **Lógica:** em `jogo/mundo.py`, mude `TICKS_POR_SEGUNDO` (hoje 20).
- **Tela:** em `aplicacao/aplicacao.py`, mude `QUADROS_POR_SEGUNDO` (hoje 60).

Mais nada muda: tudo que anda ou espera usa `dt` em segundos, as animações usam o tempo, e o render interpola entre dois ticks seja qual for a proporção. Mais ticks respondem mais rápido ao controle e gastam mais processamento; menos ticks deixam cada passo maior (projéteis rápidos já andam em subpassos de 8 px, então não atravessam parede). Recargas e durações viram múltiplos do tick: a 20 ticks, de 0,05 em 0,05 s.
