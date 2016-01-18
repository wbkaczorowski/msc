from datetime import time
from sensor_reader import SensorReader
from led import LED, LEDModel, TempModel
from pid import PID
from database import Database
import time
import sys
import threading

MIN_VALUE = 0
MAX_VALUE = 550
CONST_TIME = 1.0
MANUAL = "manual"
AUTO = "automatic"

class Controller(object):
    def __init__(self, sensor_reader, led, database=None, file=None):
        self.sensor_reader = sensor_reader
        self.led = led
        self.database = database
        self.output_file = file

        self.pid = PID(0.495, 0.594, 0.0, MIN_VALUE, MAX_VALUE, 5)
        # self.pid = PID(2.0, 0.0, 0.0, MIN_VALUE, MAX_VALUE, 0)
        self.mode = MANUAL

    def _init_thread(self):
        self.automatic_mode_thread = threading.Thread(target=self.start_automatic)
        self.automatic_mode_thread.start()

    def start_automatic(self):
        start_time_ref = time.time()
        while self.mode == AUTO:
            try:
                start_time = time.time()
                # wait_time = 1.0
                # while wait_time > 0:
                #     wait_time = CONST_TIME + start_time - time.time()
                #     time.sleep(0.1)
                measured_value = int(self.sensor_reader.handle_reading(self.sensor_reader.readline())[1])
                pid_value = self.pid.update(measured_value)
                pwm_value = LEDModel.get_pwm(pid_value)
                output = "{0}, {1}, {2}, {3}".format(time.time() - start_time_ref, measured_value, pid_value, pwm_value)
                print output
                self.led.update_all(pwm_value)
                try:
                    self.output_file.write(output + "\n")
                    # self.database.insert_into_control_table(measured_value, pid_value)
                except:
                    # does not matter if saving exists
                    pass
            except Exception as e:
                print e
                # exception probably caused by reading, sleep to give some time to update
                time.sleep(0.1)
                pass


    def update_pid_point(self, point, test_mode=False):
        if test_mode:
            self.pid.set_point(point)
        else:
            self.pid.set_point(LEDModel.get_lux(point))
        if not self.mode == AUTO:
            self.mode = AUTO
            self._init_thread()


    def update_manual(self, rgb_value):
        if not self.mode == MANUAL:
            self.mode = MANUAL
            self.automatic_mode_thread.join()
        if self.mode == MANUAL:
            self.led.update_rgb(rgb_value)

    def update_temp(self, temp_value):
        rgb_tuple = TempModel.get_rgb(temp_value)
        # TODO te wartości ogarnąć
        # self.update_manual()


    def stop(self):
        self.mode = MANUAL
        if self.automatic_mode_thread.isAlive():
            self.automatic_mode_thread.join(0.01)

    # Identification methods
    def only_measure_thread(self, repeats):
        self.sensor_reader.start_reading()
        i = 0
        while i < repeats:
            try:
                # time.sleep(0.7)
                read = self.sensor_reader.get_last_read()
                if read:
                    measured_value = int(read[1])
                    output = "{0}, {1}".format(i, measured_value)
                    print output
                    self.output_file.write(output)
                    i = i + 1
            except:
                pass

    def single_measure(self, repeats):
        i = 0
        start_time = time.time()
        while i < repeats:
            try:
                measured_value = int(self.sensor_reader.handle_reading(self.sensor_reader.readline())[1])
                output = "{}, {}, {}".format(time.time() - start_time, i, measured_value)
                print output
                self.output_file.write(output + "\n")
                i = i + 1
            except Exception as e:
                print e
                pass

    def single_measure_led(self, repeats, led_value):
        self.led.update_all(led_value)
        i = 0
        start_time = time.time()
        while i < repeats:
            try:
                measured_value = int(self.sensor_reader.handle_reading(self.sensor_reader.readline())[1])
                output = "{}, {}, {}".format(time.time() - start_time, i, measured_value)
                print output
                self.output_file.write(output + "\n")
                i = i + 1
            except Exception as e:
                print e
                pass


    def single_loop(self):
        i = 0
        start_time = time.time()
        while i < 255:
            try:
                self.led.update_all(i)
                time.sleep(0.5)
                measured_value = int(self.sensor_reader.handle_reading(self.sensor_reader.readline())[1])
                output = "{}, {}, {}".format(time.time() - start_time, i, measured_value)
                print output
                self.output_file.write(output + "\n")
                i += 1
            except Exception as e:
                print e
                pass

    def stairs_loop(self):
        i = 0
        start_time = time.time()
        while i < 255:
            try:
                self.led.update_all(i)
                j = 0
                while j < 20:
                    measured_value = int(self.sensor_reader.handle_reading(self.sensor_reader.readline())[1])
                    output = "{}, {}, {}".format(time.time() - start_time, i, measured_value)
                    print output
                    self.output_file.write(output + "\n")
                    j += 1
                i += 20
            except Exception as e:
                print e
                pass

# testing purposes
if __name__ == "__main__":

    sr = SensorReader('/dev/ttyUSB0', 115200)
    # sr.start_reading()
    led = LED()
    out_file = open(time.strftime('%Y%m%d-%H%M%S') + ".csv", "w")
    database = Database("../rpi.db")
    controller = Controller(sr, led, file=out_file)
    try:
        if len(sys.argv) >= 2:
            for arg in sys.argv:
                if arg == "single_loop":
                    print "single loop option selected"
                    controller.single_loop()
                elif arg == "single":
                    print "measure on single thread selected"
                    controller.single_measure(100)
                elif arg == "stairs":
                    print "measure on single thread selected"
                    controller.stairs_loop()
                elif arg == "single_led":
                    print "measure on single thread selected"
                    controller.single_measure_led(100, 255)
        else:
            controller.update_pid_point(300, True)
            # somehow this works
            while True:
                time.sleep(100)
    finally:
        print "done"
        out_file.close()
        controller.stop()
        database.close_connection()
        led.stop()
        sr.close()
        print "all closed"
