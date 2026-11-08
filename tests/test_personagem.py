import pygame

from movimento.movimento_livre import MovimentoLivre
from personagens.personagem import DURACAO_ACAO, Personagem
from personagens.tipos import Lado


def criar(**extras):
    return Personagem(lado=Lado.HEROIS, nome="Mago", posicao=pygame.Vector2(40, 40),
                      tamanho=pygame.Vector2(12, 12), aparencia="mago", vida_maxima=60,
                      velocidade=70, movimento=MovimentoLivre(), **extras)


def test_comeca_com_vida_cheia_e_parado():
    p = criar()
    assert p.vida == p.vida_maxima == 60
    assert p.esta_vivo
    assert p.acao_atual == "parado"


def test_mover_guarda_intencao_e_vira_o_olhar():
    p = criar()
    p.mover(pygame.Vector2(-1, 0))
    assert p.intencao == pygame.Vector2(-1, 0)
    assert p.direcao_olhar == pygame.Vector2(-1, 0)


def test_mover_limita_o_tamanho_em_1():
    p = criar()
    p.mover(pygame.Vector2(3, 4))
    assert round(p.intencao.length(), 5) == 1


def test_atacar_e_especial_so_marcam_o_pedido():
    p = criar()
    p.atacar()
    p.especial()
    assert p.quer_atacar and p.quer_especial


def test_receber_dano_e_invulnerabilidade():
    p = criar(tempo_invulneravel=0.8)
    assert p.receber_dano(25, agressor=7) is True
    assert p.vida == 35 and p.ultimo_agressor == 7
    assert p.receber_dano(25, agressor=7) is False   # ainda invulnerável
    p.avancar_tempos(1.0)
    assert p.receber_dano(100, agressor=7) is True
    assert p.vida == 0 and not p.esta_vivo


def test_sem_ataque_nao_pode_atacar():
    assert criar().pode_atacar() is False


def test_mudar_acao_respeita_duracao_do_ataque():
    p = criar()
    p.mudar_acao("atacando")
    p.mudar_acao("andando")
    assert p.acao_atual == "atacando"                # o golpe não é cortado
    p.avancar_tempos(DURACAO_ACAO)
    p.mudar_acao("andando")
    assert p.acao_atual == "andando"
    p.avancar_tempos(0.1)
    p.mudar_acao("andando")
    assert round(p.tempo_na_acao, 5) == 0.1          # mesma ação não zera o tempo
