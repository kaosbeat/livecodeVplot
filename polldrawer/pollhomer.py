from grbl_streamer import GrblStreamer


def my_callback(eventstring, *data):
    args = []
    for d in data:
        args.append(str(d))
    print("MY CALLBACK: event={} data={}".format(eventstring.ljust(30), ", ".join(args)))



### init the machine

grbl = GrblStreamer(my_callback)
grbl.setup_logging()
grbl.cnect("/dev/ttyUSB0", 115200)
grbl.poll_start()

print("ABOUT TO START HOMING")
# grbl.killalarm()
grbl.homing()
