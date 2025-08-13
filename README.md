# livecodeVplot
Live codeable Vplotter


GRBL needs to stream
https://onehossshay.wordpress.com/2011/08/26/grbl-a-simple-python-interface/

is buffer is full, wait...
python buffer

# reference projects
https://github.com/patriciogonzalezvivo/vPlotter?tab=readme-ov-file  
https://github.com/rottaca/VPlotter  
https://github.com/tinkerlog/Kritzler  
https://github.com/MarginallyClever/Makelangelo-firmware  
https://www.2e5.com/plotter/V/design/  

# arduino software
Live coding a Vplotter should be as easy as sending some commands. The very bare commands we need are

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




## create SVG from vsk

vsk save "sketchname" --config "configname"


## create HPGL from svg for ROLAND plotter

vpype read test.svg.svg linemerge --tolerance 0.1mm linesort reloop linesimplify layout -l --fit-to-margins 1cm --page-size a3 --landscape write knota3props.svg 
vpype read test.svg.svg linemerge --tolerance 0.1mm linesort reloop linesimplify layout -l --fit-to-margins 1cm  a3 write knota3props.svg 

vpype read input.svg write --device dxy --page-size a3 --landscape output.hpgl             

vpype read patterns/output/patterns_carvegrid1.svg write --device dxy --page-size a3 --landscape output.svg

### fit drawing to page
-m = margin
vpype read patterns/output/patterns_carvegrid2.svg layout -m  3cm --landscape  a3     write --device dxy  output.hpgl

### plot it

#### ubuntu connect 
1.
sudo rfcomm release rfcomm0

2.
-Open bluetooth prefs  DONT- remove device HC06
-reconnect
- Connect to HC06 > pin 1234

3.
sudo rfcomm bind rfcomm0  20:13:07:25:34:59

#### send to plotter via chiplotle



## create GCODE file for DIY ploytter

vpype read kaos/output/kata225.svg gscrib --config=plotterXY_config.toml --output=output.gcode