.data
input_file:         .asciz "Imagem_PB.raw"  # Arquivo RAW sem cabeçalho
output_img_file:    .asciz "Imagem_PB_equalizada_assembly.raw"
output_txt_file:    .asciz "ocorrencias_assembly.txt"

pixel_buffer:       .space 262144  # Buffer para 512x512 pixels
equalized_buffer:   .space 262144
histogram:          .word 0:256
cdf:                .word 0:256
cdf_min:            .word 0
cdf_max:            .word 0

.text
.globl main

main:
    # Ler arquivo de entrada
    li a7, 1024       # syscall open
    la a0, input_file
    li a1, 0          # modo leitura
    ecall
    bltz a0, exit     # erro na abertura
    
    mv s0, a0         # guardar file descriptor
    
    li a7, 63         # syscall read
    mv a0, s0
    la a1, pixel_buffer
    li a2, 262144     # tamanho máximo
    ecall
    mv s1, a0         # guardar tamanho lido
    
    li a7, 57         # syscall close
    mv a0, s0
    ecall

    # Calcular histograma
    la t0, pixel_buffer
    add t1, t0, s1
    la s2, histogram  # Carregar endereço base do histograma
calc_hist:
    lbu t2, (t0)      # Carregar pixel
    slli t3, t2, 2    # Offset = valor * 4
    add t4, s2, t3    # Endereço do elemento
    lw t5, 0(t4)      # Carregar contagem
    addi t5, t5, 1    # Incrementar
    sw t5, 0(t4)      # Guardar de volta
    addi t0, t0, 1
    blt t0, t1, calc_hist

    # Calcular CDF
    la t0, histogram
    la t1, cdf
    li t2, 0          # acumulador
    li t3, 0          # contador
calc_cdf_loop:
    lw t4, 0(t0)
    add t2, t2, t4
    sw t2, 0(t1)
    addi t0, t0, 4
    addi t1, t1, 4
    addi t3, t3, 1
    li t5, 256
    blt t3, t5, calc_cdf_loop

    # Encontrar min/max CDF
    la t0, cdf
    lw t1, 0(t0)      # cdf_min
    sw t1, cdf_min, t2
    li t3, 255
    slli t3, t3, 2
    add t0, t0, t3
    lw t1, 0(t0)      # cdf_max
    sw t1, cdf_max, t2

    # Equalizar pixels
    la t0, pixel_buffer
    la t1, equalized_buffer
    add t2, t0, s1
equalize_loop:
    lbu t3, (t0)      # valor original
    slli t4, t3, 2    # offset
    la t5, cdf
    add t5, t5, t4
    lw t4, 0(t5)      # cdf[valor]
    lw t5, cdf_min
    sub t4, t4, t5    # numerador
    li t6, 255
    mul t4, t4, t6
    lw t6, cdf_max
    sub t6, t6, t5    # denominador
    div t4, t4, t6    # novo valor
    sb t4, (t1)       # guardar pixel equalizado
    addi t0, t0, 1
    addi t1, t1, 1
    blt t0, t2, equalize_loop

    # Escrever imagem equalizada
    li a7, 1024       # syscall open
    la a0, output_img_file
    li a1, 1          # modo escrita
    ecall
    bltz a0, exit
    
    mv s2, a0
    li a7, 64         # syscall write
    mv a0, s2
    la a1, equalized_buffer
    mv a2, s1
    ecall
    
    li a7, 57         # syscall close
    mv a0, s2
    ecall

exit:
    li a7, 10
    ecall