from personagens.tipos import Lado

def test_lado_oposto():
    assert Lado.HEROIS.oposto() == Lado.MONSTROS
    assert Lado.MONSTROS.oposto() == Lado.HEROIS