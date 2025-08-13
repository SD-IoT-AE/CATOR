import unittest
from src.dynex import DYNEX
import numpy as np

class TestDYNEX(unittest.TestCase):

    def test_training_and_prediction(self):
        X = np.random.rand(50, 5)
        y = np.random.randint(0, 2, 50)
        model = DYNEX()
        model.fit(X, y)
        pred = model.predict(X[0].reshape(1, -1))
        self.assertIn(pred, [0, 1])

if __name__ == "__main__":
    unittest.main()
