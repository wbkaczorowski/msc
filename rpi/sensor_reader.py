import serial


class SensorReader(object):
    def __init__(self, device_port, baudrate):
        self.ser = serial.Serial(device_port, baudrate)


    def read(self):
        try:
            state = self.ser.readline()
            return self.handle_reading(state)
        except:
            pass


    def handle_reading(self, state):
        splitted = state.strip().split(':')
        print(splitted)
        return splitted


# testing purposes
if __name__ == "__main__":
    sr = SensorReader('/dev/ttyUSB0', 115200)
    sr.read()