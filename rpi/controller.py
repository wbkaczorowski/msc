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
AUTO_3 = "three channel"

MOTES_COLOR = {4: 'red', 6: 'green', 7: 'blue'}


class Controller(object):
    def __init__(self, sensor_reader, led, database=None, file=None):
        self.sensor_reader = sensor_reader
        self.led = led
        self.database = database
        self.output_file = file

        self.pid = PID(0.495, 0.594, 0.0, MIN_VALUE, MAX_VALUE, 0)

        self.red_pid = PID(0.495, 0.594, 0.0, MIN_VALUE, 65, 0)
        self.green_pid = PID(0.495, 0.594, 0.0, MIN_VALUE, 80, 0)
        self.blue_pid = PID(0.495, 0.594, 0.0, MIN_VALUE, 70, 0)

        # self.pid = PID(2.0, 0.0, 0.0, MIN_VALUE, MAX_VALUE, 0)
        self.last_reads = {}
        self.mode = MANUAL

    def _init_thread(self):
        self.automatic_mode_thread = threading.Thread(target=self.start_automatic)
        self.automatic_mode_thread.start()

    def _init_three_thread(self):
        self.automatic_mode_three_thread = threading.Thread(target=self.start_three_channel)
        self.automatic_mode_three_thread.start()

    def _init_read_thread(self):
        self.read_thread = threading.Thread(target=self.start_read_thread)
        self.read_thread.start()

    def start_automatic(self):
        start_time_ref = time.time()
        while self.mode == AUTO:
            try:
                # start_time = time.time()
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

    def start_three_channel(self):
        start_time_ref = time.time()
        while self.mode == AUTO_3:
            try:
                read_packet = self.sensor_reader.handle_reading(self.sensor_reader.readline());
                # print MOTES_COLOR[int(read_packet[0])] + " : " + read_packet[1]

                key = MOTES_COLOR[int(read_packet[0])]
                if key == 'red':
                    red_pid_value = self.red_pid.update(int(read_packet[1]))
                    red_pwm_value = LEDModel.get_red_pwm(red_pid_value)
                    red_output = "{0}: {1}, {2}, {3}, {4}".format(key,
                                                              time.time() - start_time_ref, int(read_packet[1]),
                                                              red_pid_value,
                                                              red_pwm_value)
                    print red_output
                    self.led.update_value_red(red_pwm_value)
                    try:
                        self.output_file.write(red_output + "\n")
                        # self.database.insert_into_control_table(measured_value, pid_value)
                    except:
                        # does not matter if saving exists
                        pass
                elif key == 'green':
                    green_pid_value = self.green_pid.update(int(read_packet[1]))
                    green_pwm_value = LEDModel.get_green_pwm(green_pid_value)
                    green_output = "{0}: {1}, {2}, {3}, {4}".format(key,
                                                              time.time() - start_time_ref, int(read_packet[1]),
                                                              green_pid_value,
                                                              green_pwm_value)
                    print green_output
                    self.led.update_value_green(green_pwm_value)
                    try:
                        self.output_file.write(green_output + "\n")
                        # self.database.insert_into_control_table(measured_value, pid_value)
                    except:
                        # does not matter if saving exists
                        pass
                elif key == 'blue':
                    blue_pid_value = self.blue_pid.update(int(read_packet[1]))
                    blue_pwm_value = LEDModel.get_blue_pwm(blue_pid_value)
                    blue_output = "{0}: {1}, {2}, {3}, {4}".format(key,
                                                              time.time() - start_time_ref, int(read_packet[1]),
                                                              blue_pid_value,
                                                              blue_pwm_value)
                    print blue_output
                    self.led.update_value_blue(blue_pwm_value)
                    try:
                        self.output_file.write(blue_output + "\n")
                        # self.database.insert_into_control_table(measured_value, pid_value)
                    except:
                        # does not matter if saving exists
                        pass
            except Exception as e:
                print e
                # exception probably caused by reading, sleep to give some time to update
                # time.sleep(0.1)
                pass

    def start_read_thread(self):
        while self.mode == MANUAL:
            try:
                read_packet = self.sensor_reader.handle_reading(self.sensor_reader.readline())
                self.last_reads[read_packet[0]] = read_packet[1]
                print self.last_reads
            except Exception as e:
                # print e
                pass


    def update_rgb_pid_point(self, red, green, blue, test_mode=False):
        if test_mode:
            if red is not None:
                self.red_pid.set_point(red)
            if green is not None:
                self.green_pid.set_point(green)
            if blue is not None:
                self.blue_pid.set_point(blue)
        else:
            if red is not None:
                self.red_pid.set_point(LEDModel.get_red_lux(red))
            if green is not None:
                self.green_pid.set_point(LEDModel.get_green_lux(green))
            if blue is not None:
                self.blue_pid.set_point(LEDModel.get_blue_lux(blue))
        self.do_three_thread_init()

    def update_red_pid_point(self, red_point, test_mode=False):
        if test_mode:
            self.red_pid.set_point(red_point)
        else:
            self.red_pid.set_point(LEDModel.get_red_lux(red_point))
        self.do_three_thread_init()

    def update_green_pid_point(self, green_point, test_mode=False):
        if test_mode:
            self.green_pid.set_point(green_point)
        else:
            self.green_pid.set_point(LEDModel.get_green_lux(green_point))
        self.do_three_thread_init()

    def update_blue_pid_point(self, blue_point, test_mode=False):
        if test_mode:
            self.blue_pid.set_point(blue_point)
        else:
            self.blue_pid.set_point(LEDModel.get_blue_lux(blue_point))
        self.do_three_thread_init()

    def do_three_thread_init(self):
        try:
            if self.read_thread is not None and self.read_thread.isAlive():
                self.read_thread.join(0.01)
        except Exception as e:
            print e
            pass
        if self.mode == AUTO:
            self.automatic_mode_thread.join()
        if not self.mode == AUTO_3:
            self.mode = AUTO_3
            self._init_three_thread()

    def update_pid_point(self, point, test_mode=False):
        try:
            if self.read_thread is not None and self.read_thread.isAlive():
                self.read_thread.join(0.01)
        except Exception as e:
            print e
            pass
        if test_mode:
            self.pid.set_point(point)
        else:
            self.pid.set_point(LEDModel.get_lux(point))
        if self.mode == AUTO_3:
            self.automatic_mode_three_thread.join()
        if not self.mode == AUTO:
            self.mode = AUTO
            self._init_thread()

    def update_manual(self, rgb_value):
        if not self.mode == MANUAL:
            self.mode = MANUAL
            self.automatic_mode_thread.join()
        if self.mode == AUTO_3:
            self.mode = MANUAL
            self.automatic_mode_three_thread.join()
        if self.mode == MANUAL:
            self.led.update_rgb(rgb_value)
            if self.read_thread is None or not self.read_thread.isAlive():
                self._init_read_thread()



    def update_temp(self, temp_value):
        rgb_tuple = TempModel.get_rgb(temp_value)
        if not self.mode == MANUAL:
            self.mode = MANUAL
            self.automatic_mode_thread.join()
        if self.mode == AUTO_3:
            self.automatic_mode_three_thread.join()
        if self.mode == MANUAL:
            self.led.update_rgb_tuple(rgb_tuple)
            if self.read_thread is None or not self.read_thread.isAlive():
                self._init_read_thread()

    def stop(self):
        self.mode = MANUAL
        try:
            if self.automatic_mode_thread is not None and self.automatic_mode_thread.isAlive():
                self.automatic_mode_thread.join(0.01)
        except Exception as e:
            print e
            pass
        try:
            if self.automatic_mode_three_thread is not None and self.automatic_mode_three_thread.isAlive():
                self.automatic_mode_three_thread.join(0.01)
        except Exception as e:
            print e
            pass
        try:
            if self.read_thread is not None and self.read_thread.isAlive():
                self.read_thread.join(0.01)
        except Exception as e:
            print e
            pass

    def get_temp_rgb_lux(self, temp):
        tup = TempModel.get_rgb(temp)
        red = LEDModel.get_red_lux(tup[0])
        green = LEDModel.get_green_lux(tup[1])
        blue = LEDModel.get_blue_lux(tup[2])
        return red, green, blue
    #
    #
    # Identification methods
    #
    #
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
                # time.sleep(0.5)
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

    def stairs_colors(self):
        i = 0
        self.led.update_all(0);
        start_time = time.time()
        print "Start iterating..."
        while i < 255:
            try:
                self.led.update_rgb_tuple((i, 0, 0))
                # time.sleep(0.5)
                measured_value = int(self.sensor_reader.handle_reading(self.sensor_reader.readline())[1])
                output = "{}, {}, {}".format(time.time() - start_time, i, measured_value)
                print output
                self.output_file.write(output + "\n")
                i += 1
            except Exception as e:
                print e
                pass
        i = 0
        while i < 255:
            try:
                self.led.update_rgb_tuple((0, i, 0))
                # time.sleep(0.5)
                measured_value = int(self.sensor_reader.handle_reading(self.sensor_reader.readline())[1])
                output = "{}, {}, {}".format(time.time() - start_time, i, measured_value)
                print output
                self.output_file.write(output + "\n")
                i += 1
            except Exception as e:
                print e
                pass
        i = 0
        while i < 255:
            try:
                self.led.update_rgb_tuple((0, 0, i))
                # time.sleep(0.5)
                measured_value = int(self.sensor_reader.handle_reading(self.sensor_reader.readline())[1])
                output = "{}, {}, {}".format(time.time() - start_time, i, measured_value)
                print output
                self.output_file.write(output + "\n")
                i += 1
            except Exception as e:
                print e
                pass


# testing purposes
if __name__ == "__main__":

    # rpi
    sr = SensorReader('/dev/ttyUSB0', 115200)

    # red/4
    # sr = SensorReader('/dev/tty.usbserial-MFU7XGR7', 115200)

    # blue/7
    # sr = SensorReader('/dev/tty.usbserial-MFUD5O75', 115200)
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
                elif arg == "colors":
                    print "colors stairs mode"
                    controller.stairs_colors()
                elif arg == "3":
                    print "3 channel pid model"
                    # TODO pid 3 channel
        else:
            print "starting 3 channel pid"
            # rgb_tuple = controller.get_temp_rgb_lux(6000)
            # controller.update_rgb_pid_point(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2], test_mode=True)
            controller.update_red_pid_point(30, True)
            controller.update_green_pid_point(8, True)
            controller.update_blue_pid_point(30, True)
            # controller.update_pid_point(80, True)

            # somehow this works
            while True:
                print "sleep"
                time.sleep(100)
    except Exception as e:
        print e
    finally:
        print "done"
        out_file.close()
        controller.stop()
        database.close_connection()
        led.stop()
        sr.close()
        print "all closed"
