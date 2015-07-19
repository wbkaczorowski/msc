from sensor_reader import SensorReader
# from led import LEDController
from pid import PID
from database import Database

MIN_VALUE = 0
MAX_VALUE = 5500


class Controller(object):
    def __init__(self, sensor_reader, pid):
        self.sensor_reader = sensor_reader
        self.pid = pid


    def run(self):
        while True:
            try:
                measured_value = float(self.sensor_reader.read()[1])
                print "measured value : {0}".format(measured_value)
                pid_value = pid.update(measured_value)
                print "pid value : {0}".format(pid_value)
                database.insert_into_control_table(measured_value, pid_value)
            except:
                pass


# testing purposes
if __name__ == "__main__":
    sr = SensorReader('/dev/ttyUSB0', 115200)
    # led = LEDController()
    database = Database()
    pid = PID(3.0, 0.4, 0.0, MAX_VALUE, MIN_VALUE)
    pid.setPoint(500.0)
    controller = Controller(sr, pid)
    try:
        controller.run()
    except:
        database.close_connection()