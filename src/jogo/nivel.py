"""Classe Nivel: um nível em andamento e o tick que move tudo.

O que é:
    Junta um Mapa com quem está nele: personagens, controladores e
    projéteis. A cada tick faz as etapas abaixo, sempre nesta ordem, como
    o Simulacao::tick_atualizar da simulação lobo-coelho. O Nivel não sabe
    o formato do mapa (só usa a interface Mapa) e não desenha nada.

Atributos:
    - nome: str. Ex.: "Catacumbas".
    - numero: int.
    - mapa: Mapa.
    - personagens: dict[EntidadeId, Personagem].
    - controladores: dict[EntidadeId, Controlador]. Quem manda em cada um.
    - raios_visao: dict[EntidadeId, float]. Até onde cada um enxerga.
    - projeteis: dict[EntidadeId, Projetil].
    - fila: FilaComandos.
    - proximo_id: EntidadeId.

Montagem:
    - adicionar(personagem: Personagem, controlador: Controlador,
      raio_visao: float) -> EntidadeId.
    - trocar_controlador(id: EntidadeId, controlador: Controlador) -> bool:
      False se o id não existe.
    - remover(id: EntidadeId) -> Personagem | None: tira do nível (usado
      para levar os heróis ao próximo nível).
    - buscar(id: EntidadeId) -> Personagem | None.

Consultas:
    - observar(id: EntidadeId) -> Visao: monta o retrato do que esse
      personagem enxerga, como o Mundo::observar da simulação.
    - herois() -> list[Personagem] e monstros() -> list[Personagem].
    - esta_limpo() -> bool: nenhum monstro vivo (a saída abre).

O tick:
    - tick_atualizar(dt: float, tick: int) -> list[Evento]:
        1. coletar_comandos(tick): para cada personagem vivo, monta a
           Visao, chama controlador.gerar_comandos e põe na fila. Ninguém
           altera o mundo nesta etapa.
        2. executar_comandos(): esvazia a fila e aplica cada comando no
           personagem, se ele ainda existir e estiver vivo.
        3. mover_personagens(dt): personagem.movimento.atualizar(...) para
           cada um, e avancar_tempos(dt).
        4. resolver_combate(dt): ver jogo/combate.py.
        5. remover_mortos(): tira quem morreu e cria os eventos
           PersonagemDerrotado.
        6. checar_saida(): HeroiNaSaida quando um herói encosta na saída
           com o nível limpo.
      Devolve os eventos do tick para o Mundo aplicar as regras.

Quem usa: Mundo, RenderizadorNivel (só lê).
Usa: mapa/mapa.py, controle/, personagens/, jogo/combate.py,
jogo/eventos.py.
"""
