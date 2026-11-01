"""Classe TelaClasses (herda de Tela): escolha da classe.

O que aparece:
    Um cartão para cada classe de data/classes.json (hoje Mago, Arqueiro e
    Bárbaro), cada um com imagem, nome e atributos. O cartão selecionado
    fica destacado, e embaixo aparece a descrição da classe selecionada.
    Uma classe nova no JSON aparece aqui sozinha.

Atributos:
    - cartoes: list[CartaoClasse]. Um por ClasseHeroi do Catalogo.
    - selecionado: int. Índice do cartão destacado.

O que faz:
    - tratar_entrada(entrada: EntradaMenu):
        * ESQUERDA e DIREITA mudam o selecionado;
        * CONFIRMAR grava a classe no PerfilJogador do P1 e troca para
          TelaJogo;
        * VOLTAR volta para TelaInicial.
    - desenhar(superficie): cartões e descrição.

Co-op (quando for feito): um selecionado por jogador, cada um mexendo com
o próprio dispositivo (a EntradaMenu diz de qual dispositivo veio cada
ação).

Usa: ui/cartao_classe.py, jogo/catalogo.py, aplicacao/sessao.py.
"""
