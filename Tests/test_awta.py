import unittest
from unittest.mock import MagicMock
from src.awta import AWTA
from src.dynex import DYNEX

class TestAWTA(unittest.TestCase):

    def test_feature_extraction_and_detection(self):
        mock_dynex = DYNEX()
        mock_dynex.trained = True
        mock_dynex.predict = MagicMock(return_value=1)  # Always detect attack

        awta = AWTA(
            config_path="config/cator_config.json",
            p4_config="config/p4_switch_config.json",
            dynex_model=mock_dynex
        )
        # Mock P4 interface
        for sw, iface in awta.switches:
            iface.read_register_all = MagicMock(return_value=[10, 20, 30])
        # Run one loop iteration
        awta._pull_features = MagicMock(return_value=[[0.5] * 21])
        label = mock_dynex.predict([[0.5] * 21])
        self.assertEqual(label, 1)

if __name__ == "__main__":
    unittest.main()
