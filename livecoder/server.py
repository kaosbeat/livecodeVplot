import asyncio
import serial
import time 
import random
from threading import Event
from threading import Thread
from queue import Queue
from rtmidi.midiutil import open_midiinput, list_input_ports
import mido
from configdata import config
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
# from lib.midiinitiutil import available_inports_list
# from lib.midiparser import parseMsg, connectMidi
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=2)

oscip = config["osc"]["ip"]
oscport = config["osc"]["port"]
oscloop = False

BAUD_RATE = 115200

curX=0
curY=0
minX=0
minY=0
maxX=780
maxY=1720
fspeed=8000





def checkLimits(x,y):
    global curX,curY,minX,minY,maxX,maxY
    print("X = ", curX + x)
    print("Y = ", curY + y) 
    if (not (minX < curX + x < maxX)) or (not (minY < curY + y < maxY)):
        print("out of limits!")
        return False
    return True

def checkLimitsAbs(x,y):
    global curX,curY,minX,minY,maxX,maxY
    print("X = ", x)
    print("Y = ", y) 
    if (not (minX < x < maxX)) or (not (minY < y < maxY)):
        print("out of limits!")
        return False
    return True


def remove_comment(string):
    if (string.find(';') == -1):
        return string
    else:
        return string[:string.index(';')]


def remove_eol_chars(string):
    # removed \n or traling spaces
    return string.strip()

def wait_for_movement_completion(ser,cleaned_line):
    Event().wait(0.5)
    if cleaned_line != '$X' or '$$':
        idle_counter = 0
        while True:
            # Event().wait(0.01)
            ser.reset_input_buffer()
            command = str.encode('?' + '\n')
            ser.write(command)
            grbl_out = ser.readline() 
            grbl_response = grbl_out.strip().decode('utf-8')
            if grbl_response != 'ok':
                if grbl_response.find('Idle') > 0:
                    idle_counter += 1
            if idle_counter > 10:
                break
    return

def stream_gcode(ser,gcode):
    # with contect opens file/connection and closes it if function(with) scope is left
        # send_wake_up(ser)
        for line in gcode.splitlines():
            # cleaning up gcode from file
            cleaned_line = remove_eol_chars(remove_comment(line))
            # print(line)
            if cleaned_line:  # checks if string is empty
                print("Sending gcode:" + str(cleaned_line))
                # converts string to byte encoded string and append newline
                command = str.encode(line + '\n')
                ser.write(command)  # Send g-code
                wait_for_movement_completion(ser,cleaned_line)
                grbl_out = ser.readline()  # Wait for response with carriage return
                print(" : " , grbl_out.strip().decode('utf-8'))
        print('End of gcode')

def initPlotter():
    global curX,curY,minX,minY,maxX,maxY
    gcode='''
        G21 ; millimeters
        G90 ; absolute coordinate
        G17 ; XY plane
        G94 ; units per minute feed rate mode
        M3 S555 ; Turning on spindle
        G0 X0 Y0 ; Go to zero location
        G04P0.01 ; timeout sync
        '''
    stream_gcode(ser,gcode)
    # ser.write(gcode.encode())
    # response = ser.readline()
    # print(response.decode())
    # ser.close()
    print("xy=", curX, curY )
    print("limits minXY=", minX , minY )
    print("limits maxXY=", maxX , maxY )

def initPen():
    gcode = '''
        G90 ; absolute coordinates
        G21 Z5 F1000;
        G21 Z0 F1000;
        '''
    stream_gcode(ser,gcode)
    
    # ser.write(gcode.encode())
    # response = ser.readline()
    # print("pen init :" + response.decode())

def placePen():
    gcode = '''
        G90 ; absolute coordinates
        G21 Z5 F1000;
        '''
    stream_gcode(ser,gcode)
    
    # ser.write(gcode.encode())
    # response = ser.readline()
    # print("pen placed :" + response.decode())

def liftPen():
    gcode = '''
        G90 ; absolute coordinates
        G21 Z0 F1000;
        '''
    stream_gcode(ser,gcode)
    
    # ser.write(gcode.encode())
    # response = ser.readline()
    # print("pen lifted :" + response.decode())


def goto(x,y):
    global curX,curY,minX,minY,maxX,maxY,fspeed
    liftPen()
    print("gotoX = ", x)
    print("gotoY = ", y) 
    if checkLimitsAbs(x,y):
        gcode = "G90 \n G0 X%d Y%d F%d" %(x,y,fspeed )
        # print(gcode)
        stream_gcode(ser,gcode)
        # ser.write(gcode.encode())
        # response = ser.readline()
        # print(response.decode())
        curX=x
        curY=y
        return True
    else:
        return False

    
     
def rectangle(width,height):
    global curX,curY,minX,minY,maxX,maxY,fspeed
    if checkLimits(width,height):
        placePen()
        gcode='''
        ; relative mode
        G91
        ; Create rectangle
        G1 X0 Y0 F{fspeed}
        G1 Y{width}
        G1 X{height}
        G1 Y-{width}
        G1 X-{height}
        ; absolutre mode
        G90
        '''.format(width=width, height=height, fspeed=fspeed )
        stream_gcode(ser,gcode)
        
        # ser.write(gcode.encode())
        # response = ser.readline()
        # print(response.decode())
        # ser.close()


def line(x,y):
    '''
     draw line from currentXY to curX+x, curY+y
    '''
    global curX,curY,minX,minY,maxX,maxY,fspeed
    if checkLimits(x,y):
        placePen()
        gcode='''
        ; relative mode
        G91
        ; Create line
        G1 X0 Y0 F{fspeed}
        G1 X{x} Y{y}
        ; absolute mode
        G90
        '''.format(x=x, y=y, fspeed=fspeed )
        stream_gcode(ser,gcode)
        
        # ser.write(gcode.encode())
        # response = ser.readline()
        # print(response.decode())
        curX+=x
        curY+=y
        # print("linecommand done:")
        # response = ser.readline()
        # print(response.decode())
        return True
    else:
        return False

def oscword(address, *args):
    global oscqueue, oscloop
    oscloop = True
    plt = {
        "cmd": args[0], 
        "par":args[1], 
    }
    print(plt)
    oscqueue.put(plt)

async def oscPLT(oscqueue):
    global oscloop
    while True:
        while oscloop:
            while (oscqueue.qsize() > 0):
                print("playing OSCloop", str(oscqueue.qsize()), str(oscloop))
                plt = oscqueue.get()
                print(plt)
                with oscqueue.mutex:
                    oscqueue.queue.clear()
                # await asyncio.sleep(line["transition"]/1000)
                # print("oscloop = ", str(oscloop))
        await asyncio.sleep(1) 
        # print("waiting for osc") 




## init Midi
print("init Midi")
ports = mido.get_input_names()
print(ports)

## init plotter
print("init plotter")
initPlotter()
initPen()
goto(200,200)
# placePen()

for i in range(7):
    rectangle(i*40,i*60)
    liftPen()
    # line(random.randint(0,100),random.randint(0,100))
line(50,0)
# goto(0,0)
# line(0,60)
# goto(0,0)
# line(60,60)
# goto(0,0)
# liftPen()  
# goto(340,-140)
# goto(340,140)
# goto(0,140)
# goto(0,0)
rectangle(100,140)
liftPen()
goto(0,0)
ser.close()

async def loop():
    """Example main loop that only runs for 10 iterations before finishing"""
    for i in range(10):
        print(f"Loop {i}")
        await asyncio.sleep(1)
        

## init OSC
dispatcher = Dispatcher()
dispatcher.map("/pltcmd", oscword)
oscqueue = Queue()
  
        
async def main():
    global oscqueue    
    oscdaemon = Thread(target=asyncio.run , args=(oscPLT(oscqueue),), daemon=True, name='oscPLT')
    oscdaemon.start()
    
    try:
        print("initializing osc client")
        oscserver = AsyncIOOSCUDPServer((oscip, oscport), dispatcher, asyncio.get_event_loop())
        transport, protocol = await oscserver.create_serve_endpoint()  # Create datagram endpoint and start serving
        await loop()
        
        transport.close() 
        
    except KeyboardInterrupt:
        print('killed by keyboard')
        transport.close()
    finally:
        print("closing") 

if __name__ == "__main__":
    asyncio.run(main())
