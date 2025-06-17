# the config variable contains all startup parameters. These cannot be changed without restarting the server
config = { 
    "osc": {
        "enabled": True,
        "ip": "0.0.0.0",
        "port": 1137  
    },
    "serial":{
        "dev": '/dev/ttyUSB0', 
        "speed":115200, 
        "timeout":2
    },
    "plotter": {
        "minX":0,
        "minY":0,
        "maxX":780, # mm
        "maxY":1720, # mm
        "fspeed":4000, # mm/min
        "accel":100,  # mm/s**2
    }
}
