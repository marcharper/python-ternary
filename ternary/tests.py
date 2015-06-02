import unittest

from ternary import plotting

class FunctionCases(unittest.TestCase):

    def test_normalize(self):
        l = [1,2,3]
        normalized = plotting.normalize(l)
        expected = [1./6, 2./6, 3./6]
        self.assertEqual(normalized, expected)
        # Test Exception
        self.assertRaises(ValueError, plotting.normalize, [0,0,0])

    def test_simplex_points(self):
        steps = 0
        expected = [(0, 0, 0)]
        points = list(plotting.simplex_points(steps=steps))
        self.assertEqual(points, expected)

        steps = 1
        expected = [(0, 0, 1), (0, 1, 0), (1, 0, 0)]
        points = list(plotting.simplex_points(steps=steps))
        self.assertEqual(points, expected)

        steps = 2
        expected = [(0, 0, 2), (0, 1, 1), (0, 2, 0), (1, 0, 1), (1, 1, 0), (2, 0, 0)]
        points = list(plotting.simplex_points(steps=steps))
        self.assertEqual(points, expected)

        steps = 3
        expected = [(0, 0, 3), (0, 1, 2), (0, 2, 1), (0, 3, 0), (1, 0, 2), (1, 1, 1), (1, 2, 0), (2, 0, 1), (2, 1, 0), (3, 0, 0)]
        points = list(plotting.simplex_points(steps=steps))
        self.assertEqual(points, expected)

    def test_simplex_points_without_boundary(self):
        steps = 0
        expected = []
        points = list(plotting.simplex_points(steps=steps, boundary_points=False))
        self.assertEqual(points, expected)

        steps = 1
        expected = []
        points = list(plotting.simplex_points(steps=steps, boundary_points=False))
        self.assertEqual(points, expected)

        steps = 2
        expected = []
        points = list(plotting.simplex_points(steps=steps, boundary_points=False))
        self.assertEqual(points, expected)

        steps = 3
        expected = [(1, 1, 1)]
        points = list(plotting.simplex_points(steps=steps, boundary_points=False))
        self.assertEqual(points, expected)

    def test_project_point(self):
        point = (0,0,0)
        projected = plotting.project_point(point)
        expected = (0.0, 0.0)
        self.assertEqual(projected, expected)

        point = (1,0,0)
        projected = plotting.project_point(point)
        expected = (0.0, 0.0)
        self.assertEqual(projected, expected)

        point = (0,1,0)
        projected = plotting.project_point(point)
        expected = (1.0, 0.0)
        self.assertEqual(projected, expected)

        point = (0,0,1)
        projected = plotting.project_point(point)
        expected = (0.5, plotting.SQRT3OVER2)
        self.assertEqual(projected, expected)

        point = (1,1,1)
        projected = plotting.project_point(point)
        expected = (1.5, plotting.SQRT3OVER2)
        self.assertEqual(projected, expected)

    def test_triangle_coordinates(self):
        #>>> ternary.triangle_coordinates(0,0)
        #[(0.0, 0.0), (1.0, 0.0), (0.5, 0.8660254037844386)]
        #>>> ternary.triangle_coordinates(0,1)
        #[(1.0, 0.0), (2.0, 0.0), (1.5, 0.8660254037844386)]
        #>>> ternary.triangle_coordinates(1,1)
        #[(1.5, 0.8660254037844386), (2.5, 0.8660254037844386), (2.0, 1.7320508075688772)]
        #>>> ternary.triangle_coordinates(2,2)
        #[(3.0, 1.7320508075688772), (4.0, 1.7320508075688772), (3.5, 2.598076211353316)]
        pass
    
if __name__ == "__main__":
    unittest.main()

    