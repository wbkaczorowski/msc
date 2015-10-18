import RPi.GPIO as GPIO


class LED(object):
    RED_PIN = 23
    GREEN_PIN = 24
    BLUE_PIN = 25
    PWM_FREQ = 50  # in Hz

    def __init__(self):
        self.current_RGB = "000000"
        self.red = 0
        self.green = 0
        self.blue = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RED_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_PIN, GPIO.OUT)
        GPIO.setup(self.BLUE_PIN, GPIO.OUT)

        self.pwm_red = GPIO.PWM(self.RED_PIN, self.PWM_FREQ)
        self.pwm_green = GPIO.PWM(self.GREEN_PIN, self.PWM_FREQ)
        self.pwm_blue = GPIO.PWM(self.BLUE_PIN, self.PWM_FREQ)

        self.pwms = [self.pwm_red, self.pwm_green, self.pwm_blue]
        for pwm in self.pwms:
            pwm.start(0)


    def update_rgb(self, rgb_string_value):
        self.red = self.get_red_value(rgb_string_value)
        self.green = self.get_green_value(rgb_string_value)
        self.blue = self.get_blue_value(rgb_string_value)
        self.current_RGB = self.rgb_hex_string()
        self.update_red()
        self.update_green()
        self.update_blue()

    def stop(self):
        for pwm in self.pwms:
            pwm.stop()
        GPIO.cleanup()
        print "LEDs stoped"

    def update_all(self, single_value):
        self.red = single_value
        self.green = single_value
        self.blue = single_value
        self.current_RGB = self.rgb_hex_string()
        self.update_red()
        self.update_green()
        self.update_blue()

    def rgb_hex_string(self):
        return '{0:06x}'.format((self.red << 16) + (self.green << 8) + self.blue)

    # TODO te wartosci poprawic
    def update_red(self):
        # print "red: ", self.red
        # print "red: ", self.red*100.0/255.0
        self.pwm_red.ChangeDutyCycle(self.red * 100.0 / 255.0)

    def update_green(self):
        # print "green: ",  self.green
        # print "green: ",  self.green*100.0/255.0
        self.pwm_green.ChangeDutyCycle(self.green * 100.0 / 255.0)


    def update_blue(self):
        # print "blue: ",  self.blue
        # print "blue: ",  self.blue*100.0/255.0
        self.pwm_blue.ChangeDutyCycle(self.blue * 100.0 / 255.0)


    @staticmethod
    def get_red_value(data):
        return int(data[0:2], 16)


    @staticmethod
    def get_green_value(data):
        return int(data[2:4], 16)


    @staticmethod
    def get_blue_value(data):
        return int(data[4:6], 16)


class LEDModel(object):
    @staticmethod
    def get_lux(pwm):
        lux = 2.15 * pwm + 2.26
        return lux

    @staticmethod
    def get_pwm(lux):
        pwm = (lux - 2.26) / 2.15
        if pwm > 255:
            pwm = 255
        elif pwm < 0:
            pwm = 0
        return int(pwm)

if __name__ == "__main__":

    print '{0:06x}'.format((0 << 16) + (12 << 8) + 255)

    print 10*100.0/255.0

    # print(LEDModel.getLux(13.0))
    # led = LED()
    # try:
    #     while True:
    #         try:
    #             value = int(raw_input('Input:'))
    #             led.update_all(value)
    #         except ValueError:
    #             print "Not a number"
    # finally:
    #     led.stop()