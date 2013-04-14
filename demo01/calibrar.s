	org $2800
	
	bra main
	
inicio:
	dw $3000

execz:
	dw $3000
	
valores:
	db 0
	
soma:
	dw $6ACE
	
teste:
	db 6
		
termino:
	dw $486A

autocal:	
	db 0
	db 0
	db 0
	db 0
	db 0
	db 0
	db 0
	db 0
	db 0
	db 0
	db 0
	db 0
	db 0
	db 0
	db 0
	db 0
	
	
mensagem:
	db "ERRO"
	db 00

header:
	db 00

	
main:
	orcc #$50     ; desabilita interrupcoes
	lda #$ff      
	tfr a,dp
	leay [valores]

tec:
	jsr [$a000]
	beq tec

	
	ldb <$21   
	orb #$8       ; liga o motor
	stb <$21

	;bsr calbaite	

hd:	
	leax [header]
	bsr lebaite
	lda #$55
	cmpa -1,x
	beq hd	
	
	ldx inicio
lx:	
	bsr lebaite
	cmpx termino
	bne lx

	ldb <$21   
	andb #$f7       ; desliga o motor
	stb <$21

	
	ldx #0
	
	ldy inicio
st:	
	ldb ,y+
	abx
	cmpy termino
	bne st
	
	cmpx soma
	bne erro
	
	ldx execz
	tfr x,pc

erro:
	ldx #$400
	leay [mensagem]
lerr:	
	lda, y+
	tsta
fim:	
	beq fim
	sta, x+
	bra lerr
	
	
lebaite:
	lda #8
	sta valores
loop1:
	ldb <$20
	rorb
	bcs loop1
	clra
lzero1:
	inca 
	ldb <$20	
	rorb
	bcc lzero1
;	cmpa #18
;	bhi loop1
;	tsta
;	beq loop1
	cmpa teste
	ror ,x
	stx $400
	dec valores
	bne loop1
	leax 1,x
	rts


calbaite:
	leax [autocal]
	lda #16
	sta valores
calloop:
	ldb <$20
	rorb
	bcs calloop
	clra
callzero:
  	inca 
	ldb <$20	
	rorb
	bcc callzero
	cmpa #18
	bhs calloop
	sta, x+
	dec valores
	bne calloop
	ldd #0		
	leax [autocal]
max:
	cmpb a,x
	bhi prox
	ldb a,x
prox:
	inca
	cmpa #16
	bne max
	decb
	stb teste
	rts	
	
	