import random
import unittest

from numpy.testing import assert_array_equal, assert_array_almost_equal

from ternary.helpers import normalize, project_point, planar_to_coordinates, simplex_iterator, SQRT3OVER2


class FunctionCases(unittest.TestCase):

    def test_normalize(self):
        l = [1, 2, 3]
        normalized = normalize(l)
        expected = [1./6, 2./6, 3./6]
        self.assertEqual(normalized, expected)
        # Test Exception
        self.assertRaises(ValueError, normalize, [0, 0, 0])

    def test_simplex_iterator(self):
        scale = 0
        expected = [(0, 0, 0)]
        points = list(simplex_iterator(scale=scale))
        self.assertEqual(points, expected)

        scale = 1
        expected = [(0, 0, 1), (0, 1, 0), (1, 0, 0)]
        points = list(simplex_iterator(scale=scale))
        self.assertEqual(points, expected)

        scale = 2
        expected = [(0, 0, 2), (0, 1, 1), (0, 2, 0), (1, 0, 1), (1, 1, 0), (2, 0, 0)]
        points = list(simplex_iterator(scale=scale))
        self.assertEqual(points, expected)

        scale = 3
        expected = [(0, 0, 3), (0, 1, 2), (0, 2, 1), (0, 3, 0), (1, 0, 2), (1, 1, 1), (1, 2, 0), (2, 0, 1), (2, 1, 0),
                    (3, 0, 0)]
        points = list(simplex_iterator(scale=scale))
        self.assertEqual(points, expected)

    def test_simplex_iterator_without_boundary(self):
        scale = 0
        expected = []
        points = list(simplex_iterator(scale=scale, boundary=False))
        self.assertEqual(points, expected)

        scale = 1
        expected = []
        points = list(simplex_iterator(scale=scale, boundary=False))
        self.assertEqual(points, expected)

        scale = 2
        expected = []
        points = list(simplex_iterator(scale=scale, boundary=False))
        self.assertEqual(points, expected)

        scale = 3
        expected = [(1, 1, 1)]
        points = list(simplex_iterator(scale=scale, boundary=False))
        self.assertEqual(points, expected)

    @staticmethod
    def test_project_point():
        point = (0, 0, 0)
        projected = project_point(point)
        expected = (0.0, 0.0)
        assert_array_equal(projected, expected)

        point = (1, 0, 0)
        projected = project_point(point)
        expected = (1.0, 0.0)
        assert_array_equal(projected, expected)

        point = (0, 1, 0)
        projected = project_point(point)
        expected = (0.5, SQRT3OVER2)
        assert_array_equal(projected, expected)

        point = (0, 0, 1)
        projected = project_point(point)
        expected = (0, 0)
        assert_array_equal(projected, expected)

        point = (1, 1, 1)
        projected = project_point(point)
        expected = (1.5, SQRT3OVER2)
        assert_array_equal(projected, expected)

    @staticmethod
    def test_planar_to_coordinates():
        projected = (0.0, 0.0)
        point = planar_to_coordinates(projected, scale=100)
        expected = (0.0, 0.0, 100.0)
        assert_array_equal(point, expected)

        projected = (100.0, 0.0)
        point = planar_to_coordinates(projected, scale=100)
        expected = (100.0, 0.0, 0.0)
        assert_array_equal(point, expected)

        projected = (40.0, 0)
        point = planar_to_coordinates(projected, scale=100)
        expected = (40.0,  0.0, 60.0)
        assert_array_equal(point, expected)

        projected = (10.0, SQRT3OVER2)
        point = planar_to_coordinates(projected, scale=100)
        expected = (9.5,  1.0, 89.5)
        assert_array_equal(point, expected)

        projected = (10.0, SQRT3OVER2)
        point = planar_to_coordinates(projected, scale=100)
        expected = (9.5,  1.0, 89.5)
        assert_array_equal(point, expected)

    @staticmethod
    def test_coordinate_maps():
        """Test that the coordinate projection functions are in fact inverses."""
        def random_point(scale=1):
            x = random.random() * scale
            y = random.random() * (scale - x)
            z = scale - x - y
            return x, y, z

        for _ in range(20):
            scale = random.randint(1, 100)
            p = random_point(scale=scale)
            projected = project_point(p)
            p2 = planar_to_coordinates(projected, scale=scale)
            assert_array_almost_equal(p, p2)


if __name__ == "__main__":
    unittest.main()
