from wave import WaveFile


ondas = { 0 : [ 255,0], 1 : [255,0,0,0] }
onda_min = [[255,0,255,0],[255,0,0,0]]

with WaveFile("teste2.wav") as a:
    a.llwrite(bytearray(ondas[0] * 441000))
    a.pausa()
    a.llwrite(bytearray(ondas[1] * 294000))
    a.pausa()
    a.llwrite(bytearray((ondas[0] + ondas[1]) * 176400))
    a.pausa()
    a.llwrite(bytearray((ondas[1] + ondas[0]) * 176400))
