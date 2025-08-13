import unittest
from src.dtw import DTW

class TestDTW(unittest.TestCase):

    def test_increase_window(self):
        dtw = DTW(theta_min=0.2, theta_max=0.8, min_window=5, max_window=20, delta=2)
        dtw.current_window = 5
        new_window = dtw.adjust_window(0.1)
        self.assertEqual(new_window, 7)

    def test_decrease_window(self):
        dtw = DTW(theta_min=0.2, theta_max=0.8, min_window=5, max_window=20, delta=2)
        dtw.current_window = 10
        new_window = dtw.adjust_window(0.9)
        self.assertEqual(new_window, 8)

if __name__ == "__main__":
    unittest.main()
