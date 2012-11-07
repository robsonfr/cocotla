from casconv import cocotla, Cas2Bin
from sys import argv

if __name__ == "__main__":
    entrada = argv[1].lower()
    if entrada.endswith("rom"):
        nome = entrada.split(".")[0].upper()
        inicial = 0x3000
        exc = 0x3000
        with open(argv[1],"rb") as x:
            dados = bytearray(x.read())        
    elif entrada.endswith("cas"):
        cas = Cas2Bin(argv[1])
        nome, inicial, exc, dados = cas.read()
    cocotla("cocotla_" + nome + ".wav", "cocotla.rom", dados, inicial, exc)
    
    