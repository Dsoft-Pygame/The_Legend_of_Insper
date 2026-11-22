"""Um andar da torre em andamento: o mapa, o herói, os inimigos, os projéteis e as poções."""

import random

import pygame

from jogo.mapa import Mapa
from personagens.inimigos import Dragao, Esqueleto, Morcego, Slime
from personagens.pocao import Pocao
from settings import BLACK, BROWN, CHANCE_POCAO, DARK_GRAY, GRAY, YELLOW, TAMANHO_TILE
from ui import carregar_imagem

class Nivel:
    """Um nível em andamento: o mapa, o herói, os inimigos, os projéteis e as poções.

    A cada quadro faz todo mundo andar, resolve os golpes e tira quem morreu.
    """

    def __init__(self, nome, arquivo, chao, parede, heroi, pontuacao, som):
        """Lê o mapa, põe o herói no H, cria os inimigos das letras do mapa e o chefe no C, e escolhe os
        tiles do chão e das paredes.
        """
        self.nome = nome
        self.mapa = Mapa(arquivo)
        self.heroi = heroi
        self.pontuacao = pontuacao        # a mesma da partida inteira: passa de um nível para o outro
        self.som = som                    # o Som da Aplicacao, para tocar os acertos e as mortes
        self.heroi.posicao = pygame.Vector2(self.mapa.inicio_heroi)
        self.inimigos = []
        self.chao = []                    # (tile, imagem) de cada tile de chão, com a variante já escolhida
        self.paredes = []                 # o mesmo para as paredes
        self.montar_tiles(chao, parede)
        self.imagem_saida = carregar_imagem("saida.png")
        self.imagem_saida_aberta = carregar_imagem("saida_aberta.png")

        for letra, x, y in self.mapa.inimigos:
            self.inimigos.append(self.criar_inimigo(letra, x, y))
        self.chefe = None                 # o Dragão, só no nível que tem C no mapa
        if self.mapa.chefe is not None:
            self.chefe = Dragao(self.mapa.chefe[0], self.mapa.chefe[1])
            self.inimigos.append(self.chefe)
        self.projeteis = []
        self.pocoes = []                  # poções de vida que caíram dos inimigos
        self.tempo = 0                    # segundos neste nível (a saída pisca com ele)

    def montar_tiles(self, chao, parede):
        """Escolhe uma vez só o desenho de cada tile do chão e de cada parede."""
        imagens_chao = self.carregar_variantes(chao)
        imagens_parede = self.carregar_variantes(parede)
        for x in range(0, self.mapa.largura, TAMANHO_TILE):
            for y in range(0, self.mapa.altura, TAMANHO_TILE):
                tile = pygame.Rect(x, y, TAMANHO_TILE, TAMANHO_TILE)
                self.chao.append((tile, self.sortear_variante(imagens_chao, tile)))
        for tile in self.mapa.paredes:
            self.paredes.append((tile, self.sortear_variante(imagens_parede, tile)))

    def carregar_variantes(self, nome):
        """As 4 variantes de um tile: "chao" carrega tiles/chao_1.png até tiles/chao_4.png."""
        imagens = []
        for numero in range(1, 5):
            imagens.append(carregar_imagem("tiles/" + nome + "_" + str(numero) + ".png"))
        return imagens

    def sortear_variante(self, imagens, tile):
        """Escolhe a variante pela posição do tile, então o mesmo lugar sempre tem o mesmo desenho.
        A primeira (a lisa) aparece 3 vezes mais que as outras, para o chão não ficar poluído.
        """
        sorteio = random.Random(tile.x * 10000 + tile.y)   # a posição é a semente
        return sorteio.choices(imagens, weights=[3, 1, 1, 1])[0]

    def criar_inimigo(self, letra, x, y):
        """Cria o inimigo de uma letra do mapa: s slime, e esqueleto, m morcego."""
        if letra == "e":
            return Esqueleto(x, y)
        if letra == "m":
            return Morcego(x, y)
        return Slime(x, y)                # "s" e qualquer letra desconhecida viram slime

    def atualizar(self, dt):
        """Avança o nível dt segundos, nesta ordem: herói, inimigos, projéteis, acertos, contato, mortos e
        poções.
        """
        self.tempo += dt
        self.heroi.atualizar(dt, self.mapa)          # 1. o herói anda
        for inimigo in self.inimigos:                # 2. cada inimigo pensa, anda e mexe a animação
            self.projeteis.extend(inimigo.atualizar(dt, self.heroi, self.mapa))
            inimigo.deslizar(dt, self.mapa)          # o knockback que levou
            inimigo.animar(dt)
        self.mover_projeteis(dt)                     # 3. os projéteis andam
        self.aplicar_acertos()                       # 4. projétil que encosta dá dano
        self.aplicar_contato()                       # 5. inimigo encostado no herói dá dano
        self.remover_mortos()                        # 6. quem morreu sai do nível (e às vezes deixa uma poção)
        self.pegar_pocoes()                          # 7. poção encostada no herói cura

    def mover_projeteis(self, dt):
        """Os projéteis andam e somem os que bateram na parede ou acabaram o tempo."""
        restantes = []
        for projetil in self.projeteis:
            projetil.atualizar(dt)
            if not projetil.acabou(self.mapa):
                restantes.append(projetil)
        self.projeteis = restantes

    def aplicar_acertos(self):
        """Projétil do herói dá dano nos inimigos, e projétil de inimigo dá dano no herói.

        Cada projétil acerta cada alvo uma vez só. O que não atravessa some no primeiro acerto.
        """
        restantes = []
        for projetil in self.projeteis:
            alvos = self.inimigos
            if projetil.dono == "inimigo":
                alvos = [self.heroi]
            sumiu = False
            for alvo in alvos:
                if not sumiu and projetil.pode_acertar(alvo, self.mapa):
                    alvo.receber_dano(projetil.dano)
                    if projetil.dono == "heroi":
                        alvo.empurrar(projetil.direcao_empurrao(alvo), projetil.empurrao)
                    projetil.ja_acertou.append(alvo)
                    self.som.tocar("acerto")
                    if not projetil.atravessa:
                        sumiu = True          # flecha e bola de fogo param no primeiro que acertam
            if not sumiu:
                restantes.append(projetil)
        self.projeteis = restantes

    def aplicar_contato(self):
        """Inimigo encostado no herói dá dano. Depois de um golpe o herói fica piscando
        (invulnerável), então o dano não se repete a cada quadro.
        """
        for inimigo in self.inimigos:
            if inimigo.esta_vivo() and inimigo.retangulo().colliderect(self.heroi.retangulo()):
                self.heroi.receber_dano(inimigo.dano_contato)

    def remover_mortos(self):
        """Os inimigos sem vida saem do nível e somam os pontos deles."""
        vivos = []
        for inimigo in self.inimigos:
            if inimigo.esta_vivo():
                vivos.append(inimigo)
            elif inimigo is self.chefe:
                self.pontuacao.chefe_derrotado(inimigo.nome, inimigo.pontos)
                self.som.tocar("chefe_derrotado")
            else:
                self.pontuacao.inimigo_derrotado(inimigo.nome, inimigo.pontos)
                self.som.tocar("inimigo_derrotado")
                if random.random() < CHANCE_POCAO:
                    self.pocoes.append(Pocao(inimigo.posicao.x, inimigo.posicao.y))
        self.inimigos = vivos

    def pegar_pocoes(self):
        """O herói que encosta numa poção recupera vida, e a poção some."""
        restantes = []
        for pocao in self.pocoes:
            if pocao.retangulo().colliderect(self.heroi.retangulo()):
                self.heroi.curar(pocao.cura)
                self.som.tocar("menu_confirmar")
            else:
                restantes.append(pocao)
        self.pocoes = restantes

    def esta_limpo(self):
        """Sem inimigos, a saída abre."""
        return len(self.inimigos) == 0

    def heroi_na_saida(self):
        """True quando o herói encosta na saída aberta."""
        if self.mapa.saida is None or not self.esta_limpo():
            return False
        return self.heroi.retangulo().colliderect(self.mapa.saida)
        
    def desenhar(self, superficie, camera):
        """Desenha pela câmera o chão, as paredes, a saída (aberta ou fechada), as poções, os inimigos, os
        projéteis e o herói, nessa ordem.
        """
        superficie.fill(BLACK)
        for tile, imagem in self.chao:                 # o chão, tile por tile
            if camera.esta_visivel(tile):
                self.desenhar_tile(superficie, camera, tile, imagem, DARK_GRAY)
        for tile, imagem in self.paredes:
            if camera.esta_visivel(tile):
                self.desenhar_tile(superficie, camera, tile, imagem, GRAY)

        if self.mapa.saida is not None:
            if self.esta_limpo():                    # sem inimigos, a porta fica aberta
                self.desenhar_tile(superficie, camera, self.mapa.saida, self.imagem_saida_aberta, YELLOW)
            else:
                self.desenhar_tile(superficie, camera, self.mapa.saida, self.imagem_saida, BROWN)
                # Desenha as entidades por cima do cenário
        
        for pocao in self.pocoes:
            pocao.desenhar(superficie, camera)

        for inimigo in self.inimigos:
            inimigo.desenhar(superficie, camera)

        for projetil in self.projeteis:
            projetil.desenhar(superficie, camera)

        self.heroi.desenhar(superficie, camera)
    def desenhar_tile(self, superficie, camera, tile, imagem, cor): #usa imagem se existir
        """Desenha um tile com a imagem dele ou, se a imagem não existe, com um quadrado da cor."""
        if imagem is None:
            pygame.draw.rect(superficie, cor, camera.para_tela(tile))
        else:
            superficie.blit(imagem, camera.para_tela(tile))