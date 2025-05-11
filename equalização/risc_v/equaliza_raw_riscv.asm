# equaliza_raw_riscv.asm
# Lê QCIF raw (176×144) e escreve raw equalizado.

    .data
hist:      .space 1024      # histograma
map_eq:    .space 1024      # mapa de equalização
buffer:    .space 25344     # QCIF raw

    .text
    .globl main
main:
    # 1) Ler raw
    li   a0, 0
    la   a1, buffer
    li   a2, 25344
    li   a7, 63       # read
    ecall

    # 2) Zerar histograma
    la   t0, hist
    li   t1, 256
zero_loop:
    sw   x0, 0(t0)
    addi t0, t0, 4
    addi t1, t1, -1
    bnez t1, zero_loop

    # 3) Construir histograma
    la   t0, buffer
    li   t1, 25344
fill_loop:
    lbu  t2, 0(t0)
    addi t0, t0, 1
    slli t3, t2, 2
    la   t4, hist
    add  t4, t4, t3
    lw   t5, 0(t4)
    addi t5, t5, 1
    sw   t5, 0(t4)
    addi t1, t1, -1
    bnez t1, fill_loop

    # 4) Gerar mapa de equalização
    la   t0, hist
    la   t1, map_eq
    li   t2, 0        # acumulado
    li   t3, 0        # índice
    li   t4, 25344    # total pixels
map_loop:
    lw   t5, 0(t0)
    add  t2, t2, t5
    li   t5, 255
    mul  t5, t2, t5
    div  t5, t5, t4
    sw   t5, 0(t1)
    addi t0, t0, 4
    addi t1, t1, 4
    addi t3, t3, 1
    li   t6, 256
    blt  t3, t6, map_loop

    # 5) Aplicar equalização
    la   t0, buffer
    li   t1, 25344
apply_loop:
    lbu  t2, 0(t0)
    slli t3, t2, 2
    la   t4, map_eq
    add  t4, t4, t3
    lw   t5, 0(t4)
    sb   t5, 0(t0)
    addi t0, t0, 1
    addi t1, t1, -1
    bnez t1, apply_loop

    # 6) Escrever raw equalizado
    li   a0, 1
    la   a1, buffer
    li   a2, 25344
    li   a7, 64       # write
    ecall

    # 7) Exit
    li   a7, 10
    ecall
