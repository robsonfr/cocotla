	org $2800
	
	bra main
	
inicio:
	
	
valores:
	db 0

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
	
soma:
	dw 0
	
teste:
	db 6
	
termino:
	dw $600
	
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

	
	bsr calbaite
	lda teste
	sta $400

	ldx #$401
lx:	
	bsr lebaite
	cmpx termino
	bne lx
	ldx #$401
	bra lx
	
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
	cmpa teste
	ror ,x
	dec valores
	bne loop1
	leax 1,x
	rts
	