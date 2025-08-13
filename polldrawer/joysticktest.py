# from pyjoystick.sdl2 import Key, Joystick, run_event_loop

# def print_add(joy):
#     print('Added', joy)

# def print_remove(joy):
#     print('Removed', joy)

# def key_received(key):
#     print('Key:', key)

# run_event_loop(print_add, print_remove, key_received)


import pywinusb.hid as hid


def readData(data):
    #print(data)
    print("Raw data: {0}".format(data))
    return None

# VID and PID customization changes here...
filter = hid.HidDeviceFilter(vendor_id = 0x03eb, product_id = 0x2402)
hid_device = filter.get_devices()
device = hid_device[0]
device.open()
print(hid_device)

device.set_raw_data_handler(readData)