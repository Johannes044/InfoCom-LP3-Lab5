import unittest
from unittest.mock import patch, MagicMock
import math
import sys
import os
sys.path.append(os.path.abspath('../src'))
sys.path.append(os.path.abspath('../src/pi'))
import simulator 


class TestDroneSimulation(unittest.TestCase):

    def test_getMovement_non_zero_distance(self):
        src = (0.0, 0.0)
        dst = (3.0, 4.0)  # 5 units away
        lSpeed = 10
        dx, dy = simulator.getMovement(src, dst, lSpeed)
        self.assertAlmostEqual(dx, 6.0)
        self.assertAlmostEqual(dy, 8.0)

    def test_getMovement_zero_distance(self):
        src = (1.0, 1.0)
        dst = (1.0, 1.0)
        dx, dy = simulator.getMovement(src, dst, 10)
        self.assertEqual(dx, 0)
        self.assertEqual(dy, 0)

    def test_moveDrone(self):
        src = (0.0, 0.0)
        d_long = 2.0
        d_lat = 1.0
        # Rörelsen ska nu ske utan fördröjning
        new_coords = simulator.moveDrone(src, d_long, d_lat)
        # Här kollar vi på den faktiska rörelsen, utan att multiplicera med delay.
        self.assertAlmostEqual(new_coords[0], 2.0)
        self.assertAlmostEqual(new_coords[1], 1.0)

    @patch("simulator.requests.Session")
    def test_run_post_request_and_return_coords(self, mock_session_class):
        # Mock server
        mock_session = MagicMock()
        mock_session.post.return_value.status_code = 200
        mock_session_class.return_value.__enter__.return_value = mock_session

        # Setup
        id = "drone1"
        current_coords = (0.0, 0.0)
        to_coords = (0.0001, 0.0001)
        from_coords = (0.0, 0.0)
        simulator.utilities.lSpeed = 0.0002  # Se till att rörelsen är snabbare
        # Ingen delay längre, eftersom vi har tagit bort det från koden
        simulator.delay = 0.01  # Vi kan fortfarande definiera delay här om du vill ha en tidsintervall i vissa fall.

        # Kör drönarens rörelse
        result = simulator.run(id, current_coords, from_coords, to_coords, "http://fakeurl")

        self.assertIsInstance(result, tuple)
        self.assertAlmostEqual(result[0], to_coords[0], delta=0.00005)
        self.assertAlmostEqual(result[1], to_coords[1], delta=0.00005)
        self.assertTrue(mock_session.post.called)

if __name__ == "__main__":
    unittest.main()
