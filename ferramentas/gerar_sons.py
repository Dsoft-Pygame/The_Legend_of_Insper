"""Gera os sons do jogo por síntese (ondas quadrada, triangular e ruído), só com a biblioteca padrão.

Cria em src/assets/sons/ os 8 efeitos (.wav) e as 4 músicas (.ogg) que o src/sons.py espera.
Para o .ogg usa o ffmpeg, se ele estiver instalado. Sem o ffmpeg, deixa as músicas em .wav.

Como rodar, da raiz do repositório:
    python ferramentas/gerar_sons.py

Os números aleatórios usam semente fixa: rodar de novo gera os mesmos arquivos.
"""
import math
import os
import random
import shutil
import struct
import subprocess
import wave

TAXA = 44100                                  # amostras por segundo
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "assets", "sons")

random.seed(7)


# ---------------------------------------------------------------- ondas e envelope

def frequencia(nota):
    """Nota MIDI (60 = Dó central) -> frequência em Hz."""
    return 440.0 * 2 ** ((nota - 69) / 12)


def onda(tipo, fase, largura=0.5):
    """Valor da onda (-1 a 1) numa fase de 0 a 1."""
    if tipo == "quadrada":
        if fase < largura:
            return 1.0
        return -1.0
    if tipo == "triangular":
        return 4 * abs(fase - 0.5) - 1
    if tipo == "serra":
        return 2 * fase - 1
    if tipo == "seno":
        return math.sin(2 * math.pi * fase)
    return random.uniform(-1, 1)              # "ruido"


def envelope(i, total, ataque, liberacao):
    """Volume de 0 a 1: sobe no ataque, fica, e desce na liberação (em amostras)."""
    if i < ataque:
        return i / ataque
    if i > total - liberacao:
        return max(0.0, (total - i) / liberacao)
    return 1.0


def tom(buffer, inicio, duracao, freq, freq_final=None, tipo="quadrada", volume=0.3,
        ataque=0.005, liberacao=0.05, largura=0.5, vibrato=0.0, decaimento=0.0):
    """Soma um tom no buffer. freq_final faz a frequência deslizar (em escala exponencial)."""
    if freq_final is None:
        freq_final = freq
    comeco = int(inicio * TAXA)
    total = int(duracao * TAXA)
    a = max(1, int(ataque * TAXA))
    r = max(1, int(liberacao * TAXA))
    fase = 0.0
    for i in range(total):
        pos = comeco + i
        if pos >= len(buffer):
            break
        t = i / total
        f = freq * (freq_final / freq) ** t
        if vibrato > 0:
            f = f * (1 + vibrato * math.sin(2 * math.pi * 5.5 * i / TAXA))
        fase = (fase + f / TAXA) % 1.0
        v = volume * envelope(i, total, a, r)
        if decaimento > 0:
            v = v * math.exp(-decaimento * i / TAXA)
        buffer[pos] += v * onda(tipo, fase, largura)


def ruido(buffer, inicio, duracao, volume=0.3, decaimento=8.0, corte=1.0, corte_final=None):
    """Soma um ruído que some aos poucos. corte (0 a 1) abafa o som: perto de 0 fica grave."""
    if corte_final is None:
        corte_final = corte
    comeco = int(inicio * TAXA)
    total = int(duracao * TAXA)
    anterior = 0.0
    for i in range(total):
        pos = comeco + i
        if pos >= len(buffer):
            break
        t = i / total
        c = corte + (corte_final - corte) * t
        anterior = anterior + c * (random.uniform(-1, 1) - anterior)   # filtro passa-baixa simples
        v = volume * math.exp(-decaimento * i / TAXA) * envelope(i, total, 20, 200)
        buffer[pos] += v * anterior


def suavizar(buffer, corte):
    """Filtro passa-baixa de um polo: tira o chiado das ondas quadradas."""
    anterior = 0.0
    for i in range(len(buffer)):
        anterior = anterior + corte * (buffer[i] - anterior)
        buffer[i] = anterior


def normalizar(buffer, pico=0.85):
    maior = max(abs(x) for x in buffer)
    if maior > 0:
        fator = pico / maior
        for i in range(len(buffer)):
            buffer[i] = buffer[i] * fator


def salvar_wav(buffer, caminho):
    with wave.open(caminho, "wb") as arquivo:
        arquivo.setnchannels(1)
        arquivo.setsampwidth(2)
        arquivo.setframerate(TAXA)
        dados = bytearray()
        for x in buffer:
            x = max(-1.0, min(1.0, x))
            dados += struct.pack("<h", int(x * 32767))
        arquivo.writeframes(bytes(dados))


def vazio(segundos):
    return [0.0] * int(segundos * TAXA)


# ---------------------------------------------------------------- efeitos

def efeito_ataque():
    """Golpe: um "fuuu" de ruído que desce, com um estalo agudo no começo."""
    b = vazio(0.22)
    ruido(b, 0, 0.22, volume=0.6, decaimento=12, corte=0.6, corte_final=0.05)
    tom(b, 0, 0.08, frequencia(84), frequencia(60), tipo="quadrada", volume=0.25, largura=0.25)
    return b


def efeito_acerto():
    """Pancada: batida grave que cai rápido e um pouco de ruído."""
    b = vazio(0.16)
    tom(b, 0, 0.14, 220, 60, tipo="quadrada", volume=0.5, liberacao=0.04, largura=0.5)
    ruido(b, 0, 0.08, volume=0.5, decaimento=30, corte=0.8)
    return b


def efeito_inimigo_derrotado():
    """Inimigo some: arpejo descendente e um ruído de "puf"."""
    b = vazio(0.45)
    notas = [76, 72, 67, 60]
    for k in range(len(notas)):
        tom(b, k * 0.07, 0.09, frequencia(notas[k]), tipo="quadrada", volume=0.3, largura=0.25)
    ruido(b, 0.25, 0.2, volume=0.35, decaimento=15, corte=0.3)
    return b


def efeito_chefe_derrotado():
    """Chefe cai: explosão longa e depois uma fanfarra de vitória."""
    b = vazio(2.2)
    ruido(b, 0, 1.2, volume=0.8, decaimento=3, corte=0.5, corte_final=0.03)
    tom(b, 0, 0.6, 120, 30, tipo="quadrada", volume=0.4, liberacao=0.2)
    fanfarra = [(60, 0.0, 0.12), (64, 0.12, 0.12), (67, 0.24, 0.12), (72, 0.36, 0.7)]
    for nota, quando, dur in fanfarra:
        tom(b, 0.8 + quando, dur, frequencia(nota), tipo="quadrada", volume=0.28, largura=0.25,
            liberacao=0.08, vibrato=0.004)
        tom(b, 0.8 + quando, dur, frequencia(nota - 12), tipo="triangular", volume=0.3, liberacao=0.08)
    return b


def efeito_heroi_derrotado():
    """Derrota: notas tristes que descem e ficam mais lentas."""
    b = vazio(1.5)
    notas = [(67, 0.0, 0.25), (66, 0.25, 0.25), (65, 0.5, 0.3), (64, 0.8, 0.65)]
    for nota, quando, dur in notas:
        tom(b, quando, dur, frequencia(nota), tipo="quadrada", volume=0.28, largura=0.5,
            liberacao=0.1, vibrato=0.006)
        tom(b, quando, dur, frequencia(nota - 24), tipo="triangular", volume=0.35, liberacao=0.1)
    tom(b, 0.8, 0.65, frequencia(64), frequencia(52), tipo="triangular", volume=0.2, liberacao=0.3)
    return b


def efeito_porta():
    """Passar pela porta: subida rápida, como um teletransporte."""
    b = vazio(0.55)
    tom(b, 0, 0.45, 200, 1200, tipo="quadrada", volume=0.22, largura=0.25, liberacao=0.15)
    notas = [60, 67, 72, 79]
    for k in range(len(notas)):
        tom(b, 0.05 + k * 0.08, 0.1, frequencia(notas[k]), tipo="triangular", volume=0.35)
    return b


def efeito_menu_mover():
    """Mexer no menu: bip curtinho."""
    b = vazio(0.06)
    tom(b, 0, 0.05, frequencia(81), tipo="quadrada", volume=0.3, largura=0.25, liberacao=0.02)
    return b


def efeito_menu_confirmar():
    """Confirmar: dois bips subindo."""
    b = vazio(0.2)
    tom(b, 0, 0.06, frequencia(76), tipo="quadrada", volume=0.3, largura=0.25, liberacao=0.02)
    tom(b, 0.06, 0.13, frequencia(83), tipo="quadrada", volume=0.3, largura=0.25, liberacao=0.06)
    return b


# ---------------------------------------------------------------- músicas

def tocar_linha(b, notas, bpm, tipo, volume, oitava=0, largura=0.5, vibrato=0.0, legato=0.9):
    """notas: lista de (nota MIDI ou None para pausa, duração em tempos). Toca em sequência."""
    tempo = 60.0 / bpm
    agora = 0.0
    for nota, tempos in notas:
        dur = tempos * tempo
        if nota is not None:
            tom(b, agora, dur * legato, frequencia(nota + oitava), tipo=tipo, volume=volume,
                largura=largura, vibrato=vibrato, liberacao=min(0.08, dur * 0.4))
        agora += dur


def bateria(b, padrao, bpm, compassos, volume=0.3):
    """padrao: texto de 8 posições por compasso (colcheias). B = bumbo, c = caixa, h = chimbal."""
    colcheia = 60.0 / bpm / 2
    for c in range(compassos):
        for k in range(len(padrao)):
            quando = (c * len(padrao) + k) * colcheia
            letra = padrao[k]
            if letra == "B":
                tom(b, quando, 0.12, 150, 45, tipo="seno", volume=volume * 1.6, liberacao=0.05)
            elif letra == "c":
                ruido(b, quando, 0.12, volume=volume * 0.9, decaimento=25, corte=0.7)
            elif letra == "h":
                ruido(b, quando, 0.04, volume=volume * 0.35, decaimento=60, corte=1.0)


def acordes_em_baixo(acordes, padrao):
    """Linha de baixo: cada acorde (nota raiz) vira um compasso no padrão dado (lista de (intervalo, tempos))."""
    linha = []
    for raiz in acordes:
        for intervalo, tempos in padrao:
            if intervalo is None:
                linha.append((None, tempos))
            else:
                linha.append((raiz + intervalo, tempos))
    return linha


def arpejo(acordes, notas_por_compasso, tempos_cada):
    """Arpejo: cada acorde é uma lista de notas tocadas uma por vez, repetindo."""
    linha = []
    for acorde in acordes:
        for k in range(notas_por_compasso):
            linha.append((acorde[k % len(acorde)], tempos_cada))
    return linha


def musica_menu():
    """Calma, em Lá menor: arpejo suave, melodia lenta e baixo. 90 bpm, 8 compassos."""
    bpm = 90
    compassos = 8
    b = vazio(compassos * 4 * 60 / bpm)
    acordes = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62],
               [57, 60, 64], [53, 57, 60], [52, 56, 59], [52, 56, 59]]
    tocar_linha(b, arpejo(acordes, 8, 0.5), bpm, "triangular", 0.22, oitava=12)
    melodia = [(76, 2), (74, 1), (72, 1), (72, 3), (None, 1),
               (72, 1), (71, 1), (69, 2), (71, 3), (None, 1),
               (76, 2), (77, 1), (76, 1), (74, 3), (72, 1),
               (71, 2), (72, 1), (71, 1), (68, 3), (None, 1)]
    tocar_linha(b, melodia, bpm, "quadrada", 0.12, largura=0.25, vibrato=0.004)
    raizes = [45, 41, 36, 43, 45, 41, 40, 40]
    tocar_linha(b, acordes_em_baixo(raizes, [(0, 2), (7, 2)]), bpm, "triangular", 0.32)
    suavizar(b, 0.35)
    return b


def musica_torre():
    """Aventura, em Ré menor: melodia que anda, baixo pulsando e bateria. 132 bpm, 16 compassos."""
    bpm = 132
    compassos = 16
    b = vazio(compassos * 4 * 60 / bpm)
    raizes = [38, 46, 48, 45, 38, 46, 43, 45] * 2
    tocar_linha(b, acordes_em_baixo(raizes, [(0, 0.5), (0, 0.5), (12, 0.5), (0, 0.5)] * 2),
                bpm, "triangular", 0.35, legato=0.8)
    frase_a = [(62, 1), (65, 0.5), (69, 0.5), (67, 1), (65, 1),
               (70, 1.5), (69, 0.5), (67, 2),
               (67, 1), (69, 0.5), (70, 0.5), (72, 1), (70, 1),
               (69, 3), (None, 1)]
    frase_b = [(74, 1), (72, 0.5), (70, 0.5), (69, 1), (67, 1),
               (70, 1.5), (69, 0.5), (67, 2),
               (67, 1), (65, 0.5), (64, 0.5), (65, 1), (67, 1),
               (69, 2), (73, 2)]
    melodia = frase_a + frase_b + frase_a + [(74, 1), (72, 0.5), (70, 0.5), (69, 1), (67, 1),
                                             (65, 1.5), (64, 0.5), (62, 2),
                                             (64, 1), (65, 1), (67, 1), (64, 1),
                                             (62, 3), (None, 1)]
    tocar_linha(b, melodia, bpm, "quadrada", 0.13, largura=0.25, vibrato=0.003)
    tocar_linha(b, melodia, bpm, "quadrada", 0.05, oitava=-12, largura=0.5)
    bateria(b, "Bhchbhch", bpm, compassos, volume=0.22)
    suavizar(b, 0.4)
    return b


def musica_chefe():
    """Tensa, em Mi menor: baixo rápido em colcheias, notas cromáticas e bateria forte. 156 bpm, 8 compassos."""
    bpm = 156
    compassos = 8
    b = vazio(compassos * 4 * 60 / bpm)
    raizes = [40, 40, 41, 40, 40, 40, 43, 42]
    tocar_linha(b, acordes_em_baixo(raizes, [(0, 0.5)] * 8), bpm, "serra", 0.2, legato=0.7)
    tocar_linha(b, acordes_em_baixo(raizes, [(0, 0.5)] * 8), bpm, "triangular", 0.25, legato=0.7)
    melodia = [(64, 1.5), (67, 0.5), (66, 1), (63, 1),
               (64, 1.5), (71, 0.5), (70, 2),
               (65, 1.5), (68, 0.5), (67, 1), (65, 1),
               (64, 3), (None, 1),
               (76, 1), (75, 1), (74, 1), (73, 1),
               (72, 1.5), (71, 0.5), (67, 2),
               (67, 1), (70, 1), (74, 1), (79, 1),
               (78, 2), (75, 2)]
    tocar_linha(b, melodia, bpm, "quadrada", 0.13, largura=0.5, vibrato=0.005)
    bateria(b, "BhcBBhch", bpm, compassos, volume=0.25)
    suavizar(b, 0.45)
    return b


def musica_resultado():
    """Fim de partida, em Dó maior: tranquila e curta. 100 bpm, 8 compassos."""
    bpm = 100
    compassos = 8
    b = vazio(compassos * 4 * 60 / bpm)
    acordes = [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62],
               [60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62, 65]]
    tocar_linha(b, arpejo(acordes, 4, 1), bpm, "triangular", 0.2, oitava=12, legato=0.95)
    melodia = [(72, 1), (76, 1), (79, 2),
               (81, 1), (79, 1), (76, 2),
               (77, 1), (76, 1), (74, 1), (72, 1),
               (74, 3), (None, 1),
               (72, 1), (76, 1), (79, 2),
               (81, 1), (84, 1), (81, 2),
               (79, 1), (77, 1), (76, 1), (74, 1),
               (72, 3), (None, 1)]
    tocar_linha(b, melodia, bpm, "quadrada", 0.12, largura=0.25, vibrato=0.004)
    raizes = [36, 45, 41, 43, 36, 45, 41, 43]
    tocar_linha(b, acordes_em_baixo(raizes, [(0, 2), (7, 1), (12, 1)]), bpm, "triangular", 0.3)
    suavizar(b, 0.35)
    return b


# ---------------------------------------------------------------- salvar tudo

EFEITOS = {
    "ataque.wav": efeito_ataque,
    "acerto.wav": efeito_acerto,
    "inimigo_derrotado.wav": efeito_inimigo_derrotado,
    "chefe_derrotado.wav": efeito_chefe_derrotado,
    "heroi_derrotado.wav": efeito_heroi_derrotado,
    "porta.wav": efeito_porta,
    "menu_mover.wav": efeito_menu_mover,
    "menu_confirmar.wav": efeito_menu_confirmar,
}
MUSICAS = {
    "musica_menu.ogg": musica_menu,
    "musica_torre.ogg": musica_torre,
    "musica_chefe.ogg": musica_chefe,
    "musica_resultado.ogg": musica_resultado,
}


def main():
    os.makedirs(PASTA, exist_ok=True)
    for nome in EFEITOS:
        b = EFEITOS[nome]()
        normalizar(b, 0.8)
        salvar_wav(b, os.path.join(PASTA, nome))
        print("efeito:", nome)
    ffmpeg = shutil.which("ffmpeg")
    for nome in MUSICAS:
        b = MUSICAS[nome]()
        normalizar(b, 0.75)
        wav = os.path.join(PASTA, nome.replace(".ogg", ".wav"))
        salvar_wav(b, wav)
        if ffmpeg is not None:
            subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", wav, "-c:a", "libvorbis",
                            "-q:a", "4", os.path.join(PASTA, nome)], check=True)
            os.remove(wav)
            print("música:", nome)
        else:
            print("música (sem ffmpeg, ficou em .wav):", wav)


main()
