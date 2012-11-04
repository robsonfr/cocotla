    org $2000
      
       
    ; rotina para ler os dados
 
    ; agora vamos desabilitar IRQ e FIRQ...
    orcc #$50
 
    ; agora vamos ligar o motor...
    lda $ff21
    ora #$8
    sta $ff21
    
    ldx #$0
l2:    leax -1,x
    bne l2

    ; x tem o endereco de destino
    ldx    #$400
lop1:
    clrb
    lda  #8
    
    ; Le 8 bits para fazer 1 byte
baite:
    bsr   lebit
    rorb
    deca
    bne  baite
    
    stb, x+
    cmpx #$600
    bne lop1
    
    ; no final vamos habilitar IRQ e FIRQ
    andcc #$a7
    ; e ligar o motor
    lda $ff21
    anda #$f7
    sta $ff21

    ; para fechar, um loop infinito...
lp1: 
     bra lp1    
     
    ; le um bit, retorna em cc
    ; preserva a e b, destroi y
lebit:
    pshs a,b

baixo:
    ldb $ff20  ; 4
    rorb       ; 2
    bcc baixo
    
    ldy #0
alto:
    ldb  $ff20    ; 4
    leay 1,y
    rorb      ; 2
    bcs alto ; 3
    
    puls b,a
    cmpy #$0002 
    rts           
   