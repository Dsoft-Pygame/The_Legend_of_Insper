from entrada.entrada_menu import AcaoMenu, EntradaMenu, EntradaQuadro


def test_entrada_vazia():
    quadro = EntradaQuadro()
    assert quadro.fechar is False
    assert quadro.menu.acoes == ()
    assert quadro.menu.texto == ""


def test_tem_e_dispositivo_de():
    menu = EntradaMenu(acoes=((AcaoMenu.CONFIRMAR, "teclado"),), texto="a")
    assert menu.tem(AcaoMenu.CONFIRMAR)
    assert not menu.tem(AcaoMenu.VOLTAR)
    assert menu.dispositivo_de(AcaoMenu.CONFIRMAR) == "teclado"
    assert menu.dispositivo_de(AcaoMenu.VOLTAR) is None