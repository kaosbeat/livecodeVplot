import asyncio
import serial
import time 
import random
import pickle

from threading import Event
from threading import Thread
from queue import Queue
from rtmidi.midiutil import open_midiinput, list_input_ports
from lib.midiinitiutil import available_inports_list, connectMidi
from lib.midiparser import parseMsg
import mido
from configdata import config
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
# from lib.midiinitiutil import available_inports_list
# from lib.midiparser import parseMsg, connectMidi
from vectorfuncs import *
from motionfuncs import *


if config["mode"] == "serial":
    ser = serial.Serial(config["serial"]["dev"], config["serial"]["speed"], timeout=config["serial"]["timeout"])
elif config["mode"] == "virtual":
    ser = virtualserialports.run(1, loopback=True, debug=False)
    # ser = "/dev/pts/2"

voteconfig = {
    "turfsperline" : 100,
    "turfwidth" : 10,
    "turfheight" : 40,
    "turfspace": 20,
    "farmy" : 100,
    "housey" : 200,
    "woodsy" : 300,
    "arty": 400,
    "shopy" : 500 
}

print("getting ready")

print(ser)

oscip = config["osc"]["ip"]
oscport = config["osc"]["port"]
oscloop = False

BAUD_RATE = 115200



state={
    'curX':0,
    'curY':0,
    'mode':'init',
    'gcode': """"""
}

minX= config["plotter"]["minX"]
minY= config["plotter"]["minY"]
maxX = config["plotter"]["maxX"]
maxY = config["plotter"]["maxY"]
fspeed =  config["plotter"]["fspeed"]


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

# votes = {
#     "farm":0,
#     "house":0,
#     "woods":0,
#     "art":0,
#     "shop":0,
#     "status":"done"
# }

votes = {}
# save_object(votes,"votes.pickle")

def loadData():
    global votes
    print("loading data")
    with open("votes.pickle", 'rb') as inp:
        votes = pickle.load(inp)
        print(votes)

def saveGCODE():
    global state
    with open("total.gcode", "w") as f:
        f.write(state["gcode"])

def checkLimits(x,y):
    global state, config
    print("X = ", state['curX'] + x)
    print("Y = ", state['curY'] + y) 
    if (not (config['plotter']['minX'] < state['curX'] + x < config['plotter']['maxX'])) or (not (config['plotter']['minY'] < state['curY'] + y < config['plotter']['maxY'])):
        print("out of limits!")
        return False
    return True

def checkLimitsAbs(x,y):
    global state, config
    print("X = ", x)
    print("Y = ", y) 
    if (not (config['plotter']['minX'] < x < config['plotter']['maxX'])) or (not (config['plotter']['minY'] < y < config['plotter']['maxY'])):
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
    Event().wait(0.005)
    print("about to send", cleaned_line)
    if cleaned_line != '$X' or '$$':
        idle_counter = 0
        while True:
            if config["mode"] == "serial":
                # Event().wait(0.01)
                ser.reset_input_buffer()
                command = str.encode('?' + '\n')
                ser.write(command)
                grbl_out = ser.readline() 
                grbl_response = grbl_out.strip().decode('utf-8')
            else:
                grbl_response = 'ok'
                idle_counter = 11
            if grbl_response != 'ok':
                if grbl_response.find('Idle') > 0:
                    idle_counter += 1
            if idle_counter > 10:
                break
    return

def stream_gcode(ser,gcode):
    global state
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
            state["gcode"]+=(line + '\n')
            wait_for_movement_completion(ser,cleaned_line)
            grbl_out = ser.readline()  # Wait for response with carriage return
            print(" : " , grbl_out.strip().decode('utf-8'))
    print('End of gcode')
    saveGCODE()

def initPlotter():
    global state, config    
    gcode='''
        G21 ; millimeters
        G90 ; absolute coordinate
        G17 ; XY plane
        G94 ; units per minute feed rate mode
        M3 S555 ; Turning on spindle
        G0 X0 Y0 F1500 ; Go to zero location
        G04P0.01 ; timeout sync
        '''
    stream_gcode(ser,gcode)
    
    # saveGCODE
    # ser.write(gcode.encode())
    # response = ser.readline()
    # print(response.decode())
    # ser.close()i
    print("xy=", state['curX'], state['curY'] )
    print("limits minXY=", config['plotter']['minX'] , config['plotter']['minY'] )
    print("limits maxXY=", config['plotter']['maxX'] , config['plotter']['maxY'] )
    state['mode'] = 'ready'

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


def goto(x,y, speed=None):
    global state, config    
    # global curX,curY,minX,minY,maxX,maxY,fspeed
    if speed == None:
        speed = config["plotter"]['fspeed']
    liftPen()
    print("gotoX = ", x)
    print("gotoY = ", y) 
    print("gotospeed =", speed)
    if checkLimitsAbs(x,y):
        gcode = "G90 \n G0 X%d Y%d F%d" %(x,y,speed )
        # print(gcode)
        stream_gcode(ser,gcode)
        # ser.write(gcode.encode())
        # response = ser.readline()
        # print(response.decode())
        state['curX']=x
        state['curY']=y
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


def line(x,y, speed):
    '''
     draw line from currentXY to curX+x, curY+y
    '''
    global config, state
    if speed == None:
        speed = config["plotter"]['fspeed']
    print("linespeed =", speed)
    if checkLimits(x,y):
        placePen()
        gcode='''
        ; relative mode
        G91
        ; Create line
        G1 X0 Y0 F{speed}
        G1 X{x} Y{y}
        ; absolute mode
        G90
        '''.format(x=x, y=y, speed=speed )
        stream_gcode(ser,gcode)
        
        # ser.write(gcode.encode())
        # response = ser.readline()
        # print(response.decode())
        state['curX']+=x
        state['curY']+=y
        # print("linecommand done:")
        # response = ser.readline()
        # print(response.decode())
        return True
    else:
        return False

def turf(vote):
    global config, state, votes, voteconfig
    # first add vote to db
    votes[vote] += 1
    votes["status"] == "updating"

    # calculate position
    if vote == "farm":
        ypos = voteconfig["turfheight"]*votes["farm"]//voteconfig["turfsperline"] + voteconfig["farmy"]
    if vote == "house":
        ypos = voteconfig["turfheight"]*votes["house"]//voteconfig["turfsperline"] + voteconfig["housey"]
    if vote == "woods":
        ypos = voteconfig["turfheight"]*votes["woods"]//voteconfig["turfsperline"] + voteconfig["woodsy"]
    if vote == "art":
        ypos = voteconfig["turfheight"]*votes["art"]//voteconfig["turfsperline"] + voteconfig["arty"]
    if vote == "shop":
        ypos = voteconfig["turfheight"]*votes["shop"]//voteconfig["turfsperline"] + voteconfig["shopy"]

    xpos = voteconfig["turfwidth"] * votes[vote]%voteconfig["turfsperline"] 

    if votes[vote]%5 == 0: 
        linetype = "slant"
        xpos -= 5*voteconfig["turfwidth"]
        ypos += 1*voteconfig["turfheight"]/5
        xpos2 = xpos+6*voteconfig["turfwidth"]
        ypos2 = ypos+3*voteconfig["turfheight"]/5
    else:
        linetype = straight
        xpos2 = xpos
        ypos2 = ypos + voteconfig["turfheight"]

    goto(xpos,ypos, speed=None)
    line(xpos2, ypos2)

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
                if plt["cmd"] == "test":
                    rectangle(100,100)
                # if plt["cmd"] == "mode":
                #     if state["mode"] = plt["par"]
                # else:
                #     if state["mode"] = "control"
                #         if plt["cmd"] == ""
                

                with oscqueue.mutex:
                    oscqueue.queue.clear()
                # await asyncio.sleep(line["transition"]/1000)
                # print("oscloop = ", str(oscloop))
        await asyncio.sleep(1) 
        # print("waiting for osc") 

## extra motion helper functions


# calculate distance and time to goto
def gotoXYinTime(x,y,ms):
    global state, config
    '''returns speed in mm/s needed to go to x,y in ms'''
    print(state)
    d = dist(state['curX'],state['curY'],x, y)
    print("distance = ", d)
    # time needed to accel/decel to max speed
    t = TfromVA(config['plotter']["fspeed"], config['plotter']['accel'])
    print("acceltime = ", t)
    # distance traveled during accel / decel
    da = XfromAT(config['plotter']['accel'], 2*t)
    print("acceldistance = ", da)
    # minimum time needed for d
    if da > d:
        # full speed never reached
        #minimum time to reach d = td
        td = TfromXA(d, config['plotter']['accel'])
        if td > ms/1000:
            # we cannot fulfill request
            print(" impossible timing, minimum time in ms: ", td)
            return config['plotter']["fspeed"]
        if ms/1000 >= td:
            # adjust max speed so we go slow enough
            v = VfromXA(d,config['plotter']['accel'])
            # not taking into account accel decel to new calc for now
            print("speed is ", v)
            return v
    else:
        # distance not covered during accel / decel at  max speed = dv
        dv = d - da
        # we just return the maxspeed
        print("speed is maxspeed ", config['plotter']["fspeed"])
        return config['plotter']["fspeed"]



def input_callback(msg):
    print("MESSAGE RECEIVED", msg)

## init Midi
print("init Midi")
ports = mido.get_input_names()
print(ports)
# inport = mido.open_input('Teensy MIDI:Teensy MIDI Port 1 24:0', callback=input_callback)

# mididevices = available_inports_list()
## put alle devices in list
port_name = 'Teensy MIDI:Teensy MIDI Port 1 24:0'
print(port_name)
# print(mididevices)
midiin, port_name = open_midiinput(port_name)


class MidiInputHandler(object):
    global ticks

    def __init__(self, port):
        self.port = port
        # self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        # self._wallclock += deltatime
        # print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        print(message[2])
        if message[1] == 1 and message[2] == 127:
            goto(100,100)
            line(60,60)

        # parseMsg(event, deltatime)  ### needs to be rtmidi msg obj? not event?

    #         parseNote   On(message)




## init plotter
print("init plotter")
initPlotter()
initPen()


## load database status




# print("GOING, ", gotoXYinTime(200,200,10000))

# goto(200,200, gotoXYinTime(200,200,10000))

# placePen()

# for i in range(10):
    # speed = gotoXYinTime(400,400,i*500)
    # goto(400,400, 4000)
    # speed = gotoXYinTime(200,200,i*500)
    # line(200,200, 4000)
    # liftPen()
    # line(random.randint(0,100),random.randint(0,100))


# line(50,100,gotoXYinTime(50,100,10000))
# # goto(0,0)
# # line(0,60)
# # goto(0,0)
# # line(60,60)
# # goto(0,0)
# # liftPen()  
# # goto(340,-140)
# # goto(340,140)
# # goto(0,140)
# # goto(0,0)
# rectangle(100,140)
# liftPen()
# goto(0,0)
# ser.close()

async def loop():
    """Example main loop that only runs for 10 iterations before finishing"""
    for i in range(10):
        print(f"Loop {i}")
        await asyncio.sleep(1)
    while True:
        await asyncio.sleep(1)
        print("waiting for cvommands")
        

## init OSC
dispatcher = Dispatcher()
dispatcher.map("/pltcmd", oscword)
oscqueue = Queue()
  
        
async def main():
    global oscqueue, votes
    global midiin
    midiin.set_callback(MidiInputHandler(port_name))
    print("midi callback enabled")
    loadData()
    oscdaemon = Thread(target=asyncio.run , args=(oscPLT(oscqueue),), daemon=True, name='oscPLT')
    oscdaemon.start()
    
    try:
        # print("initializing osc client")
        # oscserver = AsyncIOOSCUDPServer((oscip, oscport), dispatcher, asyncio.get_event_loop())
        # transport, protocol = await oscserver.create_serve_endpoint()  # Create datagram endpoint and start serving
        await loop()
        # transport.close() 
        
    except KeyboardInterrupt:
        print('killed by keyboard')
        transport.close()
    finally:
        print("closing") 
        midiin.close_port()
        del midiin

if __name__ == "__main__":
    asyncio.run(main())
