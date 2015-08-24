from sensor_reader import SensorReader
from led import LEDController
from pid import PID
from database import Database
import time
import sys

MIN_VALUE = 0
MAX_VALUE = 600


class Controller(object):
    def __init__(self, sensor_reader, pid, led, database):
        self.sensor_reader = sensor_reader
        self.pid = pid
        self.led = led
        self.database = database

    def run(self):
        while True:
            try:
                measured_value = float(self.sensor_reader.read()[1])
                print "measured value : {0}".format(measured_value)
                pid_value = pid.update(measured_value)
                signal = self.process_siganl(pid_value)
                print "calculated values : {0}, {1}".format(pid_value, signal)
                self.led.update_all(signal)
                self.database.insert_into_control_table(measured_value, pid_value)
            except KeyboardInterrupt:
                print "Keyboard Interrupt!"
                exit()
            except:
                pass

    def process_siganl(self, set_value):
        normalised_value = (255.0/float(MAX_VALUE)) * set_value
        return normalised_value


    def test_cycle(self):
        i = 0
        while i < 255:
            try:
                self.led.update_all(i)
                time.sleep(0.23)
                read = self.sensor_reader.read()
                if read:
                    measured_value = float(read[1])
                    print "{0}, {1}".format(i, measured_value)
                    self.database.insert_into_control_table(measured_value, -666)
                    i = i + 1
            except:
                pass


# testing purposes
if __name__ == "__main__":
    sr = SensorReader('/dev/ttyUSB0', 115200)
    led = LEDController()
    database = Database()
    pid = PID(3.0, 0.5, 0.0, MAX_VALUE, MIN_VALUE)
    pid.setPoint(200.0)
    controller = Controller(sr, pid, led, database)
    try:
        if len(sys.argv) >= 2:
            controller.test_cycle()
        else:
            controller.run()

    finally:
        print "done"
        database.close_connection()
        led.stop()
        sr.close()
