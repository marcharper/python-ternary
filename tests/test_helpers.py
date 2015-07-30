
import unittest

from ternary.helpers import normalize, project_point, simplex_iterator, SQRT3OVER2, permute_point, compose_permutations

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
        projected = tuple(project_point(point))
        expected = (0.0, 0.0)
        self.assertEqual(projected, expected)

        point = (1, 0, 0)
        projected = tuple(project_point(point))
        expected = (1.0, 0.0)
        self.assertEqual(projected, expected)

        point = (0, 1, 0)
        projected = tuple(project_point(point))
        expected = (1./2, SQRT3OVER2)
        self.assertEqual(projected, expected)

        point = (0, 0, 1)
        projected = tuple(project_point(point))
        expected = (0, 0)
        self.assertEqual(projected, expected)

        point = (1, 1, 1)
        projected = tuple(project_point(point))
        expected = (1.5, SQRT3OVER2)
        self.assertEqual(projected, expected)

    def test_permutations(self):
        point = (3, 4, 5)
        permutation = "012"
        permuted = permute_point(point, permutation)
        self.assertEqual(permuted, point)

        permutation = "120"
        permuted = permute_point(point, permutation)
        self.assertEqual(permuted, (4, 5, 3))

        permutation = "102"
        permuted = permute_point(point, permutation)
        self.assertEqual(permuted, (4, 3, 5))

    def test_compose_permutations(self):
        inner = "brl"
        outer = "lrb"
        composite = compose_permutations(inner, outer)
        self.assertEqual(composite, outer)

        inner = "rlb"
        outer = "brl"
        composite = compose_permutations(inner, outer)
        self.assertEqual(composite, inner)

        inner = "rlb"
        outer = "lrb"
        composite = compose_permutations(inner, outer)
        self.assertEqual(composite, "rbl")

if __name__ == "__main__":
    unittest.main()
