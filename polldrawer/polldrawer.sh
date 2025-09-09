#!/bin/bash
/usr/bin/screen -s "/bin/bash" -dmS polldrawer
/usr/bin/screen  -S polldrawer -X stuff "cd /home/kaos/livecodeVplot/polldrawer\n"
/usr/bin/screen  -S polldrawer -X stuff "pyenv activate vplotter\n"
/usr/bin/screen  -S polldrawer -X stuff "python polldrawer.py\n"

