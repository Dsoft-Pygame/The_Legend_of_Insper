from jogo.pontuacao import Pontuacao


def test_soma_inimigos_niveis_e_chefe():
    p = Pontuacao()
    p.inimigo_derrotado("Slime", 50)
    p.inimigo_derrotado("Slime", 50)
    p.nivel_concluido("Térreo")
    p.chefe_derrotado("Dragão Ancião", 2000)
    assert p.total == 2600
    assert p.inimigos_derrotados == 3
    assert "Térreo concluído +500" in p.extrato


def test_bonus_so_se_venceu():
    perdeu = Pontuacao()
    perdeu.aplicar_bonus(venceu=False, tempo=60, vida_restante=1.0)
    assert perdeu.total == 0
    venceu = Pontuacao()
    venceu.aplicar_bonus(venceu=True, tempo=0, vida_restante=1.0)
    assert venceu.total == 3000 + 1000