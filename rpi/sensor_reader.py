import serial


class SensorReader(object):
    def __init__(self, device_port, baudrate):
        self.ser = serial.Serial(device_port, baudrate)
        # self.ser.setTimeout(1)

    def read(self):
        try:
            state = self.ser.readline()
            return self.handle_reading(state)
        except:
            pass

    def handle_reading(self, state):
        splitted = state.strip().split(':')
        if len(splitted) == 2 and splitted[0].isdigit() and splitted[1].isdigit():
            return splitted

    def close(self):
        self.ser.close()


# testing purposes
if __name__ == "__main__":
    sr = SensorReader('/dev/ttyUSB0', 115200)
    try:
        while True:
            value = sr.read()
            if value:
                print(value)
    except KeyboardInterrupt:
        print "done"
    finally:
        sr.close()
