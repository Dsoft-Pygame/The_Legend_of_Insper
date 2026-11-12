import pygame

from jogo import combate
from mapa.mapa_tiles import MapaTiles
from movimento.movimento_livre import MovimentoLivre
from personagens.ataques.ataque_projetil import AtaqueProjetil
from personagens.personagem import Personagem
from personagens.projetil import Projetil
from personagens.tipos import Lado


def criar_personagem(lado, x, y, ataque=None, dano_contato=0, invulneravel=0.0):
    p = Personagem(lado=lado, nome="P", posicao=pygame.Vector2(x, y), tamanho=pygame.Vector2(12, 12),
                   aparencia="x", vida_maxima=100, velocidade=80, movimento=MovimentoLivre(),
                   ataque=ataque, dano_contato=dano_contato, tempo_invulneravel=invulneravel)
    p.id = id(p) % 10000
    return p


def mapa_aberto(colunas=20, linhas=5, parede_na_coluna=None):
    celulas = [["chao"] * colunas for _ in range(linhas)]
    if parede_na_coluna is not None:
        for linha in celulas:
            linha[parede_na_coluna] = "parede"
    return MapaTiles(celulas, {}, 16)


def test_disparar_ataques_comeca_recarga():
    heroi = criar_personagem(Lado.HEROIS, 50, 50, ataque=AtaqueProjetil(0.3, 10, 200, 1))
    heroi.atacar()
    novos = combate.disparar_ataques([heroi])
    assert len(novos) == 1
    assert heroi.recarga_ataque == 0.3 and heroi.acao_atual == "atacando"
    assert heroi.quer_atacar is False
    heroi.atacar()
    assert combate.disparar_ataques([heroi]) == []   # ainda recarregando


def test_projetil_rapido_nao_atravessa_parede():
    mapa = mapa_aberto(parede_na_coluna=3)             # parede de x=48 a x=64
    flecha = Projetil(Lado.HEROIS, 1, pygame.Vector2(40, 40), pygame.Vector2(4, 4), "flecha",
                      pygame.Vector2(600, 0), dano=10, duracao=1)   # 30 px por tick!
    flecha.id = 99
    assert combate.mover_projeteis([flecha], mapa, 0.05) == [99]
    assert flecha.posicao.x < 64


def test_acerto_tira_vida_uma_vez_e_some():
    alvo = criar_personagem(Lado.MONSTROS, 60, 40)
    flecha = Projetil(Lado.HEROIS, 1, pygame.Vector2(40, 40), pygame.Vector2(4, 4), "flecha",
                      pygame.Vector2(400, 0), dano=10, duracao=1)
    flecha.id = 5
    combate.mover_projeteis([flecha], mapa_aberto(), 0.05)   # passa por cima do alvo neste tick
    assert combate.aplicar_acertos([flecha], [alvo]) == [5]
    assert alvo.vida == 90 and alvo.ultimo_agressor == 1


def test_projetil_nao_acerta_o_proprio_lado():
    amigo = criar_personagem(Lado.HEROIS, 44, 40)
    flecha = Projetil(Lado.HEROIS, 1, pygame.Vector2(40, 40), pygame.Vector2(4, 4), "flecha",
                      pygame.Vector2(100, 0), dano=10, duracao=1)
    combate.mover_projeteis([flecha], mapa_aberto(), 0.05)
    assert combate.aplicar_acertos([flecha], [amigo]) == []
    assert amigo.vida == 100


def test_contato_machuca_heroi_com_invulnerabilidade():
    heroi = criar_personagem(Lado.HEROIS, 40, 40, invulneravel=0.8)
    slime = criar_personagem(Lado.MONSTROS, 44, 40, dano_contato=10)
    combate.aplicar_contato([heroi, slime])
    combate.aplicar_contato([heroi, slime])
    assert heroi.vida == 90                           # só uma vez, por causa da invulnerabilidade
