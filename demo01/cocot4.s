    org $600
      
    bra inicio   
    ; rotina para ler os dados
c2:
    db 0
c3:
    db 0
inicio: 
    pshs a,b,x,dp
    ; agora vamos desabilitar IRQ e FIRQ...
    orcc #$50
 
    lda #$ff
    tfr a,dp
 
    ; agora vamos ligar o motor...
    lda <$21
    ora #$8
    sta <$21    
    
lp3:
    clr c2
    lda #8
    sta c3
; tem que ler ateh encontrar algo diferente de 55h
btte:
    bsr   lebit
    ror c2
    dec c3
    bne  btte
    cmpb #$55
    beq lp3

    lda #7
    sta c3
btt2:
    bsr   lebit
    ror c2
    dec c3
    bne  btt2
    
    ; x tem o endereco de destino
    ;ldx    #$3000
    ldx #$400
lop1:
    ldb c2
    sta ,x+
    ;cmpx #$486A
    cmpx #$600
    beq fim
    stx $0400
    clr c2
    lda  #8
    sta c3
    ; Le 8 bits para fazer 1 byte
baite:
    bsr   lebit
    ror c2
    dec c3
    bne  baite    
    
    bra lop1
fim:    
    ; no final vamos habilitar IRQ e FIRQ
   andcc #$a7
    ; e desligar o motor
   lda <$21
   anda #$f7
   sta <$21

   puls dp,x,b,a
    ; para fechar, um loop infinito...
lp1: 
    jmp $ac73
    jmp $3000 
    ;bra lp1 
     
    ; le um bit, retorna em cc
    ; destroi a e b
lebit:
    ldb #1
baixo:
    bitb <$20  ; 4
    beq baixo
    
    clra
alto:
    inca
    bitb <$20  ; 4
    bne alto
    cmpa #7
    rts           
    