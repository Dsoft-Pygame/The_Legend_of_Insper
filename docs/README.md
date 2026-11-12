# The Legend of Insper

Jogo de ação top-down em Python com [pygame](https://www.pygame.org/). O jogador digita o nome, escolhe uma classe (Mago, Arqueiro ou Bárbaro) e atravessa três níveis, cada um maior que a tela, até enfrentar o chefe no último. Ganhando ou perdendo, a pontuação vai para o ranking.

## Estado atual

A arquitetura está definida e todos os arquivos existem, mas só com o docstring do que cada um vai conter. O código ainda vai ser escrito, na ordem sugerida em [ARQUITETURA.md](ARQUITETURA.md#ordem-sugerida-para-implementar).

O desenho deixa cada sistema trocável sem mexer no resto: o personagem só expõe ações e não sabe quem manda nele (teclado, controle ou IA), o jeito de andar e o mapa ficam atrás de interfaces, e inimigos, classes e níveis são dados em JSON. O jogo também já está preparado para co-op local. A lógica roda a 20 ticks por segundo e a tela a 60 quadros por segundo, com o movimento e as animações lisos entre um tick e outro.

## Como rodar (quando houver código)

Requisitos: Python 3.10 ou mais novo.

```
pip install -r requirements.txt
python src/main.py
```

## Controles planejados

Configuráveis em `src/data/controles.json`.

| | Andar | Atacar | Especial |
|---|---|---|---|
| Jogador 1 (teclado) | W A S D | Espaço | Shift esquerdo |
| Jogador 2 (teclado, co-op) | Setas | Ctrl direito | Shift direito |
| Controle | Analógico ou direcional | Botão 0 | Botão 1 |

Nos menus: setas ou WASD navegam, Enter confirma, Esc volta e Backspace apaga.

## Estrutura

```
src/
├── main.py, settings.py
├── aplicacao/     loop principal e sessão com os jogadores
├── entrada/       teclado, controles e eventos (único lugar com pygame.event e pygame.key)
├── telas/         tela inicial, classes, jogo e resultado
├── ui/            caixa de texto, ranking, cartão de classe, HUD
├── render/        câmera e desenho do nível
├── jogo/          mundo, nível, combate, fábrica, dados, pontuação, ranking
├── controle/      controladores (humano e IA), comandos e fila de comandos
├── ia/            sistemas de decisão dos inimigos
├── personagens/   personagem, projétil, visão, classe do herói, ataques
├── movimento/     jeitos de andar (livre, grade)
├── mapa/          interface do mapa e carregadores
├── assets/        arte e sons
└── data/          conteúdo do jogo em JSON e mapas em texto
```

## Documentação

- [ARQUITETURA.md](ARQUITETURA.md): camadas, classes, fluxo do input até a ação, ciclo do tick, telas, co-op e ordem de implementação.
