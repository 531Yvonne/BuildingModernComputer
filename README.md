# Building a Modern Computer
This is a Project based on Nand2Tetris, which builds a modern computer from scratch at both hardware and software level.

# Video Demo
[![Watch the video](https://img.youtube.com/vi/E6q1FZwOOzY/0.jpg)](https://youtu.be/E6q1FZwOOzY)

# Overview
## Logic Chips

Hardware Description Language (HDL) is used to build a set of elementary logic gates (And, Or, Not, Mux, ...)

## Arithmetic Logic Unit and RAM

Elementary logic gates are used to build a family of adder chips, culminating in the construction of an Arithmetic-Logic Unit and further more ---- build a memory hierarchy, from single-bit cells to registers to RAM units of arbitrary sizes.
  
## Machine Language and Computer Architecture

* Two low-level interactive programs are written in assembly language, they can be executed on the given CPUEmulator.

* Computer Architecture: build the computer by combining CPU, Memory, known as Hack, which can be used to run the programs wrote in assembly language

## Assembler

Translate the symbolic instructions into binary codes understood by the computer we built. In order to develop this assembler, the python program performs parsing, code generation, and symbol resolution.

## VM Translator

Modern compilers typically translate high-level programs into an intermediate code designed to run on an abstract virtual machine. The python program in this folder is a JRE-like program that translates the push/pop and arithmetic VM commands into assembly code, designed to run on the Hack computer built earlier.

In part 2, two critically important programming abstractions: branching and subroutines can be realized, which extends the basic translator built in part 1 into a full-blown VM translator. This translator will become the backend of compilers that translate high-level programs into VM code (similar to Bytecode). 

## Compiler

* Context-free grammars and recursive parsing algorithms were used to build a syntax analyzer (tokenizer and parser) for the Jack language
* Morph the syntax analyzer built in part 1 into a full-scale compiler that realizes high-level programming abstractions (classes, methods, statements, expressions, objects, etc.) and translates Jack programs into VM code. 

## Game Programming using High Level Language

A high level language Jack – a simple, high-level, object-based, java like language, was used to design a grahical and keyboard controlled computer game, which can be executed on the Hack computer.

