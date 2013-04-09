import sys,math
from io import BytesIO
from itertools import izip_longest, chain
from struct import pack,unpack
from wave import WaveFile, pausa

def ondas(zero_one = 0, cocotla = False, bit_length = 8, samples_per_second = 44100, channels = 2):
    bits = { 8 : (127,127,"B",1), 16 : (0,32767,"<h",1) }    
    if not bit_length in bits.keys():
        bit_length = 8
    mid_value, factor, fmt, sgn = bits[bit_length]        

    if cocotla:
        num_of_samples = (10, 6)
        sgn = -1        
        if bit_length == 16:
            mid_value = bits[bit_length][1]
            fmt = "<H"
    else:
        num_of_samples = (samples_per_second / 1090, samples_per_second / 2000)
    nos = num_of_samples[zero_one & 1]
    for k in range(nos):
        for baite in bytearray(pack(fmt, int(mid_value + sgn * factor * math.sin(float(k) / float(nos) * math.pi * 2.0))) * channels):
        #for baite in bytearray(pack(fmt, int(mid_value + sgn * factor * math.sqrt(1-math.pow(math.cos(float(k) / float(nos) * math.pi * 2.0),2.0)))) * channels):
            yield baite    

onda = [int(127.0 + 127.0 * math.sin(float(k) / 22.0 * math.pi)) for k in range(44)]
onda_2 = [int(127.0 + 127.0 * math.sin(float(k) / 12.0 * math.pi)) for k in range(24)]

onda_3 = [int(127.0 - 127.0 * math.sin(float(k) / 5.0 * math.pi)) for k in range(10)]
onda_4 = [int(127.0 - 127.0 * math.sin(float(k) / 3.0 * math.pi)) for k in range(6)]

#onda_3 = [int(127.0 - 127.0 * math.sin(float(k) / 3.0 * math.pi)) for k in range(6)]
#onda_4 = [int(127.0 - 127.0 * math.sin(float(k) / 2.0 * math.pi)) for k in range(4)]


#onda_3 = [0,255,0,255,0,255,0,255,0];
#onda_4 = [0,0,0,0,0,255,0,255,0];

onda_bytes = (bytearray(chain.from_iterable([pack("B",n) * 2 for n in onda])),
              bytearray(chain.from_iterable([pack("B",n) * 2 for n in onda_2])))
    
onda_x = (bytearray(chain.from_iterable([pack("B",n) * 2 for n in onda_3])),
              bytearray(chain.from_iterable([pack("B",n) * 2 for n in onda_4])))

onda_tipos = {True : onda_x, False : onda_bytes}              
              
NOME_ARQUIVO = 0
DADOS = 1
EOF = 15           
            
class Bloco(object):
    def __init__(self, tipo, dados, pausa=False):
        self.__tipo = tipo
        self.__tamanho = len(dados)
        self.__dados = dados
        self.__pausa = pausa
   
   
    @property
    def pausa(self):
        return self.__pausa
   
    @property
    def data(self):
        soma = self.__tipo + self.__tamanho
        for d in self.__dados:
            if d != None: soma += d
        soma = soma % 256
        return bytearray([0x55,0x3C,self.__tipo,self.__tamanho]) + bytearray(self.__dados) + bytearray([soma,0x55])
   
    def write(self, out):
        out.write(self.data)   
        return False
        
    def __str__(self):
        return "%02X %d %s" % (self.__tipo, self.__tamanho, str(self.__pausa))
            
class BlocoArquivo(Bloco):
#   def __init__(self, tipo, nome, ascii = False, staddr = 0x1F0B, ldaddr = 0x1F0B):
    def __init__(self, tipo, nome, ascii = False, staddr = 0x1600, ldaddr = 0x1600):
        Bloco.__init__(self, 0, bytearray(nome.upper()[:8] + " " * (max(0, 8-len(nome)))) + bytearray([tipo, {False: 0, True: 0xFF}[ascii], 0]) + bytearray(pack(">H",staddr)) + bytearray(pack(">H",ldaddr))) 
        self.__pausa = True
        
    def write(self,out):
        Bloco.write(self,out)
        return True
        
class BlocoEOF(Bloco):
    def __init__(self):
        Bloco.__init__(self, 0xFF, []) 

def novo_bloco_arquivo(data):
    nome = str(data[0:8]).strip()
    subtipo = data[8]
    ascii = data[9] != 0
    gap = data[10] != 0
    end_inicial = data[11] * 256 + data[12]
    end_exec = data[13] * 256 + data[14]
    return BlocoArquivo(subtipo, nome, ascii, end_inicial, end_exec)
        
def cas_to_wav(arq, modo="wb"):
    return Cas2Wav(arq)

def cas_to_wavmem(arq, modo="wb"):
    return Cas2WavStream()

def dados_bin(dados, st=0xC000, rn=0xC000, exc = True):
    ret = bytearray([0] + list(pack(">HH", len(dados), st)) + list(dados))
    if exc:
        ret = ret + bytearray([255] + list(pack(">HH", 0, rn)))
    return ret
    
class Cas2Bin(object):
    def __init__(self, filename="input.cas"):
        self.__filename = filename
    
    @staticmethod    
    def _read_single_block(inp, header = False):
        if header:             
            inp.read(127)
        i = inp.read(1)
        while i == 'U': i = inp.read(1)
        assinatura_bloco = i
        if assinatura_bloco != '\x3c':
            raise Exception("Invalid format " + assinatura_bloco)

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

    def read_blocos(self, stream = None):
        blocos_dados = []
        if stream:
            b = stream
        else:
            b = open(self.__filename, "rb")
        with b as e:
            tipo, data = Cas2Bin._read_single_block(e, True)
            if tipo != NOME_ARQUIVO:
                raise Exception("Invalid format")
            else:
                arquivo = novo_bloco_arquivo(data)
                                                    
                tipo, dt = Cas2Bin._read_single_block(e,False)
                while tipo == DADOS:
                    blocos_dados.append(Bloco(DADOS,dt))
                    tipo, dt = Cas2Bin._read_single_block(e,False)
                
                return (arquivo, blocos_dados)
                
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
                return (nome, end_inicial, end_exec, dados, gap)
  
    
class Cas2Wav(WaveFile):
    def __init__(self, filename=None, tem_gap=True, sps=44100, stereo=False, bps=8):
        WaveFile.__init__(self, filename, tem_gap, sps, stereo, bps)

        self.__onda_tipos = {}
        for i in (False,):
            self.__onda_tipos[i] = (bytearray(ondas(0, i, bps, sps, 1 + stereo)),bytearray(ondas(1, i, bps, sps, 1 + stereo)))
        self.__onda_tipos[True] = onda_x
              
    def write(self, data, velocidade=False):
        oo = self.__onda_tipos[velocidade]
        for b in bytearray(data):
            baite = b
            for _ in range(8):
                bloco = oo[baite & 0x01]
                self.llwrite(bloco)
                baite >>= 1

    def write_leader(self):
        leader = bytearray(['U'] * 128)
        self.write(leader,False)        
                
    def write_bloco(self, bloco):
        self.write(bloco.data, False)
        if bloco.pausa:
            self.pausa()                  
    
    def write_todos_blocos(self, todos_blocos):
        self.write_leader()
        self.write_bloco(todos_blocos[0])
        if self._gap: 
            self.pausa()
        self.write_leader()
        for bloco in todos_blocos[1]:
            self.write_bloco(bloco)
        self.write_bloco(BlocoEOF())

            
class Cas2WavStream(Cas2Wav):
    def __init__(self, tem_gap=True, sps=44100, stereo=False, bps=8, stream = None):
        Cas2Wav.__init__(self, None, tem_gap, sps, stereo, bps)        
        if stream != None:
            self._file = stream
        else:
            from io import BytesIO
            self._file = BytesIO()
        #Cas2Wav.set_file(self, self.__file)       
        

def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)        
   
def cocotla_loader(output_fn, target, dados, app, ajuste=6, staddr = 0x3000, rnaddr = 0x3000, off_st = 0x05, off_eof = 0x07, off_rn = 0x09, off_aj = 0x02):
    dados[off_aj] = ajuste
    dados[off_st:off_st+2] = bytearray(pack(">H", staddr))
    
    dados[off_rn:off_rn+2] = bytearray(pack(">H", rnaddr))
        
    final_addr = staddr + len(app)
    
    dados[off_eof:off_eof+2] = bytearray(pack(">H", final_addr))
    
    leader = bytearray("U" * 128)
    l2 = bytearray(range(256)*2)
    q = len(dados) // 255 + 1
    u  = len(dados) % 255

    nome, ext = target.split(".")
    with output_fn(target) as s:
        
        s.write_leader()
        BlocoArquivo(2, "CO" + nome.upper()[0:6],ascii = False, staddr = 0x600, ldaddr = 0x600).write(s)
        s.pausa()
        s.write_leader()
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
        s.write(bytearray([app[-1],0,0,0,0,0,0,0,0,0]), True)
        
def cocotla(target, fn_loader, app, ajuste=6, staddr = 0x600, rnaddr = 0x600, off_st = 0x05, off_eof = 0x07, off_rn = 0x09, off_aj = 0x02):    
#def cocotla(target, fn_loader, app, ajuste=6, staddr = 0x3000, rnaddr = 0x3000, off_st = 0x39, off_eof = 0x41, off_rn = 0x6a, off_aj = 0x76):    
    with open(fn_loader, "rb") as arq:
        dados = bytearray(arq.read())
    cocotla_loader(cas_to_wav, target, dados, app, ajuste, staddr, rnaddr, off_st, off_eof, off_rn, off_aj)

def blocos_binario(nome, dados, st_addr = 0x1600, rn_addr = 0x1600):
    dd = []
    buffer = []
    for b in dados:
        l = len(buffer)
        if l > 0 and len(buffer) % 255 == 0:
            dd.append(Bloco(DADOS, buffer))
            buffer = []
        buffer.append(b)
    if l > 0 == 0:
        dd.append(Bloco(DADOS, buffer))
    return (BlocoArquivo(2, nome, False, st_addr, rn_addr), dd)
    
if __name__ == "__main__":
    entrada = sys.argv[1]
    with open(entrada,"rb") as e:
        dados = bytearray(e.read())
    nome_saida = entrada.replace(".rom", ".cas")
    bl = blocos_binario(entrada.replace(".","-").upper(),  dados)
    with open(nome_saida,"wb") as saida:
        saida.write(bytearray('U' * 128))
        bl[0].write(saida)
        saida.write(bytearray('U' * 128))
        for bloco in bl[1]:
            bloco.write(saida)            
        BlocoEOF().write(saida)