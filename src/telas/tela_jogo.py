"""Classe TelaJogo (herda de Tela): a tela onde se joga.

O que é:
    Uma tela "fina": quem controla a partida é o Mundo, e quem desenha o
    nível é o RenderizadorNivel. A TelaJogo só monta as peças, passa o
    tempo, desenha e decide quando a partida acabou.

Atributos:
    - mundo: Mundo.
    - renderizador: RenderizadorNivel.
    - hud: Hud.
    - aviso_nivel: float. Segundos restantes mostrando o nome do nível.

O que faz:
    - ao_entrar(): para CADA PerfilJogador da Sessao (um hoje, vários no
      co-op):
        1. pede o dispositivo dele ao GerenciadorDispositivos;
        2. cria o personagem com fabrica.criar_heroi(perfil.classe, ...);
        3. cria um ControladorHumano com esse dispositivo;
        4. junta tudo num Heroi.
      Depois cria o Mundo com a lista de heróis e o tema da Sessao.
    - tratar_entrada(entrada: EntradaMenu): VOLTAR pode pausar (futuro).
      O movimento dos heróis não passa por aqui: vem dos dispositivos,
      pelos controladores.
    - atualizar(dt): mundo.tempo_avancar(dt). Se mundo.terminou(), guarda
      o resultado e a pontuação na Sessao e troca para TelaResultado.
    - desenhar(superficie): renderizador.desenhar(superficie,
      mundo.nivel_atual) e, por cima, hud.desenhar(superficie,
      mundo.resumo()). Ao trocar de nível, mostra o nome dele no meio da
      tela por uns segundos.

Usa: jogo/mundo.py, jogo/fabrica.py, controle/controlador_humano.py,
render/renderizador_nivel.py, ui/hud.py,
entrada/gerenciador_dispositivos.py.
"""
