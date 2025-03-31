# livecodeVplot
Live codeable Vplotter


# reference projects
https://github.com/patriciogonzalezvivo/vPlotter?tab=readme-ov-file  
https://github.com/rottaca/VPlotter  
https://github.com/tinkerlog/Kritzler  
https://github.com/MarginallyClever/Makelangelo-firmware  
https://www.2e5.com/plotter/V/design/  

# arduino software
Live coding a Vplotter should be as easy as sendinng some commands. The very bare commands we need are

## commands
1. pen up
2. pen down
3. getCurrentPos
4. moveXY_Absolute
5. moveXY_Relative
6. calibrate/config
7. reset

All other commands should be implemented on the livecoding side, probably a python REPL or similar, and should be macros of these commands

## serial interface
listening for G-code style commands, industry standards


## live code interface
macros for squares/cubes/circles
macros for dashed lines
svg > 
