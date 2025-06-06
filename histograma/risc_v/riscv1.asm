

    .data
hist:       .space 1024

buffer:     .space 25344

str_pix:    .string "Pixel "
str_sep:    .string " - Ocorrencia "
str_nl:     .string "\n"

    .text
    .globl main
main:
    li   a0, 0            # file descriptor stdin
    la   a1, buffer       # endere�o do buffer
    li   a2, 25344        # n�mero de bytes a ler
    li   a7, 63           # syscall read
    ecall

    la   t0, hist
    li   t1, 256
zero_loop:
    sw   x0, 0(t0)
    addi t0, t0, 4
    addi t1, t1, -1
    bnez t1, zero_loop

    la   t2, buffer
    li   t3, 25344
proc_loop:
    lbu  t4, 0(t2)
    addi t2, t2, 1
    slli t5, t4, 2
    la   t6, hist
    add  t6, t6, t5
    lw   s1, 0(t6)
    addi s1, s1, 1
    sw   s1, 0(t6)
    addi t3, t3, -1
    bnez t3, proc_loop

    li   s0, 0
print_loop:
    # print_string "Pixel "
    la   a0, str_pix
    li   a7, 4
    ecall
    # print_int s0
    mv   a0, s0
    li   a7, 1
    ecall
    # print_string " - Ocorrencia "
    la   a0, str_sep
    li   a7, 4
    ecall
    # print_int hist[s0]
    slli s2, s0, 2
    la   s3, hist
    add  s3, s3, s2
    lw   a0, 0(s3)
    li   a7, 1
    ecall
    # print_string newline
    la   a0, str_nl
    li   a7, 4
    ecall
    # pr�ximo �ndice
    addi s0, s0, 1
    li   s4, 256
    blt  s0, s4, print_loop

    li   a7, 10
    ecall
