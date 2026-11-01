import settings


def test_tela_tem_resolucao_de_gba():
    assert settings.LARGURA_TELA == 240
    assert settings.ALTURA_TELA == 160


def test_pasta_data_existe():
    assert settings.PASTA_DATA.is_dir()


def test_cores_novas_existem():
    for nome in ["DARK_GRAY", "BROWN", "ORANGE", "CYAN", "PINK", "PURPLE", "MAGENTA"]:
        assert len(getattr(settings, nome)) == 3