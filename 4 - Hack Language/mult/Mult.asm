// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Program: 
// Functionality: Implement R0*R1 by adding R0 to R2 for R1 times.
    // Create a counter to track rounds of addition
    @n
    M=0
    // Initiate R2's value at 0 to store result after each round of addition
    @R2
    M=0
(LOOP)
    // Go to END when counter n >= R1 (Add R0 for R1 times completed)
    @R1
    D=M
    @n
    D=M-D
    @END
    D;JGE    
    // Add R0 to R2
    @R0
    D=M
    @R2
    M=D+M 
    // Increase counter n by 1 
    @n
    M=M+1
    // Go to LOOP
    @LOOP
    0;JMP
(END)
    @END
    0;JMP