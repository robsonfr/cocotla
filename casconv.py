import sys,math
from itertools import izip_longest, chain
from struct import pack

onda = [int(127.0 * math.sin(float(k) / 20.0 * math.pi)) for k in range(40)]
onda_2 = [int(127.0 * math.sin(float(k) / 11.0 * math.pi)) for k in range(22)]

onda_3 = [int(127.0 * math.sin(float(k) / 10.0 * math.pi)) for k in range(20)]
onda_4 = [int(127.0 * math.sin(float(k) / 5.5 * math.pi)) for k in range(11)]

#onda_3 = [3,253]
#onda_4 = [253,3]

#onda_3 = [int(32000.0 * math.sin(float(k) / 4.0 * math.pi)) for k in range(8)]
#onda_4 = [int(32000.0 * math.sin(float(k) / 2.0 * math.pi)) for k in range(4)]
onda_bytes = (bytearray(chain.from_iterable([pack("b",n) for n in onda])),
              bytearray(chain.from_iterable([pack("b",n) for n in onda_2])))
    
onda_x = (bytearray(chain.from_iterable([pack("b",n)  for n in onda_3])),
              bytearray(chain.from_iterable([pack("b",n) for n in onda_4])))

onda_tipos = {True : onda_x, False : onda_bytes}              
              
def cas_to_wav(arq, modo="wb"):
    return Cas2Wav(arq)
    
class Cas2Wav(object):
    def __init__(self, filename="cassette.wav"):
        self.__file = open(filename,"wb")
                
    def __enter__(self):
        # Header
        self.__file.write(bytearray("RIFF") + bytearray([0]*4) + bytearray("WAVE"))
        # 16,0,0,0: tamanho (PCM), 1,0 : formato (PCM), 1,0 : canais, 0x44,0xAC,0,0: taxa de amostragem (44100)
        # 0x44,0xAC,0x00,0 : byte rate (taxa * num canais * bits por amostra / 8)
        # 1,0 : alinhamento de bloco (num canais * bits por amostra  / 8)
        # 8,0 : bits por amostra
        self.__file.write(bytearray("fmt ") + bytearray([16,0,0,0,1,0,1,0, 0x44,0xAC,0,0,0x44,0xAC,0,0,1,0,8,0]))
        self.__file.write(bytearray("data") + bytearray([0]*4))
        self.__sc2s = 0
        return self
        
        
    def write(self, data, velocidade=False):
        oo = onda_tipos[velocidade]
        for b in bytearray(data):
            baite = b
            for _ in range(8):
                bloco = oo[baite & 0x01]
#                bloco = onda_bytes[baite & 1]
                self.__sc2s += len(bloco)
                self.__file.write(bloco)
                baite >>= 1
    
    def llwrite(self, data):
        self.__sc2s += len(data)
        self.__file.write(data)
    
    def __exit__(self,type,val,tb):
        try:
            self.__file.seek(4)
            self.__file.write(bytearray(pack("I",self.__sc2s + 36)))
            self.__file.seek(40)
            self.__file.write(bytearray(pack("I",self.__sc2s)))
        finally:
            self.__file.close()

class Bloco(object):
    def __init__(self, tipo, dados):
        self.__tipo = tipo
        self.__tamanho = len(dados)
        self.__dados = dados
        
    def write(self, out):
        soma = self.__tipo + self.__tamanho
        for d in self.__dados:
            if d != None: soma += d
        soma = soma % 256
        out.write(bytearray([0x55,0x3C,self.__tipo,self.__tamanho]) + bytearray(self.__dados) + bytearray([soma,0x55]))
        

class BlocoArquivo(Bloco):
#   def __init__(self, tipo, nome, ascii = False, staddr = 0x1F0B, ldaddr = 0x1F0B):
    def __init__(self, tipo, nome, ascii = False, staddr = 0x3000, ldaddr = 0x3000):
        Bloco.__init__(self, 0, bytearray(nome.upper()[:8] + " " * (max(0, 8-len(nome)))) + bytearray([tipo, {False: 0, True: 0xFF}[ascii], 0]) + bytearray(pack(">H",staddr)) + bytearray(pack(">H",ldaddr))) 

class BlocoEOF(Bloco):
    def __init__(self):
        Bloco.__init__(self, 0xFF, []) 


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)        

    
adiciona_teste = False
if sys.argv[1] == "-w":
    nome = sys.argv[2]
    fn = cas_to_wav
    saida = nome.replace(".rom",".wav")
    adiciona_teste = True
else:
    nome = sys.argv[1]
    fn = open
    saida = nome.replace(".rom",".cas")      
    
nf = nome.replace(".rom","")
print nome
with open(nome,"rb") as arq:
    dados = bytearray(arq.read())
print len(dados)    
leader = bytearray("U" * 128)
l2 = bytearray(range(256)*2)
q = len(dados) // 255
u  = len(dados) % 255
print q,u
with fn(saida,"wb") as s:    
    s.write(leader)
    BlocoArquivo(2,nf).write(s)
    s.write(leader)
    if len(dados) < 255:
        Bloco(1,dados).write(s)
    else:
        a = 0
        for b in grouper(255, dados):        
            a = a + 1
            if a == q: b = b[:u]
            Bloco(1, b).write(s)
            if a == q: break
    BlocoEOF().write(s)
    if adiciona_teste:
        #s.llwrite(bytearray([0x01,0x80] * 882))
        #s.write(leader, True)
        #for _ in range(16):
        s.write(bytearray([n for n in range(256)]*2), True)
        s.write(bytearray([55]), True)
    
