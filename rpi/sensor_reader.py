import serial
import threading
import sys
import time

class SensorReader(object):
    def __init__(self, device_port, baudrate):
        self.srl = serial.Serial(device_port, baudrate, timeout=0.5)
        self.last_read = [0, 0]
        self.read_flag = False
        self.srl.flushInput()
        sys.stdout.write("Flushing the serial port:")
        endtime = time.time() + 1
        while time.time() < endtime:
            self.srl.read()
            sys.stdout.write(".")
        sys.stdout.write("\n")
        self.srl.close()
        self.srl = serial.Serial(device_port, baudrate)

    def read(self):
        while self.read_flag:
            try:
                state = self.srl.readline()
                self.last_read = self.handle_reading(state)
            except:
                pass

    def start_reading(self):
        self.read_flag = True
        self.t = threading.Thread(target=self.read)
        self.t.daemon = True
        self.t.start()

    def stop_reading(self):
        self.read_flag = False
        try:
            if self.t.isAlive():
                self.t.join()
        except:
            # do nothing, if there was no thread no need to end it
            pass

    def readline(self):
        """
        Waits for read from serial.
        :return:
        """
        return self.srl.readline()

    def get_last_read(self):
        """
        :return: last read that was measured
        """
        return self.last_read

    def handle_reading(self, state):
        splited = state.strip().split(':')
        if len(splited) == 2 and splited[0].isdigit() and splited[1].isdigit():
            return splited

    def close(self):
        self.stop_reading()
        self.srl.close()


# testing purposes
if __name__ == "__main__":
    sr = SensorReader('/dev/tty.usbserial-MFU7XGR7', 115200)
    # sr.start_reading()
    try:
        while True:
            print(sr.readline())
    except KeyboardInterrupt:
        print "done"
    finally:
        sr.close()
