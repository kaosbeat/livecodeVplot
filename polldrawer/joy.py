import pygame

pygame.init()


def main():
    joysticks = {}
    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.
            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.",event.button )
                if event.button == 0:
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(f"Rumble effect played on joystick {event.instance_id}")

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")



            buttons = joystick.get_numbuttons()
            # text_print.tprint(screen, f"Number of buttons: {buttons}")
            # text_print.indent()

            for i in range(buttons):
                button = joystick.get_button(i)
            #     text_print.tprint(screen, f"Button {i:>2} value: {button}")
            # text_print.unindent()



if __name__ == "__main__":
    main()
    pygame.quit()