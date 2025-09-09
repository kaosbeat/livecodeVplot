# import virtualserialports
# from pyvirtualserial import VirtualSerial

# virtualserialports.run(1, loopback=True, debug=False)


# virtual_serial = VirtualSerial(timeout=60)

# while True:
#     b = virtual_serial.read(1)
#     virtual_serial.write("ok")


from pyvirtualserial import VirtualSerial

virtual_serial = VirtualSerial(timeout=60)
while True:
    b = virtual_serial.read(1)
    virtual_serial.write(b)
