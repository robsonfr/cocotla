import sys
from getopt import getopt as g
from casconv import Cas2Wav, Cas2Bin

def sintaxe():
    print "Sintaxe: cas2wav [-h | --help] [-g | --gap] [-f sps,bits,c | --format sps,bits,c] arquivo_entrada [arquivo_saida]"
    print "    -h , --help   : esta mensagem de ajuda"
    print "    -g , --gap    : coloca o gap de 1/2 segundo depois do header do nome do arquivo"
    print "    -f , --format : define o formato do arquivo de saida "
    print "                   (sps = amostras por segundo, bits = bits por amostra e c=canais (1 ou 2)"
    sys.exit()
   
if len(sys.argv) < 2:
    sintaxe()

parametros, extras = g(sys.argv[1:],"hgf:",["help", "gap","format"])

if len(extras) < 1:
    sintaxe()

nome_entrada = extras.pop(0)
if len(extras) == 1:
    nome_saida = extras.pop()
else:
    nome_saida = nome_entrada.lower().replace(".cas",".wav")


gap, sps, bits, chan = False, 44100, 8, 1
    
for p,v in parametros:
    if p == "-h":
        sintaxe()
    if p == "-g" or p == "--gap":
        gap = True
    if p == "-f" or p == "--format":
        dados = [k.strip() for k in v.split(",")]
        if len(dados) != 3:
            sintaxe()
        else:
            sps, bits, chan = (int(k) for k in dados)
    

todos_blocos = Cas2Bin(nome_entrada).read_blocos()

with Cas2Wav(nome_saida, tem_gap = gap, sps = sps, stereo = (chan == 2), bps = bits) as saida:
    saida.write_todos_blocos(todos_blocos)

