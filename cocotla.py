from casconv import cocotla, Cas2Bin
from struct import unpack
from sys import argv

if __name__ == "__main__":
    entrada = argv[1].lower()
    if len(argv) > 2:
        valor = int(argv[2])
    else:
        valor = 6
    if entrada.endswith("rom"):
        nome = entrada.split(".")[0].upper()
        inicial = 0x3000
        exc = 0x3000
        with open(argv[1],"rb") as x:
            dados = bytearray(x.read())        
    elif entrada.endswith("cas"):
        cas = Cas2Bin(argv[1])
        nome, inicial, exc, dados, gap = cas.read()
        with open("binario.bin", "wb") as fff:
            fff.write(bytearray(dados))
    elif entrada.endswith("bin") or entrada.endswith("pak"):
        nome = entrada.split(".")[0].upper()
        with open(argv[1],"rb") as y:
            tamanho = unpack("<H", y.read(2))[0]
            inicial = unpack("<H", y.read(2))[0]
            exc = inicial
            dados = bytearray(y.read(tamanho))
    cocotla(nome + ".wav", "cocotla.rom", dados, valor, inicial, exc)
    #cocotla(nome + ".wav", "cocot4.rom", dados, valor, inicial, exc)
    