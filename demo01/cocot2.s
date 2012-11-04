    org $2000
      
    
    bra principal
  
            db $ff
    
principal:
    ; rotina para ler os dados
       
    ldu  #$ff20
    
    ; primeiro vamos ligar o motor...
    lda 1,u
    ora #$8
    sta 1,u
    
    ; agora vamos desabilitar IRQ e FIRQ...
    ;    orcc #$50    
     
    ; x tem o endereco de destino
    ldx    #$400
    clra
lop1:

    ; vamos ler o bit e escrever na tela... ateh fechar 512 bits (64 bytes ou 2 linhas...)
    ldb, u
    andb #1
    cmpb $2002
    beq incrementa
armaz:
    sta, x+
    lda $2002
    anda #$1
    adda #112
    sta, x+
    stb $2002
    clra
    cmpx #$1600
    bne lop1
    bra finaliza
incrementa:
    inca
    bne lop1
    deca
    bra armaz

finaliza:    
    ; no final vamos habilitar IRQ e FIRQ
  ;  andcc #$a7
    ; e desligar o motor
    lda 1,u
    anda #$f7
    sta 1,u

    ; para fechar, um loop infinito...
lp1: 
     bra lp1    
     
    ; le um bit, retorna em cc
    ; preserva a e b
lebit:
    pshs a,b

baixo:
    ldb, u    ; 4
    rorb      ; 2
    bcc baixo ; 3

    clra    
alto:
    inca       ; 2
    ldb, u     ; 4
    rorb       ; 2
    bcs alto   ; 3    

baixo2:
    ldb, u    ; 4
    rorb      ; 2
    bcc baixo2 ; 3    

    cmpa #$3
    puls b,a
    rts           
   