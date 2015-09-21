class PID:
    def __init__(self, P=2.0, I=0.5, D=0.0, max_value=600, min_value=0, integrator_max=5000, integrator_min=0,
                 start_derivator=0, start_integrator=0):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.prev_derivator = start_derivator
        self.integrator = start_integrator
        self.integrator_max = integrator_max
        self.integrator_min = integrator_min
        self.max_value = max_value
        self.min_value = min_value

        self.set_point = 0.0
        self.error = 0.0

    def update(self, current_value):
        self.error = self.set_point - current_value

        self.P_value = self.Kp * self.error
        self.D_value = self.Kd * (self.error - self.prev_derivator)
        self.prev_derivator = self.error

        self.integrator = self.integrator + self.error

        if self.integrator > self.integrator_max:
            self.integrator = self.integrator_max
        elif self.integrator < self.integrator_min:
            self.integrator = self.integrator_min

        self.I_value = self.Ki * self.integrator

        ret_value = self.P_value + self.I_value + self.D_value

        if ret_value > self.max_value:
            ret_value = self.max_value;
        elif ret_value < self.min_value:
            ret_value = self.min_value

        return ret_value

    def setPoint(self, set_point):
        self.set_point = set_point
        self.integrator = 0
        self.prev_derivator = 0