    .data
buffer:    .space 25344       # QCIF raw
hist:      .space 1024        # 256 � 4 bytes

str_pix:   .asciz "Pixel "
str_sep:   .asciz " - Ocorrencia "
newline:   .asciz "\n"

    .text
    .globl main
main:
    # 1) Ler raw da stdin
    li   a0, 0            # fd = stdin
    la   a1, buffer
    li   a2, 25344        # m�ximo de bytes
    li   a7, 63           # syscall read
    ecall
    mv   s0, a0           # s0 = bytes realmente lidos

    # 2) Zerar histograma
    la   t0, hist
    li   t1, 256
zero_loop:
    sw   x0, 0(t0)
    addi t0, t0, 4
    addi t1, t1, -1
    bnez t1, zero_loop

    # 3) Contar cada byte lido
    la   t0, buffer       # ponteiro de leitura
    mv   t1, s0           # t1 = bytes a processar
count_loop:
    lbu  t2, 0(t0)        # t2 = pixel
    slli t3, t2, 2        # t3 = pixel*4
    la   t4, hist
    add  t4, t4, t3       # t4 = &hist[pixel]
    lw   t5, 0(t4)
    addi t5, t5, 1
    sw   t5, 0(t4)

    addi t0, t0, 1
    addi t1, t1, -1
    bnez t1, count_loop

    # 4) Imprimir histograma
    li   t0, 0            # �ndice X
print_loop:
    # "Pixel "
    la   a0, str_pix
    li   a7, 4
    ecall

    # X
    mv   a0, t0
    li   a7, 1
    ecall

    # " - Ocorrencia "
    la   a0, str_sep
    li   a7, 4
    ecall

    # hist[X]
    slli t1, t0, 2
    la   t2, hist
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

    # 5) Sair
    li   a7, 10
    ecall
