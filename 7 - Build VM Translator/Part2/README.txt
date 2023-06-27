# Project 8: VM Translator Part 2
#
# Yves Yang
#
# This source code contains a program to convert .vm file input or a directory contains .vm file(s) to assembly code at a .asm file under the same directory as the input file.


* This is a python3 program, no need to compile.

* To run the code: run the line below in your command line in the src directory:

When input is a single Xxx.vm file: 
Please Run: python3 project8.py <replace by the path of your input file (including Xxx.vm)>
The corresponding .asm output file will be generated to the same directory and named as Xxx.asm


When input is a directory with folder name Xxx
Please Run: python3 project8.py <replace by the path of this directory (DO NOT include any ending slash!!!)>
The corresponding .asm output file will be generated in this directory and named as Xxx.asm


* Functionality in detail:

<passed> ---- BasicLoop (no bootstrap code needed)
<passed> ---- FibonacciSeries (no bootstrap code needed)
<passed> ---- SimpleFunction (no bootstrap code needed)
<passed> ---- FibonacciElement (requires bootstrap code)
<passed> ---- StaticsTest (requires bootstrap code)