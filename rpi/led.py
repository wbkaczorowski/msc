import RPi.GPIO as GPIO
import math


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

    def update_rgb_tuple(self, rgb_tuple):
        self.red = int(rgb_tuple[0])
        self.green = int(rgb_tuple[1])
        self.blue = int(rgb_tuple[2])
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

    def update_value_red(self, new_val):
        self.red = new_val
        self.current_RGB = self.rgb_hex_string()
        self.update_red()

    def update_value_green(self, new_val):
        self.green = new_val
        self.current_RGB = self.rgb_hex_string()
        self.update_green()

    def update_value_blue(self, new_val):
        self.blue = new_val
        self.current_RGB = self.rgb_hex_string()
        self.update_blue()

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
        '''
        :param pwm range 0-255:
        :return lux in range  0-550:
        '''
        lux = 2.15 * pwm + 2.26
        return lux

    @staticmethod
    def get_pwm(lux):
        '''
        :param lux:
        :return pwm in range 0-255:
        '''
        pwm = (lux - 2.26) / 2.15
        if pwm > 255:
            pwm = 255
        elif pwm < 0:
            pwm = 0
        return int(pwm)

    @staticmethod
    def get_red_lux(pwm):
        lux = 0.221 * pwm + 3.502
        return lux

    @staticmethod
    def get_green_lux(pwm):
        lux = 0.223 * pwm + 3.83
        return lux

    @staticmethod
    def get_blue_lux(pwm):
        lux = 0.271 * pwm + 7.081
        return lux

    @staticmethod
    def get_red_pwm(lux):
        pwm = (lux - 3.502) / 0.221
        if pwm > 255:
            pwm = 255
        elif pwm < 0:
            pwm = 0
        return int(pwm)

    @staticmethod
    def get_green_pwm(lux):
        pwm = (lux - 3.83) / 0.223
        if pwm > 255:
            pwm = 255
        elif pwm < 0:
            pwm = 0
        return int(pwm)

    @staticmethod
    def get_blue_pwm(lux):
        pwm = (lux - 7.081) / 0.271
        if pwm > 255:
            pwm = 255
        elif pwm < 0:
            pwm = 0
        return int(pwm)

class TempModel(object):
    @staticmethod
    def get_rgb(kelvin):
        temp = kelvin / 100.0;
        # calculating red
        if temp <= 66:
            red = 255
        else:
            red = temp - 60
            red = 329.698727446 * math.pow(red, -0.1332047592)
            if red < 0:
                red = 0
            elif red > 255:
                red = 255

        # calculating green
        if temp <= 66:
            green = temp
            green = 99.4708025861 * math.log(green) - 161.1195681661
        else:
            green = temp - 60
            green = 288.1221695283 * math.pow(green, -0.0755148492)
        if green < 0:
            green = 0
        elif green > 255:
            green = 255

        # calculating blue
        if temp >= 66:
            blue = 255
        else:
            if temp <= 19:
                blue = 0
            else:
                blue = temp - 10
                blue = 138.5177312231 * math.log(blue) - 305.0447927307
                if blue < 0:
                    blue = 0
                elif blue > 255:
                    blue = 255

        return red, green, blue


# testing purposes
if __name__ == "__main__":
    # print '{0:06x}'.format((0 << 16) + (12 << 8) + 255)

    # print 10*100.0/255.0

    print TempModel.get_rgb(6800)[0]
    print TempModel.get_rgb(6800)[2]


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
