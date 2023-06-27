# Project 9: Diamond Hunter Game
#
# Yves Yang
#
# The directory contains .jack files for a Game written in Jack Language


* Compile jack files by running line below in command line:
	
JackCompiler.sh <replace by the path to directory DiamondHunter>


* Load the directory (with compiled .vm files) in VMEmulator.sh and Run the program (select NO animation mode, set FAST running speed for better experience)


* GAME INSTRUCTIONS *

- Start the game by pressing P. 
- Use Arrows to move the Thief, avoid the bouncing Policemen(random positioned each round) and collect the diamond.
- Once caught or collected the diamond, press P to play again, press Q to quit.


* Minor Issue *

Identifying whether Thief got caught by Policeman is implemented by comparing the Bitmap Editor parameter "location" for both characters. So sometimes a minor overlap won't result in "You're Caught!" (since the location points are not actually the same.)