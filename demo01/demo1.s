
	org $3000
	
	; entra em modo grafico
	
	lda #$e0
	sta $ff22
	sta $ffc3
	sta $ffc5
	
	; coloca o endereco inicial da "VRAM" em 0x600, padrao do basic
	sta $ffc7
	sta $ffc9
	sta $ffca
	sta $ffcc
	sta $ffce
	sta $ffd0
	sta $ffd2
	
	; copia conteudo de pict para a vram (vejam como eh simples)	
    
	leax  [pict]	
	ldy #$600
l1: ldd, x++
	std, y++
	cmpy #$1e00
    bne l1	
    
scroll:	
	; scroll de 2 em 2 linhas
	ldx  #3648
	leau [pict]
	ldy  #992
l2: ldd, x++
	std, u++
	leay -1,y
	bne l2
	
	leau [pict]
	leau 1984,u

    ldx #3584
l3: ldd, x++
	std, u++
	cmpx #3648
	bne l3
	
	leax [pict]
	ldu #3584
	ldy #1024
l4: ldd, x++
	std, u++
	leay -1,y
	bne l4

	jmp scroll

pict:
    # include "demo01.raw"