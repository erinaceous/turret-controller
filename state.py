"""
    state.py: Store turret state
"""


class State(object):
    def __init__(self):
        self.target_x = 0.5
        self.target_y = 0.5
        self.fire = False
        self.scanning = False
        self.mode = 1
        self.tracking = False