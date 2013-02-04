
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

    pshs a,b,x,y,u
    ldx #$600
    leay [pict]
    
    bsr uncompress
    puls y,u,x,b,a
        
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

uncompress:    
    ; y aponta para os dados compactados
    ; a, b, u e x sao destruidos
    ldd, y++
    leau d,x
    pshs u
    lda, y+
    pshs a
prox:    
    lda, y+
    cmpa, s
    beq dc
sto:    
    sta ,x+
    cmpx 1,s
    blo prox
    bra fim    
    
dc:
    lda ,y+
    bne dx
    lda, s
    bra sto
dx:    
    ldb, y+
    leau a,x
lp1:
    lda, u+
    sta, x+
    decb
    bne lp1
    cmpx 1,s
    blo prox    
fim:
    puls u
    puls a
    rts

    
pict:
    # include "demo01.raw"