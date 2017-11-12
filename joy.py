"""
    joy.py: Read X, Y and fire button from joystick
"""
import threading
import inputs


class Joy(threading.Thread):
    def __init__(
            self, input_ID=0, min_x=0, max_x=1024.0, min_y=0, max_y=1024.0,
            x_code='ABS_X', y_code='ABS_Y', trigger_code='BTN_TRIGGER'
    ):
        super(Joy, self).__init__()
        self.input = inputs.devices.gamepads[input_ID]
        self.x = 0.5
        self.y = 0.5
        self.fire = False
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.x_code = x_code
        self.y_code = y_code
        self.trigger_code = trigger_code
        self.daemon = True

    def scale(
            self, val, input_min, input_max, output_min=0.0, output_max=1.0
    ):
        val = float(val)
        return (
            (output_max - output_min)
            * (val - input_min)
            / (input_max - input_min)
        ) + output_min

    def run(self):
        while True:
            for event in self.input.read():
                if event.code == self.x_code:
                    self.x = self.scale(event.state, self.min_x, self.max_x)
                elif event.code == self.y_code:
                    self.y = self.scale(event.state, self.min_y, self.max_y)
                elif event.code == self.trigger_code:
                    self.fire = event.state