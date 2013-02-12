from wave import WaveFile


ondas = { 0 : [ 255,0,255], 1 : [255,0,0,0,0,0,255] }

with WaveFile("um_zero.wav") as a:
    a.llwrite(bytearray((ondas[1] + ondas[0]) * 4410))
