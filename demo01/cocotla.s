    org $600
      
    bra inicio   
    ; rotina para ler os dados
c1:
    db $06
;    db $03
c3:
    db 0
nb:
    db 7
staddr:
    dw $3000
enaddr:
    dw $486A
rnaddr:
    dw $3000
    
inicio: 
    ; agora vamos desabilitar IRQ e FIRQ...
    orcc #$50
 
    ; agora vamos ligar o motor...
    lda $ff21
    ora #$8
    sta $ff21
    
    
lp3:
    clrb
    lda #8
    sta c3
; tem que ler ateh encontrar algo diferente de 55h
btte:
    bsr   lebit
    rorb
    dec c3
    bne  btte
    cmpb #$55
    beq lp3

    lda nb
    sta c3
btt2:
    bsr   lebit
    rorb
    dec c3
    bne  btt2
    
    ; x tem o endereco de destino
    ldx staddr
    ;ldx #$400
lop1:
    stb ,x+
    cmpx enaddr
    ;cmpx #$600
    beq fim
    stx $0400
    clrb
    lda  #8
    sta c3
    ; Le 8 bits para fazer 1 byte
baite:
    bsr   lebit
    rorb
    dec c3
    bne  baite    
    
    bra lop1
fim:    
    ; no final vamos habilitar IRQ e FIRQ
   andcc #$a7
    ; e desligar o motor
   lda $ff21
   anda #$f7
   sta $ff21

   ldx rnaddr
   tfr x,pc
     
    ; le um bit, retorna em cc
    ; preserva b, destroi a
lebit:
    pshs b

baixo:
    ldb $ff20  ; 4
    rorb       ; 2
    bcc baixo
    
    clra
alto:
    ldb  $ff20    ; 4
    inca
    rorb      ; 2
    bcs alto ; 3
    puls b
    cmpa c1   
    rts       
    