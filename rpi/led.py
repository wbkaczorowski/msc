# from RPIO import PWM


class LEDController(object):
    RED_PIN = 23
    GREEN_PIN = 24
    BLUE_PIN = 25

    def __init__(self):
        self.current_RGB = "ffaacc"
        self.red = 0
        self.green = 0
        self.blue = 0
        # self.servo = PWM.Servo()


    def update_rgb(self, rgb_string_value):
        self.red = self.get_red_value(rgb_string_value)
        self.green = self.get_green_value(rgb_string_value)
        self.blue = self.get_blue_value(rgb_string_value)
        self.current_RGB = self.rgb_hex_string()

        self.update_red()
        self.update_green()
        self.update_blue()

    def stop(self):
        # self.servo.stop_servo(self.RED_PIN)
        # self.servo.stop_servo(self.GREEN_PIN)
        # self.servo.stop_servo(self.BLUE_PIN)
        print "LEDs stoped"


    def rgb_hex_string(self):
        return '%x' % self.red + '%x' % self.green + '%x' % self.blue

    # TODO te wartosci poprawic
    def update_red(self):
        # self.servo.set_servo(self.RED_PIN, round(self.red * 78, -1))
        print "red: ", round(self.red * 78, -1)

    def update_green(self):
        # self.servo.set_servo(self.GREEN_PIN, round(self.green * 78, -1))
        print "green: ",  round(self.green * 78, -1)

    def update_blue(self):
        # self.servo.set_servo(self.BLUE_PIN, round(self.blue * 78, -1))
        print "blue: ", round(self.blue * 78, -1)


    # TODO sprawdzic czy dobrze zczytuje miejsca w stringu
    @staticmethod
    def get_red_value(data):
        return int(data[0:2], 16)


    @staticmethod
    def get_green_value(data):
        return int(data[2:4], 16)


    @staticmethod
    def get_blue_value(data):
        return int(data[4:6], 16)