import math


class PID:
    def __init__(self, P=2.0, I=0.0, D=0.0, min_out=0, max_out=10000, tolerance=0.0):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.max_out = max_out
        self.min_out = min_out
        self.tolerance = tolerance

        self.point = 0.0
        self.error = 0.0
        self.error_total = 0.0
        self.error_prev = 0.0
        self.result = 0.0

    def update(self, current_value):
        self.error = self.point - current_value

        if math.fabs(self.error) >= self.tolerance:
            if self.max_out > (self.error_total + self.error) * self.Ki > self.min_out:
                self.error_total += self.error

            self.result = self.Kp * self.error + self.Ki * self.error_total + self.Kd * (
                self.error - self.error_prev)

            self.error_prev = self.error
            # set bounds
            if self.result > self.max_out:
                self.result = self.max_out
            elif self.result < self.min_out:
                self.result = self.min_out

        return self.result

    def set_point(self, set_point):
        if self.point != set_point:
            self.point = set_point
            self.error = 0.0
            self.error_total = 0.0
            self.error_prev = 0.0
            self.result = 0.0

