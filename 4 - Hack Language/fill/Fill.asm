// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Program: Fill.asm
// Functionality: Dynamically fill screen with black when a key is pressed;
// Dynamically unfill screen with white when no key is pressed.
    // Create a pointer to track current painting address
    // Set pointer's starting value to SCREEN
    @SCREEN
    D=A
    @pointer
    M=D
(LOOP)
    // Get the value at KBD
    @KBD
    D=M
    // When pressed (KBD != 0), go to FILL
    @FILL
    D;JNE
    // When not pressed (KBD == 0), go to UNFILL
    @UNFILL
    D;JEQ
(FILL)
    // Stop filling when pointer is at KBD-1 (last RAM address for screen)
    // Directly go back to LOOP
    @pointer
    D=M
    @KBD
    D=D-A
    @LOOP
    D;JGE
    // Pointer hasn't reached KBD-1, fill black at current pointer address
    @pointer
    A=M
    M=-1
    // Increase pointer by 1
    @pointer
    M=M+1 
    // Go to LOOP
    @LOOP
    0;JMP
(UNFILL)
    // Stop unfilling when pointer is at SCREEN (first RAM address for screen)
    @pointer
    D=M
    @SCREEN
    D=D-A
    @LOOP 
    D;JLE
    // Pointer hasn't reached SCREEN, fill white to the prior pointer address
    // which was the latest blackened bits.
    @pointer
    A=M-1
    M=0
    // Decrease pointer by 1
    @pointer
    M=M-1
    // Go to LOOP
    @LOOP
    0;JMP