import math
import os
import struct
import wave
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QSoundEffect

RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_SONS = os.path.join(RAIZ_PROJETO, "Sons")
CAMINHO_SOM = os.path.join(PASTA_SONS, "som_urna.wav")


def _gerar_som_se_nao_existir():
    "Gera automaticamente o áudio da urna se a pasta Sons não existir."
    if os.path.exists(CAMINHO_SOM):
        return

    os.makedirs(PASTA_SONS, exist_ok=True)
    taxa_amostragem = 44100

    notas = [
        (523.25, 0.12),  # Dó
        (659.25, 0.12),  # Mi
        (783.99, 0.25),  # Sol
    ]

    frames = []
    for freq, duracao in notas:
        num_amostras = int(taxa_amostragem * duracao)
        for i in range(num_amostras):
            t = i / taxa_amostragem
            valor = int(32767 * 0.4 * math.sin(2 * math.pi * freq * t))
            frames.append(struct.pack("<h", valor))

    with wave.open(CAMINHO_SOM, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(taxa_amostragem)
        wav.writeframes(b"".join(frames))


class GerenciadorSom:
    def __init__(self):
        _gerar_som_se_nao_existir()
        self.efeito = QSoundEffect()
        self.efeito.setSource(QUrl.fromLocalFile(CAMINHO_SOM))
        self.efeito.setVolume(1.0)

    def tocar(self):
        self.efeito.play()


_tocador = None


def tocar_som_confirmacao():
    global _tocador
    if _tocador is None:
        _tocador = GerenciadorSom()
    _tocador.tocar()
