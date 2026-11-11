from jogo.ranking import Partida, Ranking


def test_ranking_ordena_salva_e_carrega(tmp_path):
    arquivo = tmp_path / "ranking.json"
    ranking = Ranking(arquivo)
    ranking.carregar()                                   # arquivo não existe: lista vazia
    assert ranking.partidas == []
    assert ranking.adicionar(Partida("Ana", "Mago", 500, False)) == 1
    assert ranking.adicionar(Partida("Beto", "Bárbaro", 900, True)) == 1
    assert ranking.adicionar(Partida("Caio", "Arqueiro", 100, False)) == 3
    de_novo = Ranking(arquivo)
    de_novo.carregar()
    assert [p.nome for p in de_novo.melhores(2)] == ["Beto", "Ana"]


def test_arquivo_estragado_nao_trava(tmp_path):
    arquivo = tmp_path / "ranking.json"
    arquivo.write_text("isso não é json", encoding="utf-8")
    ranking = Ranking(arquivo)
    ranking.carregar()
    assert ranking.partidas == []