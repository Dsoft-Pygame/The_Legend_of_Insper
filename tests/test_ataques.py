import pygame

from movimento.movimento_livre import MovimentoLivre
from personagens.ataques.ataque_projetil import AtaqueProjetil
from personagens.personagem import Personagem
from personagens.tipos import Lado
from personagens.ataques.ataque_golpe import AtaqueGolpe


def criar_personagem(lado=Lado.HEROIS, x=50, y=50):
    p = Personagem(lado=lado, nome="P", posicao=pygame.Vector2(x, y), tamanho=pygame.Vector2(12, 12),
                   aparencia="x", vida_maxima=100, velocidade=80, movimento=MovimentoLivre())
    p.id = 1
    return p


def test_ataque_projetil_em_leque():
    heroi = criar_personagem()
    triplo = AtaqueProjetil(recarga=3, dano=10, velocidade=200, duracao=1, quantidade=3, abertura=30)
    projeteis = triplo.executar(heroi)
    assert len(projeteis) == 3
    assert all(p.lado == Lado.HEROIS and p.dono == heroi.id for p in projeteis)
    angulos = sorted(round(pygame.Vector2(1, 0).angle_to(p.velocidade)) for p in projeteis)
    assert angulos == [-15, 0, 15]


def test_anel_de_12():
    anel = AtaqueProjetil(recarga=5, dano=20, velocidade=90, duracao=1, quantidade=12, abertura=360)
    assert len(anel.executar(criar_personagem())) == 12


def test_golpe_frente_e_volta():
    heroi = criar_personagem()
    frente = AtaqueGolpe(recarga=0.5, dano=35, alcance=18, forma="frente").executar(heroi)[0]
    assert frente.velocidade == pygame.Vector2(0, 0)
    assert frente.posicao.x > heroi.posicao.x and not frente.atravessa
    giro = AtaqueGolpe(recarga=4, dano=25, alcance=32, forma="volta").executar(heroi)[0]
    assert giro.posicao == heroi.posicao and giro.atravessa