from sensor_reader import SensorReader
from led import LED, LEDModel
from pid import PID
from database import Database
import time
import sys
import signal
import threading

MIN_VALUE = 0
MAX_VALUE = 650
CONST_TIME = 1.0
MANUAL = "manual"
AUTO = "automatic"

class Controller(object):
    def __init__(self, sensor_reader, led, database=None):
        self.sensor_reader = sensor_reader
        self.led = led
        self.database = database

        self.pid = PID(0.675, 0.405, 0.0, MIN_VALUE, MAX_VALUE, 20)
        self.mode = MANUAL

    def _init_thread(self):
        self.automatic_mode_thread = threading.Thread(target=self.start_automatic)
        self.automatic_mode_thread.start()

    def start_automatic(self):
        start_time_ref = time.time()
        while self.mode == AUTO:
            try:
                start_time = time.time()
                wait_time = 1.0
                while wait_time > 0:
                    wait_time = CONST_TIME + start_time - time.time()
                    time.sleep(0.1)
                    measured_value = int(self.sensor_reader.get_last_read()[1])
                pid_value = self.pid.update(measured_value)
                pwm_value = LEDModel.get_pwm(pid_value)
                print "{0}, {1}, {2}, {3}".format(time.time() - start_time_ref, measured_value, pid_value, pwm_value)
                self.led.update_all(pwm_value)
                # self.database.insert_into_control_table(measured_value, pid_value)
            except Exception as e:
                print e
                # exception probably caused by reading, sleep to give some time to update
                time.sleep(0.1)
                pass


    def update_pid_point(self, point):
        self.pid.set_point(LEDModel.get_lux(point * 2.55))
        print "point: {0}".format(self.pid.point)
        if not self.mode == AUTO:
            self.mode = AUTO
            self._init_thread()


    def update_manual(self, rgb_value):
        if not self.mode == MANUAL:
            self.mode = MANUAL
            self.automatic_mode_thread.join()
        if self.mode == MANUAL:
            self.led.update_rgb(rgb_value)

    def test_cycle(self):
        i = 0
        while i < 255:
            try:
                self.led.update_all(i)
                time.sleep(0.7)
                read = self.sensor_reader.getLastRead()
                if read:
                    measured_value = int(read[1])
                    print "{0}, {1}".format(i, measured_value)
                    self.database.insert_into_control_table(measured_value, -666)
                    i = i + 1
            except:
                pass


def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)
    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)
    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)
    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)




# testing purposes
if __name__ == "__main__":

    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    sr = SensorReader('/dev/ttyUSB0', 115200)
    sr.start_reading()
    led = LED()
    database = Database("../rpi.db")
    pid = PID(0.675, 0.405, 0.0, MIN_VALUE, MAX_VALUE, 20)
    controller = Controller(sr, pid, led, database)
    try:
        if len(sys.argv) >= 2:
            controller.test_cycle()
        else:
            controller.update_pid_point(300.0)
            controller.start_automatic()

    finally:
        print "done"
        database.close_connection()
        led.stop()
        sr.close()
