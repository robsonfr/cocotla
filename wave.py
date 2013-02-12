from struct import pack

def pausa(bit_length = 8, samples_per_second = 44100, channels = 1):
    bits = { 8 : (127,"B"), 16 : (0,"<H") }
    num_of_samples = samples_per_second / 2
    if bit_length in bits.keys():
        mid_value, fmt = bits[bit_length]        
    else:
        mid_value, fmt = bits[8]
    for baite in bytearray(pack(fmt, int(mid_value)) * channels * num_of_samples):
        yield baite


class WaveFile(object):
    def __init__(self, filename=None, tem_gap=True, sps=44100, stereo=False, bps=8):
        if filename:
            self._file = open(filename,"wb")
        self._gap = tem_gap
        self._samples_per_second = sps
        self._stereo = stereo
        self._bits_per_sample = bps

        self._pausa = bytearray(pausa(bps,sps,1+stereo))
    
    #def set_file(self, file):
    #   self._file = file

    @property         
    def stream(self):
        return self._file
        
    
    def __enter__(self):
        # Header
        self._file.write(bytearray("RIFF") + bytearray([0]*4) + bytearray("WAVE"))
        # 16,0,0,0: tamanho (PCM), 1,0 : formato (PCM), 2,0 : canais, 0x80,0xBB,0,0: taxa de amostragem (48000)
        # 0x00,0x77,0x01,0 : byte rate (taxa * num canais * bits por amostra / 8)
        # 2,0 : alinhamento de bloco (num canais * bits por amostra  / 8)
        # 8,0 : bits por amostra
        canais = 1 + self._stereo
        taxa = self._samples_per_second
        b = self._bits_per_sample
        align_block = canais * b / 8
        byte_rate = taxa * align_block
        
        self._file.write(bytearray("fmt "))
        self._file.write(bytearray([16,0,0,0,1,0]))
        self._file.write(bytearray(pack("<HIIHH",canais,taxa,byte_rate,align_block,b)))
        self._file.write(bytearray("data") + bytearray([0]*4))
        self._sc2s = 0
        return self    
        
        
    def llwrite(self, data):
        self._sc2s += len(data)
        self._file.write(data)           
        
    def pausa(self):
        self.llwrite(self._pausa)

    def update(self):
        self._file.seek(4)
        self._file.write(bytearray(pack("I",self._sc2s + 36)))
        self._file.seek(40)
        self._file.write(bytearray(pack("I",self._sc2s)))

    def __exit__(self,type,val,tb):
        try:
            self.update()
        finally:
            self._file.close()		