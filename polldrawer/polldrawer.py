from grbl_streamer import GrblStreamer
import pickle
import asyncio
from threading import Event
from threading import Thread
from rtmidi.midiutil import open_midiinput, list_input_ports
import rtmidi
import mido
import os
import logging

log = logging.getLogger(__name__)


# if grbl.
config = {
    "pagex": 775,
    "pagey":1760,
    "startx" : 9, 
    "starty" : 9, 
    "startspeed" : 1000,
    "turfsperline" : 100,
    "turfwidth" : 10,
    "turfheight" : 40,
    "turfspace": 20,
    "turfy": 210,
    "farmx" : 210,
    "housex" : 320,
    "woodsx" : 430,
    "artx": 540,
    "shopx" : 650 
}

state = {
    "toolhead": "init"
}



def goto(x,y, speed=1000):
    '''
        go to absolute location
    '''
    grbl.job_new()
    grbl.poll_start()
    gcode = "G90 \n G0 X%d Y%d F%d" %(x,y,speed )
    print(gcode)
    grbl.write(gcode)
    print("starting command")
    grbl.job_run()

def line(x,y,speed=1000):
    '''
    move toolhead with pen down from current pos to abs x, y
    '''
    grbl.job_new()
    grbl.poll_start()
    gcode='''
    G90 ; absolute coordinates
    G21 Z1 F1000;
    G1 X{x} Y{y} F{speed};
    G21 Z-1 F1000;
    '''.format(x=x, y=y, speed=speed )
    grbl.write(gcode)
    print("starting line command", gcode)
    grbl.job_run()

## drawingfunctions

def turf(vote):
    global config, state, votes
    # first add vote to db
    votes[vote] += 1
    # calculate position
    if vote == "farm":
        xpos = config["farmx"] + (config["turfheight"]+config["turfspace"])*(votes["farm"]//config["turfsperline"]) 
    if vote == "house":
        xpos = config["housex"] + (config["turfheight"]+config["turfspace"])*(votes["house"]//config["turfsperline"]) 
    if vote == "woods":
        xpos = config["woodsx"] + (config["turfheight"]+config["turfspace"])*(votes["woods"]//config["turfsperline"]) 
    if vote == "art":
        xpos = config["artx"] + (config["turfheight"]+config["turfspace"])*(votes["art"]//config["turfsperline"]) 
    if vote == "shop":
        xpos = config["shopx"] + (config["turfheight"]+config["turfspace"])*(votes["shop"]//config["turfsperline"]) 

    # xpos = voteconfig["turfwidth"] * votes[vote]%voteconfig["turfsperline"] 

    ypos = config["turfy"] + config["turfwidth"]*(votes["farm"]%config["turfsperline"])

    if votes[vote]%5 == 0: 
        # linetype = "slant"
        ypos -= 4.8*config["turfwidth"]
        xpos += 1*config["turfheight"]/5
        ypos2 = ypos+4.7*config["turfwidth"]
        xpos2 = xpos+3*config["turfheight"]/5
    else:
        # linetype = straight
        xpos2 = xpos + config["turfheight"]
        ypos2 = ypos
    print("about to go", xpos, ypos, xpos2, ypos2)
    goto(xpos,ypos, 1000)
    line(xpos2, ypos2, 1000)
    goto(config["startx"], config("starty"), 1000)




def my_callback(eventstring, *data):
    args = []
    for d in data:
        args.append(str(d))
    # print("MY CALLBACK: event={} data={}".format(eventstring.ljust(30), ", ".join(args)))

    # if eventstring == "on_job_completed":
    #     print("a job well done")

    # if eventstring == "on_stateupdate":
    #     print(data)

    if  eventstring == "on_standstill":
        print(grbl.cmpos)
        print("stopped")
        if grbl.cmpos[0] != config["startx"] or grbl.cmpos[1] != config["starty"]:
            print("going to startpos")
            goto (config["startx"], config["starty"],config["startspeed"] )
        else:
            print("at startpos, ready for events")
            # if (state["toolhead"] == "turving"):
                # state["toolhead"] = "ready"
            votes["status"] = "done"
            save_object(votes, "votes.pickle")

def jobdone():
    print("fucking did it")

# machine is homed now..

# define machine functions



### init the machine

grbl = GrblStreamer(my_callback)

grbl._callback("on_job_complete", jobdone())
grbl.setup_logging()
grbl.cnect("/dev/ttyUSB0", 115200)
grbl.poll_start()

print("ABOUT TO START HOMING")
grbl.killalarm()
grbl.homing()



print("going to start position")
goto(config["startx"], config["starty"], config["startspeed"])




# /// voting state stuff

votes = {}

def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

# save_object(votes,"votes.pickle")

def loadData():
    global votes
    print("loading data")
    with open("votes.pickle", 'rb') as inp:
        votes = pickle.load(inp)
        # votes = {'farm': 0, 'house': 0, 'woods': 0, 'art': 0, 'shop': 0, 'status': 'done'}
        # save_object(votes, "votes.pickle")

        print(votes)



# /// first get midi up and running


def get_api_from_environment(api=rtmidi.API_UNSPECIFIED):
    """Return RtMidi API specified in the environment if any.

    If the optional api argument is ``rtmidi.API_UNSPECIFIED`` (the default),
    look in the environment variable ``RTMIDI_API`` for the name of the RtMidi
    API to use. Valid names are ``LINUX_ALSA``, ``UNIX_JACK``, ``MACOSX_CORE``,
    ``WINDOWS_MM`` and ``RTMIDI_DUMMY``. If no valid value is found,
    ``rtmidi.API_UNSPECIFIED`` will be used.

    Returns a ``rtmidi.API_*`` constant.

    """
    if api == rtmidi.API_UNSPECIFIED and 'RTMIDI_API' in os.environ:
        try:
            api_name = os.environ['RTMIDI_API'].upper()
            api = getattr(rtmidi, 'API_' + api_name)
        except AttributeError:
            log.warning("Ignoring unknown API '%s' in environment variable "
                        "RTMIDI_API." % api_name)

    return api

def available_inports_list(ports=None, midiio=None, api=rtmidi.API_UNSPECIFIED):
    """List MIDI ports given or available on given MIDI I/O instance."""
    midiin = rtmidi.MidiIn(get_api_from_environment(api))
    ports = midiin.get_ports()
    portsdict = {}
    if len(ports) > 0:
        # print("Available MIDI{} ports:\n".format(type_))
        for portno, name in enumerate(ports):
            print("[{}] {}".format(portno, name))
            portsdict[portno] = name
    else:
        print("No MIDI{} ports found.".format(type_))
    return portsdict

class MidiInputHandler(object):
    global ticks

    def __init__(self, port):
        self.port = port
        # self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        print(votes)
        # self._wallclock += deltatime
        # print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        
        # check if plotter is currently available

        # print(message[1])
        # print(message[2])
        if votes["status"] == "done":
            votes["status"] = "updating"
            if message[1] == 1 and message[2] == 127:
                vote = "farm"
            if message[1] == 2 and message[2] == 127:
                vote = "house"
            if message[1] == 3 and message[2] == 127:
                vote = "art"
            if message[1] == 4 and message[2] == 127:
                vote = "woods"
            if message[1] == 5 and message[2] == 127:
                vote = "shop"
            print(vote)
            turf(vote)
        else:
            print("wait till previous is done")
            print(votes)
        # parseMsg(event, deltatime)  ### needs to be rtmidi msg obj? not event?

    #         parseNote   On(message)


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








# start listening for midi event





async def loop():
    """Example main loop that only runs for 10 iterations before finishing"""
    # for i in range(10):
    #     print(f"Loop {i}")
    #     await asyncio.sleep(1)
    while True:
        
        await asyncio.sleep(1)
        # print("waiting for cvommands")
        

        
async def main():
    global votes
    global midiin
    loadData()
    midiin.set_callback(MidiInputHandler(port_name))
    print("midi callback enabled")
    votes["status"] = "done"
   
    try:
        await loop()

        
    except KeyboardInterrupt:
        print('killed by keyboard')
        transport.close()
    finally:
        print("closing") 
        midiin.close_port()
        del midiin

if __name__ == "__main__":
    asyncio.run(main())
