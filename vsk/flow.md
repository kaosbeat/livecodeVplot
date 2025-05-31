# create Sketch
`vsk run my_project`

do some live coding now    


# save sketch to config file from gui

"press sve"
name it `my_config`

# run the svg export

`vsk save --config my_coonfig sketch_kaos.py `

from the sketch directory  


# convert to gcode



# CLI
vpype \
  read drawing.svg \
  linemerge --tolerance=0.5mm \
  linesimplify --tolerance=0.1mm \
  reloop --tolerance=0.1mm \
  linesort --two-opt --passes=250 \
  gscrib 
    --tool-type=marker \
    --rack-type=manual \
    --work-z=1mm \
    --length-units=millimeters \
    --direct-write serial \
    --baudrate 115200 \
    --output=output.gcode
    



# using config
vpype read drawing.svg gscrib --config=plotterXY_config.toml --output=output.gcode