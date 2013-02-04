    org $2000
    
    bra main
    
    
    
    
main:
     pshs a,x
     clra
     sta $ff22
     sta $ffc3
;     sta $ffc5
     
    ldx #$400
lp1:
     ora #$80
     sta, x+
     inca
     cmpx #$1c00
     bne lp1
lp2:     
     jsr [$a0z00]
     beq lp2
     puls a,x
     rts
     
    