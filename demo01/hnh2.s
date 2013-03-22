    org $1600
      
    bra inicio   
    
ant:
    db 2

contador:
	db 0
	
tabela:
	db "pqrstuvwxyABCDEFX"
	
mensagem:
	db "PRESS`ANY`KEY",0

print:
	ldb, y+
	bne escreve
	rts
escreve:	
	stb, x+
	bra print
	
	
inicio: 
	pshs a,b,x,y,dp
	
	ldx #$400
	leay [mensagem]
	bsr print
tecl:	
	jsr [$a000]
	beq tecl	
	
	ldx #$400
	
    ; agora vamos desabilitar IRQ e FIRQ...
    orcc #$50
	
	
	leay [tabela]
	lda #$ff
	tfr a,dp

	; e vamos dobrar a velocidade...
	sta <$d7

	
    ; agora vamos ligar o motor...
    lda <$21
    ora #$8
    sta <$21
    
    ; a ideia eh ler os tempos de altos e baixos e escreve-los na tela...
	; b guarda o contador
ciclo:
    jsr [$a000]
    bne sair
	clr contador
	inc contador
prox:		
	lda <$20
	anda #1
	cmpa ant
	bne exibir
	inc contador	
	bne prox
	
	; estouro...	
;	ldb a,y
;	stb, x+
	ldb 16,y	
	stb, x+
    ldb #$60
    stb, x+
;	stb, x+
	bra fiml
	
exibir:
	ldb ant
	sta ant
	
	cmpb #2
	beq ciclo
	tfr b,a
;	bsr nibble
	
;	lda contador
;	lsra
;	lsra
;	lsra
;	lsra
;	bsr nibble
	
	lda contador
	bsr nibble
    lda #$60
    sta, x+
	bra fiml
	
nibble:	
	anda #15
	lda a,y
	sta, x+
	rts
	
fiml:
;	ldb #$60
;	stb, x+
	cmpx #$600
	blo ciclo
	ldx #$400
    bra ciclo

sair:
    lda <$21
    anda #$F7
    sta <$21
	
; restaurar a velocidade...
	sta <$d6
	
	andcc #$AF
tecl2:	
;	jsr [$a000]
;	beq tecl2

	puls dp,y,x,b,a
    jmp $ac73
	
	