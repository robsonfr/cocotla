from getopt import getopt as g
from casconv import dados_bin
from struct import pack
import sys

def sintaxe():
    print "Sintaxe: rom2bin [-h | --help] [-s | --start endereco] [-r | --run endereco] arquivo_entrada [arquivo_saida]"
    print "    -h , --help   : esta mensagem de ajuda"
    print "    -s , --start  : endereco de carga (em hexa)"
    print "    -r , --run    : endereco de execucao"
    sys.exit()
   
if len(sys.argv) < 2:
    sintaxe()

parametros, extras = g(sys.argv[1:],"hs:r:",["help", "start", "run"])    
start = 0xC000
run = 0xC000
for p,v in parametros:
    if p == "-h" or p == "--help":
        sintaxe()
    if p == "-s" or p == "--start":
        start = int("0x" + v, 16)
    if p == "-r" or p == "--run":
        run = int("0x" + v, 16)
    
    
nome_entrada = extras.pop(0)
if len(extras) == 1:
    nome_saida = extras.pop()
else:
    nome_saida = ".".join(nome_entrada.lower().split(".")[:-1] + ["bin"])
    
with open(nome_entrada,"rb") as entrada:
    dados = bytearray(entrada.read())

with open(nome_saida,"wb") as saida:
    saida.write(dados_bin(dados, start, run))    