import serial
import threading
import time

class SensorReader(object):
    def __init__(self, device_port, baudrate):
        self.ser = serial.Serial(device_port, baudrate)
        self.last_read = []
        self.t = threading.Thread(target=self.read)
        self.t.daemon = True

    def read(self):
        self.ser.flushInput()
        while True:
            try:
                state = self.ser.readline()
                self.last_read = self.handle_reading(state)
            except:
                pass

    def start_reading(self):
        self.t.start()

    def get_last_read(self):
        return self.last_read

    def handle_reading(self, state):
        splitted = state.strip().split(':')
        if len(splitted) == 2 and splitted[0].isdigit() and splitted[1].isdigit():
            return splitted

    def close(self):
        self.ser.close()


# testing purposes
if __name__ == "__main__":
    sr = SensorReader('/dev/tty.usbserial-MFU7XCA3', 115200)
    sr.start_reading()
    try:
        while True:
            print(sr.get_last_read())
            time.sleep(0.5)
    except KeyboardInterrupt:
        print "done"
    finally:
        sr.close()
