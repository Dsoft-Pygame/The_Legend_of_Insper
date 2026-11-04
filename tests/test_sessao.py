from aplicacao.sessao import Sessao


def test_adicionar_jogador_numera_em_ordem():
    sessao = Sessao()
    p1 = sessao.adicionar_jogador("Ana", "teclado_wasd")
    p2 = sessao.adicionar_jogador("Beto", "teclado_setas")
    assert p1.numero == 1 and p2.numero == 2
    assert p1.classe is None
    assert sessao.buscar(2) is p2
    assert sessao.buscar(3) is None


def test_limpar_esvazia_os_jogadores():
    sessao = Sessao()
    sessao.adicionar_jogador("Ana", "teclado_wasd")
    sessao.venceu = True
    sessao.limpar()
    assert sessao.jogadores == []
    assert sessao.venceu is False 