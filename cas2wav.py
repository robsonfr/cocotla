import sys
from casconv import Cas2Wav

with open(sys.argv[1], "rb") as entrada:
    dados = bytearray(entrada.read())

with Cas2Wav("saida.wav") as saida:
    saida.write(dados)

