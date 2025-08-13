import numpy as np

class DTW:
    """
    Dynamic Time-based Windowing (DTW) adjusts the observation window size
    based on Mean Decline Ratio (MDR) of entropy measurements.
    """

    def __init__(self, theta_min, theta_max, min_window, max_window, delta):
        self.theta_min = theta_min
        self.theta_max = theta_max
        self.min_window = min_window
        self.max_window = max_window
        self.delta = delta
        self.current_window = min_window

    def adjust_window(self, mdr_change):
        """
        Adjusts the window size according to MDR thresholds:
        - Increase if ΔMDR < θ_min (traffic appears stable)
        - Decrease if ΔMDR > θ_max (possible attack or sudden change)
        """
        if mdr_change < self.theta_min:
            self.current_window = min(self.max_window, self.current_window + self.delta)
        elif mdr_change > self.theta_max:
            self.current_window = max(self.min_window, self.current_window - self.delta)
        return self.current_window
