import sys,math
from itertools import izip_longest, chain
from struct import pack,unpack

onda = [int(127.0 + 127.0 * math.sin(float(k) / 22.0 * math.pi)) for k in range(44)]
onda_2 = [int(127.0 + 127.0 * math.sin(float(k) / 12.0 * math.pi)) for k in range(24)]

onda_3 = [int(127.0 + 127.0 * math.sin(float(k) / 5.0 * math.pi)) for k in range(10)]
onda_4 = [int(127.0 + 127.0 * math.sin(float(k) / 3.0 * math.pi)) for k in range(6)]

onda_bytes = (bytearray(chain.from_iterable([pack("B",n) * 2 for n in onda])),
              bytearray(chain.from_iterable([pack("B",n) * 2 for n in onda_2])))
    
onda_x = (bytearray(chain.from_iterable([pack("B",n) * 2 for n in onda_3])),
              bytearray(chain.from_iterable([pack("B",n) * 2 for n in onda_4])))

onda_tipos = {True : onda_x, False : onda_bytes}              
              
NOME_ARQUIVO = 0
DADOS = 1
EOF = 15
              
def cas_to_wav(arq, modo="wb"):
    return Cas2Wav(arq)

class Cas2Bin(object):
    def __init__(self, filename="input.cas"):
        self.__filename = filename
    
    @staticmethod    
    def _read_single_block(inp, header = False):
        if header: 
            inp.read(128)
            
        assinatura_bloco = inp.read(2)
        if assinatura_bloco != '\x55\x3c':
            raise Exception("Invalid format")

        tipo,tamanho = unpack("BB", inp.read(2))
        if tamanho > 0:
            dados = bytearray(inp.read(tamanho))
        else:
            dados = []        
        soma = unpack("B",inp.read(1))[0]
        inp.read(1)

        if header:
            inp.read(128)
        
        if soma != (tipo + tamanho + sum(dados)) % 256:
            raise Exception("Invalid checksum: %d %d", (soma, (tipo + tamanho + sum(dados)) % 256))
        else:
            return (tipo, dados)
            
        
    def read(self):
        with open(self.__filename, "rb") as e:
            tipo, data = Cas2Bin._read_single_block(e, True)
            if tipo != NOME_ARQUIVO:
                raise Exception("Invalid format")
            else:
                nome = str(data[0:8]).strip()
                subtipo = data[8]
                binario = data[9] == 0
                gap = data[10] != 0
                end_inicial = data[11] * 256 + data[12]
                end_exec = data[13] * 256 + data[14]
                
                dados = []
                tipo, dt = Cas2Bin._read_single_block(e,False)
                while tipo == DADOS:
                    dados += dt
                    tipo, dt = Cas2Bin._read_single_block(e,False)
                return (nome, end_inicial, end_exec, dados)
    
class Cas2Wav(object):
    def __init__(self, filename="cassette.wav"):
        self.__file = open(filename,"wb")
                
    def __enter__(self):
        # Header
        self.__file.write(bytearray("RIFF") + bytearray([0]*4) + bytearray("WAVE"))
        # 16,0,0,0: tamanho (PCM), 1,0 : formato (PCM), 2,0 : canais, 0x44,0xAC,0,0: taxa de amostragem (44100)
        # 0x10,0xB1,0x02,0 : byte rate (taxa * num canais * bits por amostra / 8)
        # 4,0 : alinhamento de bloco (num canais * bits por amostra  / 8)
        # 8,0 : bits por amostra
        self.__file.write(bytearray("fmt ") + bytearray([16,0,0,0,1,0,2,0, 0x80,0xBB,0,0,0x00,0x77,0x01,0x00,2,0,8,0]))
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
    def __init__(self, tipo, nome, ascii = False, staddr = 0x600, ldaddr = 0x600):
        Bloco.__init__(self, 0, bytearray(nome.upper()[:8] + " " * (max(0, 8-len(nome)))) + bytearray([tipo, {False: 0, True: 0xFF}[ascii], 0]) + bytearray(pack(">H",staddr)) + bytearray(pack(">H",ldaddr))) 

class BlocoEOF(Bloco):
    def __init__(self):
        Bloco.__init__(self, 0xFF, []) 


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)        

def cocotla(target, fn_loader, app, staddr = 0x3000, rnaddr = 0x3000, off_st = 0x2e, off_eof = 0x33, off_rn = 0x55):
    with open(fn_loader, "rb") as arq:
        dados = bytearray(arq.read())
    dados[off_st:off_st+2] = bytearray(pack(">H", staddr))
    
    dados[off_rn:off_rn+2] = bytearray(pack(">H", rnaddr))
        
    final_addr = staddr + len(app) - 1
    
    dados[off_eof:off_eof+2] = bytearray(pack(">H", final_addr))
    
    leader = bytearray("U" * 128)
    l2 = bytearray(range(256)*2)
    q = len(dados) // 255
    u  = len(dados) % 255

    nome, ext = target.split(".")
    with cas_to_wav(target) as s:
        
        s.write(leader)
        BlocoArquivo(2, "CO" + nome.upper()[0:6]).write(s)
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
        s.write(app, True)
        s.write(bytearray([0,0,0]), True)
        
    
    
if __name__ == "__main__":
    adiciona_teste = False
    if sys.argv[1] == "-w":
        nome = sys.argv[2]
        fn = cas_to_wav
        saida = nome.replace(".rom",".wav")
        adiciona_teste = True
        outro_arq = sys.argv[3]
    else:
        nome = sys.argv[1]
        fn = open
        saida = nome.replace(".rom",".cas")      
        
    nf = nome.replace(".rom","")
    with open(nome,"rb") as arq:
        dados = bytearray(arq.read())  
    leader = bytearray("U" * 128)
    l2 = bytearray(range(256)*2)
    q = len(dados) // 255
    u  = len(dados) % 255
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
            with open(outro_arq, "rb") as oa:
                df = bytearray(oa.read())
            #s.write(bytearray([n for n in range(256)]*2), True)
            #s.write(bytearray([0] * 512), True)
            s.write(df, True)
            s.write(bytearray([0,0,0]), True)
        
