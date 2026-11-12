# Simplificação do código

A pedido do professor, o código do jogo foi refatorado para ficar bem mais simples. A primeira versão (branch `main`, até o commit `7b6e7ae`) foi pensada para ser muito modular, com muitas camadas, interfaces, classes abstratas e tratamento de erros. Para o tamanho do projeto, isso deixava o código difícil de ler e de mexer.

## O que saiu

- Decoradores, como `@dataclass`, `@property`, `@classmethod` e `@abstractmethod`.
- Classes abstratas com `abc` e interfaces com `typing.Protocol`. A herança agora é sempre de uma classe mãe só, com `super()`.
- Anotações de tipo, `typing`, `dataclasses` e `enum`.
- Tratamento de exceções com `raise` e `try`. Quando precisa conferir alguma coisa, é um `if`.
- Os testes com `pytest`: a pasta `tests/` e o `pytest.ini`.
- Os arquivos JSON de conteúdo (classes, inimigos, temas, controles e aparências). Os números foram para as próprias classes e para o `settings.py`.
- As camadas de controladores, comandos, fila de comandos, sistemas de decisão da IA, registros e fábrica.
- A lógica separada em 20 ticks por segundo, com interpolação no desenho. Agora tudo anda com `velocidade * dt` a cada quadro.

Não existia parte de rede (LAN): o ranking sempre foi um arquivo local, e continua assim.

## O que não mudou

O jogo faz o mesmo que a main fazia antes da simplificação: tela inicial, escolha de classe e o Térreo, com ataque, especial e câmera. As telas inicial, de classes e de jogo ficaram iguais às da main, pixel por pixel. Nada novo entrou no jogo, e o que já estava escrito mas ainda não ligado (inimigos, combate, pontuação e ranking) continua pronto para as próximas tarefas.

| | Antes (main) | Depois |
|---|---|---|
| Arquivos `.py` em `src/` | 60 | 19 |
| Linhas de Python em `src/` | 3.934 | 910 |
| Arquivos de teste | 22 | nenhum |
| Arquivos JSON de conteúdo | 5 | nenhum |

A organização nova está em [ARQUITETURA.md](ARQUITETURA.md).

## Uso de IA

A simplificação foi feita com ajuda de inteligência artificial: o Claude, da Anthropic, usado pelo Claude Code. A IA leu o código da main, propôs um plano do que tirar e de como refazer, reescreveu o código e fez os commits deste branch, uma parte do jogo por commit. O grupo aprovou o plano e definiu até onde ir: refazer só o que a main já tinha, sem terminar o jogo. Os commits feitos com a IA trazem a linha `Co-Authored-By: Claude` no fim da mensagem.
