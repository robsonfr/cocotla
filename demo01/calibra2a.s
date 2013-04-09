	org $2800
	
	bra main
	
tabela:
	db "pqrstuvwxyABCDEFX"

valores:
	db 0
	db 0
ax:
	db 0
ant:
	db 1

escr:
	sta ax
	lsra
	lsra
	lsra
	lsra
	lda a,u
	sta ,x
	lda ax
	anda #15
	lda a,u
	sta 1,x
	rts
	
main:
	orcc #$50
	lda #$ff
	tfr a,dp
	leay [valores]
	leau [tabela]
	ldx #$444
	lda ,u
	sta, x
	sta 1,x
	sta 2,x
	sta 5,x
	sta 6,x
	
	lda 1,u
	sta 4,x
		
	leax 1,x	
	
	ldb <$21
	orb #$8
	stb <$21
	
loop:
	clr $440
	ldb <$20
	andb #1
	stb $440
	rorb	
	bcs loop
lzero:
	ldb <$20
	andb #1	
	stb $440
	inc ,y
	rorb
	bcc lzero
lum:	
	ldb <$20
	andb #1
	stb $440	
	inc 1,y
	rorb
	bcs lum
	
	lda ,y
	bsr escr
	lda 1,y
	leax 4,x
	bsr escr
	leax -4,x
	
	clr ,y
	clr 1,y
	bra loop
	