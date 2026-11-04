from jogo.catalogo import Catalogo


def test_carrega_os_dados_do_jogo():
    catalogo = Catalogo.carregar()
    assert set(catalogo.classes) == {"mago", "arqueiro", "barbaro"}
    assert catalogo.classes["mago"].nome == "Mago"
    assert catalogo.inimigos["dragao"].chefe is True
    assert catalogo.inimigos["slime"].chefe is False
    tema = catalogo.temas[catalogo.tema_padrao]
    assert len(tema.niveis) == 3
    assert tema.niveis[2].chefe == "dragao"
    assert "teclado_wasd" in catalogo.controles
    assert "chao" in catalogo.aparencias