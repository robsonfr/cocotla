import sys
from getopt import getopt as g
from casconv import Cas2Wav, Cas2Bin, blocos_binario, BlocoEOF, BlocoArquivo

def sintaxe():
    print "Sintaxe: cas2wav [-h | --help] [-c | --cas] [-g | --gap] [-f sps,bits,c | --format sps,bits,c] arquivo_entrada [arquivo_saida]"
    print "    -h , --help   : esta mensagem de ajuda"
    print "    -c , --cas    : grava um arquivo .cas ao inves de um .wav"
    print "    -g , --gap    : coloca o gap de 1/2 segundo depois do header do nome do arquivo"
    print "    -f , --format : define o formato do arquivo de saida "
    print "                   (sps = amostras por segundo, bits = bits por amostra e c=canais (1 ou 2)"
    sys.exit()
   
if len(sys.argv) < 2:
    sintaxe()

parametros, extras = g(sys.argv[1:],"hcgf:",["help", "cas", "gap","format"])

if len(extras) < 1:
    sintaxe()

nome_entrada = extras.pop(0)
if len(extras) == 1:
    nome_saida = extras.pop()
else:
    nome_saida = ".".join(nome_entrada.lower().split(".")[:-1] + ["wav"])


gap, sps, bits, chan = False, 44100, 8, 1
    
cas = False    
for p,v in parametros:
    if p == "-h":
        sintaxe()
    if p == "-c" or p == "--cas":
        cas = True
    if p == "-g" or p == "--gap":
        gap = True
    if p == "-f" or p == "--format":
        dados = [k.strip() for k in v.split(",")]
        if len(dados) != 3:
            sintaxe()
        else:
            sps, bits, chan = (int(k) for k in dados)

if nome_entrada.endswith("rom"):
    with open(nome_entrada,"rb") as inp:
        dados = bytearray(inp.read())
    todos_blocos = blocos_binario(nome_entrada.replace(".","-").upper(), dados)            
elif nome_entrada.endswith("bin"):
    with open(nome_entrada,"rb") as inp:
        bin_dados = bytearray(inp.read())    
    tam_bin = int(bin_dados[1]) * 256 + int(bin_dados[2])
    end_inicial = int(bin_dados[3] * 256) + int(bin_dados[4])
    dados = bin_dados[5:tam_bin+5]
    end_exec = int(bin_dados[tam_bin+8] * 256) + int(bin_dados[tam_bin+9])
    todos_blocos = blocos_binario(nome_entrada.replace(".","-").upper(), dados, end_inicial, end_exec)

if not cas:                      
           
    if nome_entrada.endswith("cas"):
        todos_blocos = Cas2Bin(nome_entrada).read_blocos()

    with Cas2Wav(nome_saida, tem_gap = gap, sps = sps, stereo = (chan == 2), bps = bits) as saida:
        saida.write_todos_blocos(todos_blocos)
else:
    if nome_entrada.endswith("cas"):
        print "O arquivo jah eh cas"
        sys.exit()
    else:
        nome_saida = ".".join(nome_entrada.lower().split(".")[:-1] + ["cas"])
        with open(nome_saida, "wb") as saida:
            saida.write(bytearray('U' * 128))
            todos_blocos[0].write(saida)
            saida.write(bytearray('U' * 128))
            for bloco in todos_blocos[1]:
                bloco.write(saida)
            BlocoEOF().write(saida)