import pygame

from controle.controlador import Controlador
from jogo.nivel import Nivel
from mapa.carregador_texto import CarregadorTexto
from movimento.movimento_livre import MovimentoLivre
from personagens.personagem import Personagem
from personagens.tipos import Lado


class ControladorFixo(Controlador):
    """Devolve sempre os mesmos comandos e guarda a última Visao recebida."""

    def __init__(self, comandos=()):
        self.comandos = list(comandos)
        self.ultima_visao = None

    def gerar_comandos(self, visao):
        self.ultima_visao = visao
        return list(self.comandos)


def criar_nivel(tmp_path, desenho):
    (tmp_path / "m.txt").write_text(desenho, encoding="utf-8")
    return Nivel("Teste", 1, CarregadorTexto(tmp_path).carregar("m.txt"))


def criar_personagem(lado, x, y, vida=50, ataque=None):
    return Personagem(lado=lado, nome="P", posicao=pygame.Vector2(x, y), tamanho=pygame.Vector2(12, 12),
                      aparencia="x", vida_maxima=vida, velocidade=80, movimento=MovimentoLivre(),
                      ataque=ataque, pontos=50 if lado == Lado.MONSTROS else 0)


SALA = "##########\n#........#\n#........#\n#........#\n##########\n"


def test_adicionar_da_ids_diferentes(tmp_path):
    nivel = criar_nivel(tmp_path, SALA)
    a = nivel.adicionar(criar_personagem(Lado.HEROIS, 24, 24), ControladorFixo(), 160)
    b = nivel.adicionar(criar_personagem(Lado.MONSTROS, 100, 24), ControladorFixo(), 96)
    assert a != b
    assert nivel.buscar(a).id == a
    assert len(nivel.herois()) == 1 and len(nivel.monstros()) == 1
    assert not nivel.esta_limpo()


def test_observar_so_ve_quem_esta_no_raio(tmp_path):
    nivel = criar_nivel(tmp_path, SALA)
    heroi = nivel.adicionar(criar_personagem(Lado.HEROIS, 24, 24), ControladorFixo(), 50)
    nivel.adicionar(criar_personagem(Lado.MONSTROS, 60, 24), ControladorFixo(), 96)
    nivel.adicionar(criar_personagem(Lado.MONSTROS, 140, 24), ControladorFixo(), 96)
    visao = nivel.observar(heroi)
    assert visao.eu.id == heroi
    assert len(visao.avistados) == 1                     # o de x=140 está longe demais
    assert visao.mais_proximo(Lado.MONSTROS).posicao == pygame.Vector2(60, 24)
