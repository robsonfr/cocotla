	org $2800
	
	bra main
	
valores:
	db 0
	
main:
	orcc #$50     ; desabilita interrupcoes
	lda #$ff      
	tfr a,dp
	leay [valores]
	ldx #$400
	
	ldb <$21   
	orb #$8       ; liga o motor
	stb <$21

baite:
	lda #8
	sta valores
loop:
	ldb <$20
	rorb
	bcs loop
	clra
lzero:
	inca 
	ldb <$20	
	rorb
	bcc lzero	
	sta, x
	; ror ,x
	nop
	dec valores
	bne loop
	leax 1,x
	cmpx #$600
	bne baite
	ldx #$400
	bra baite
