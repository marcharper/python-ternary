
import unittest

from numpy.testing import assert_array_equal

from ternary.helpers import normalize, project_point, simplex_iterator, SQRT3OVER2


class FunctionCases(unittest.TestCase):

    def test_normalize(self):
        l = [1,2,3]
        normalized = normalize(l)
        expected = [1./6, 2./6, 3./6]
        self.assertEqual(normalized, expected)
        # Test Exception
        self.assertRaises(ValueError, normalize, [0,0,0])

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
        expected = [(0, 0, 3), (0, 1, 2), (0, 2, 1), (0, 3, 0), (1, 0, 2), (1, 1, 1), (1, 2, 0), (2, 0, 1), (2, 1, 0), (3, 0, 0)]
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

    def test_project_point(self):
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


if __name__ == "__main__":
    unittest.main()
