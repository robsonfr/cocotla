from casconv import Cas2Bin, dados_bin
import sys

if len(sys.argv) == 1:
    print "Sintaxe: cas2bin arquivo_entrada [arquivo_saida]"
    sys.exit()   
    
nome_entrada = sys.argv[1]
if len(sys.argv) == 3:
    nome_saida = sys.argv[2]
else:
    nome_saida = ".".join(nome_entrada.lower().split(".")[:-1] + ["bin"])
    
nome, end_inicial, end_exec, dados, gap = Cas2Bin(nome_entrada).read()
    
with open(nome_saida, "wb") as out:
    out.write(dados_bin(dados, end_inicial, end_exec))