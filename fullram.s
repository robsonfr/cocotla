    org $e00

    orcc #$50    ; disable irq and firq
    ldx #$1c00
lp1:    
    sta $ffde
    lda ,x
    sta $ffdf
    sta ,x+
    cmpx $ff00
    bne lp1
    andcc #$af  ; enable irq and firq
    rts
    
    