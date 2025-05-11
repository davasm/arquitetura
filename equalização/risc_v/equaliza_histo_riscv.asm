# equaliza_e_histo_riscv.asm
# Lê até 25344 bytes da stdin (QCIF 176×144), equaliza o histograma
# e imprime o histograma da imagem equalizada em texto.

    .data
buffer:    .space 25344    # QCIF raw
hist:      .space 1024     # histograma original
map_eq:    .space 1024     # mapa de equalização
hist2:     .space 1024     # histograma equalizado

str_pix:   .asciz "Pixel "
str_sep:   .asciz " - Ocorrencia "
newline:   .asciz "\n"

    .text
    .globl main
main:
    # 1) Ler raw da stdin
    li   a0, 0            # fd = stdin
    la   a1, buffer
    li   a2, 25344        # máximo de bytes
    li   a7, 63           # syscall read
    ecall
    mv   s0, a0           # s0 = bytes realmente lidos

    # 2) Zerar hist[] e hist2[]
    la   t0, hist
    la   t1, hist2
    li   t2, 256
zero_both:
    sw   x0, 0(t0)
    sw   x0, 0(t1)
    addi t0, t0, 4
    addi t1, t1, 4
    addi t2, t2, -1
    bnez t2, zero_both

    # 3) Construir hist[] da original
    la   t0, buffer
    mv   t1, s0
    la   t2, hist
build_hist:
    lbu  t3, 0(t0)
    addi t0, t0, 1
    slli t4, t3, 2
    add  t5, t2, t4
    lw   t6, 0(t5)
    addi t6, t6, 1
    sw   t6, 0(t5)
    addi t1, t1, -1
    bnez t1, build_hist

    # 4) Gerar mapa de equalização em map_eq[]
    la   t0, hist
    la   t1, map_eq
    li   t2, 0         # acumulado
    li   t3, 0         # índice
    mv   t4, s0        # total pixels
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

    # 5) Aplicar equalização no buffer
    la   t0, buffer
    mv   t1, s0
    la   t2, map_eq
apply_eq:
    lbu  t3, 0(t0)
    addi t0, t0, 1
    slli t4, t3, 2
    add  t5, t2, t4
    lw   t6, 0(t5)
    sb   t6, -1(t0)
    addi t1, t1, -1
    bnez t1, apply_eq

    # 6) Recontar histograma da imagem equalizada em hist2[]
    la   t0, buffer
    mv   t1, s0
    la   t2, hist2
build_hist2:
    lbu  t3, 0(t0)
    addi t0, t0, 1
    slli t4, t3, 2
    add  t5, t2, t4
    lw   t6, 0(t5)
    addi t6, t6, 1
    sw   t6, 0(t5)
    addi t1, t1, -1
    bnez t1, build_hist2

    # 7) Imprimir hist2[]
    li   t0, 0
print_loop:
    # "Pixel "
    la   a0, str_pix
    li   a7, 4
    ecall

    # índice
    mv   a0, t0
    li   a7, 1
    ecall

    # " - Ocorrencia "
    la   a0, str_sep
    li   a7, 4
    ecall

    # hist2[t0]
    slli t1, t0, 2
    la   t2, hist2
    add  t2, t2, t1
    lw   a0, 0(t2)
    li   a7, 1
    ecall

    # newline
    la   a0, newline
    li   a7, 4
    ecall

    addi t0, t0, 1
    li   t1, 256
    blt  t0, t1, print_loop

    # 8) Exit
    li   a7, 10
    ecall
