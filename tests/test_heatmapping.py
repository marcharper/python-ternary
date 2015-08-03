
import unittest

from numpy.testing import assert_array_almost_equal

from ternary.heatmapping import triangle_coordinates, alt_triangle_coordinates, hexagon_coordinates
from ternary.helpers import SQRT3OVER2

class FunctionCases(unittest.TestCase):

    def test_coordinates(self):
        # Should be an equalilateral triangle
        coords = triangle_coordinates(1, 1, 1)
        expected = [(1, 1, 1), (2, 1, 0), (1, 2, 0)]
        self.assertEqual(coords, expected)

        coords = alt_triangle_coordinates(2, 2, 2)
        expected = [(2, 3, 1), (3, 2, 1), (3, 3, 0)]
        self.assertEqual(coords, expected)

        coords = hexagon_coordinates(1, 1, 1)
        expected = [(2./3, 5./3, 1.0), (4./3, 4./3, 1.0), (5./3, 2./3, 1.0),
                    (4./3, 1./3, 1.0), (2./3, 2./3, 1.), (1./3, 4./3, 1.0)]
        assert_array_almost_equal(coords, expected)


if __name__ == "__main__":
    unittest.main()
