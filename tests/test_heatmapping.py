
import unittest

from ternary.heatmapping import triangle_coordinates
from ternary.helpers import SQRT3OVER2

class FunctionCases(unittest.TestCase):

    def test_triangle_coordinates(self):
        # Should be an equalilateral triangle
        coords = triangle_coordinates(0, 0, 0)
        expected = [(0, 0, 0), (1, 0, -1), (0, 1, -1)]
        self.assertEqual(coords, expected)

if __name__ == "__main__":
    unittest.main()
